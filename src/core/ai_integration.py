#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from src.api.qwen_api import qwen_api
from src.api.search_api import search_api
from src.utils.logger import get_logger
from src.utils.error_handling import AIIntegrationError

logger = get_logger(__name__)

class AIIntegration:
    def __init__(self):
        self.qwen_api = qwen_api
        self.search_api = search_api
    
    def process_term(self, term):
        """处理专业术语，获取解释"""
        try:
            # 获取术语解释
            explanation = self.qwen_api.get_term_explanation(term)
            # 搜索相关信息
            search_results = self.search_api.search(term, num_results=3)
            
            return {
                'term': term,
                'explanation': explanation,
                'related_info': search_results
            }
        except Exception as e:
            logger.error(f"处理术语失败: {str(e)}")
            raise AIIntegrationError(f"处理术语失败: {str(e)}")
    
    def process_question(self, question, context=None):
        """处理问题，生成答案"""
        try:
            # 搜索相关信息
            relevant_info = self.search_api.get_relevant_info(question)
            
            # 构建完整上下文
            full_context = ""
            if context:
                full_context += f"上下文信息: {context}\n"
            if relevant_info:
                full_context += f"相关搜索信息: {relevant_info}\n"
            
            # 生成答案
            answer = self.qwen_api.chat_completion(question, full_context)
            
            return {
                'question': question,
                'answer': answer,
                'relevant_info': relevant_info
            }
        except Exception as e:
            logger.error(f"处理问题失败: {str(e)}")
            raise AIIntegrationError(f"处理问题失败: {str(e)}")
    
    def analyze_context(self, text):
        """分析上下文，提取关键信息"""
        try:
            prompt = f"请分析以下文本，提取关键信息和主题: {text}"
            analysis = self.qwen_api.chat_completion(prompt)
            return analysis
        except Exception as e:
            logger.error(f"分析上下文失败: {str(e)}")
            raise AIIntegrationError(f"分析上下文失败: {str(e)}")

# 示例用法
# ai = AIIntegration()
# term_result = ai.process_term("人工智能")
# print(f"术语: {term_result['term']}")
# print(f"解释: {term_result['explanation']}")
# 
# question_result = ai.process_question("什么是人工智能？")
# print(f"问题: {question_result['question']}")
# print(f"答案: {question_result['answer']}")