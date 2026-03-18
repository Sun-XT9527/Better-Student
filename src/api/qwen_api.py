#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
import json
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
    
    def recognize_speech(self, audio_data):
        """调用千问语音转文字API"""
        try:
            url = f"{self.base_url}/speech/recognize"
            data = {
                "model": self.voice_model,
                "audio": audio_data,
                "language": "zh-CN",
                "encoding": "wav"
            }
            response = requests.post(url, headers=self.headers, json=data, timeout=10)
            response.raise_for_status()
            result = response.json()
            return result.get("text", "")
        except Exception as e:
            logger.error(f"Speech recognition error: {str(e)}")
            raise AIIntegrationError(f"语音识别失败: {str(e)}")
    
    def chat_completion(self, prompt, context=None):
        """调用千问问答API"""
        try:
            url = f"{self.base_url}/chat/completions"
            messages = []
            if context:
                messages.append({"role": "system", "content": context})
            messages.append({"role": "user", "content": prompt})
            data = {
                "model": self.chat_model,
                "messages": messages,
                "temperature": 0.7,
                "max_tokens": 1024
            }
            response = requests.post(url, headers=self.headers, json=data, timeout=15)
            response.raise_for_status()
            result = response.json()
            return result["choices"][0]["message"]["content"]
        except Exception as e:
            logger.error(f"Chat completion error: {str(e)}")
            raise AIIntegrationError(f"问答生成失败: {str(e)}")
    
    def get_term_explanation(self, term):
        """获取专业术语解释"""
        prompt = f"请解释以下专业术语：{term}，要求解释准确、简洁，适合学生理解。"
        return self.chat_completion(prompt)

qwen_api = QwenAPI()