#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
import json
import dashscope
from http import HTTPStatus
from dashscope.audio.asr import Recognition
from openai import OpenAI
from src.utils.config import config
from src.utils.logger import get_logger
from src.utils.error_handling import AIIntegrationError

logger = get_logger(__name__)

class QwenAPI:
    def __init__(self):
        self.api_key = config.QWEN_API_KEY
        self.voice_model = config.QWEN_VOICE_MODEL
        self.chat_model = config.QWEN_CHAT_MODEL
        self.base_url = "https://api.qwen.com/v1"
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        # 配置dashscope API key
        dashscope.api_key = self.api_key
        # 初始化OpenAI客户端（使用阿里云百炼兼容模式）
        self.client = OpenAI(
            api_key=self.api_key,
            base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"
        )
    
    def recognize_speech(self, audio_data):
        """调用千问语音转文字API"""
        try:
            # 保存音频数据到临时文件
            import tempfile
            import os
            
            with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as temp_file:
                temp_file.write(audio_data)
                temp_file_path = temp_file.name
            
            try:
                # 使用dashscope的Recognition类
                recognition = Recognition(model=self.voice_model,
                                       format='wav',
                                       sample_rate=16000,
                                       language_hints=['zh', 'en'],
                                       callback=None)
                result = recognition.call(temp_file_path)
                
                if result and result.status_code == HTTPStatus.OK:
                    text = result.get_sentence()
                    if text:
                        logger.info(f"语音识别成功: {text[:50]}...")
                        return text
                    else:
                        error_message = "语音识别失败: 未返回识别结果"
                        logger.error(error_message)
                        raise AIIntegrationError(error_message)
                else:
                    error_message = f"语音识别失败: {result.message if result else '未知错误'}"
                    logger.error(error_message)
                    raise AIIntegrationError(error_message)
            finally:
                # 清理临时文件
                if os.path.exists(temp_file_path):
                    os.unlink(temp_file_path)
        except Exception as e:
            logger.error(f"Speech recognition error: {str(e)}")
            raise AIIntegrationError(f"语音识别失败: {str(e)}")
    
    def chat_completion(self, prompt, context=None, enable_search=False, stream=False):
        """调用千问问答API
        
        Args:
            prompt: 用户输入的提示
            context: 上下文信息
            enable_search: 是否启用联网搜索功能
            stream: 是否启用流式输出
        """
        try:
            messages = []
            if context:
                messages.append({"role": "system", "content": context})
            messages.append({"role": "user", "content": prompt})
            
            # 构建请求参数
            params = {
                "model": self.chat_model,
                "messages": messages,
                "temperature": 0.7,
                "max_tokens": 1024,
                "stream": stream,
                "extra_body": {"enable_thinking": True}
            }
            
            # 如果启用联网搜索，添加工具调用
            if enable_search:
                params["tools"] = [
                    {"type": "web_search"},
                    {"type": "web_extractor"}
                ]
            
            # 使用OpenAI SDK调用API
            completion = self.client.chat.completions.create(**params)
            
            if stream:
                # 流式输出模式
                return completion
            else:
                # 非流式输出模式
                return completion.choices[0].message.content
        except Exception as e:
            logger.error(f"Chat completion error: {str(e)}")
            raise AIIntegrationError(f"问答生成失败: {str(e)}")
    
    def get_term_explanation(self, term, enable_search=True):
        """获取专业术语解释，默认启用联网搜索获取最新信息
        
        Args:
            term: 专业术语
            enable_search: 是否启用联网搜索，默认为True
        """
        prompt = f"请解释以下专业术语：{term}，要求解释准确、简洁，适合学生理解。"
        return self.chat_completion(prompt, enable_search=enable_search)
    
    def answer_question_with_search(self, question, context=None):
        """回答问题并启用联网搜索获取相关信息
        
        Args:
            question: 问题内容
            context: 上下文信息（可选）
        """
        try:
            # 构建完整的提示
            full_prompt = question
            if context:
                full_prompt = f"基于以下上下文回答问题：\n{context}\n\n问题：{question}"
            
            # 调用千问API，启用联网搜索
            answer = self.chat_completion(full_prompt, enable_search=True)
            logger.info(f"生成问题答案（含联网搜索）: {question[:50]}...")
            return answer
        except Exception as e:
            logger.error(f"回答问题失败: {str(e)}")
            return f"无法回答该问题: {str(e)}"
    
    def search_and_summarize(self, query):
        """使用千问模型的联网搜索功能搜索并总结信息
        
        Args:
            query: 搜索查询内容
        """
        try:
            prompt = f"请搜索以下主题并提供详细的总结：{query}"
            result = self.chat_completion(prompt, enable_search=True)
            logger.info(f"搜索并总结: {query[:50]}...")
            return result
        except Exception as e:
            logger.error(f"搜索失败: {str(e)}")
            return f"搜索失败: {str(e)}"

qwen_api = QwenAPI()
