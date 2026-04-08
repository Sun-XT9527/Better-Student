#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
AI集成模块 - 使用千问模型的联网搜索功能

此模块集成了千问API的语音转文字、问答和联网搜索功能，
无需额外配置外部搜索API，所有搜索功能都通过千问模型内置工具实现。
"""

from src.api.qwen_api import qwen_api
from src.api.search_api import search_api
from src.utils.logger import get_logger
from src.utils.error_handling import AIIntegrationError

logger = get_logger(__name__)

class AIIntegration:
    """AI集成类 - 使用千问模型的联网搜索功能"""
    
    def __init__(self):
        self.qwen_api = qwen_api
        self.search_api = search_api
    
    def process_term(self, term):
        """处理专业术语，获取解释和相关信息
        
        使用千问模型的联网搜索功能获取术语的最新解释和相关信息
        
        Args:
            term: 专业术语
            
        Returns:
            包含术语、解释和相关信息的字典
        """
        try:
            # 获取术语解释（默认启用联网搜索）
            explanation = self.qwen_api.get_term_explanation(term, enable_search=True)
            
            # 使用千问搜索获取相关信息
            search_results = self.search_api.search_term_info(term)
            
            logger.info(f"处理术语成功: {term}")
            return {
                'term': term,
                'explanation': explanation,
                'related_info': search_results
            }
        except Exception as e:
            logger.error(f"处理术语失败: {str(e)}")
            raise AIIntegrationError(f"处理术语失败: {str(e)}")
    
    def process_question(self, question, context=None):
        """处理问题，生成答案
        
        使用千问模型的联网搜索功能获取最新信息并生成答案
        
        Args:
            question: 问题内容
            context: 上下文信息（可选）
            
        Returns:
            包含问题、答案和相关信息的字典
        """
        try:
            # 使用千问API的联网搜索功能直接回答问题
            answer = self.qwen_api.answer_question_with_search(question, context)
            
            # 同时获取搜索相关信息
            relevant_info = self.search_api.get_relevant_info(question)
            
            logger.info(f"处理问题成功: {question[:50]}...")
            return {
                'question': question,
                'answer': answer,
                'relevant_info': relevant_info
            }
        except Exception as e:
            logger.error(f"处理问题失败: {str(e)}")
            raise AIIntegrationError(f"处理问题失败: {str(e)}")
    
    def analyze_context(self, text):
        """分析上下文，提取关键信息
        
        Args:
            text: 待分析的文本
            
        Returns:
            分析结果
        """
        try:
            prompt = f"请分析以下文本，提取关键信息和主题: {text}"
            analysis = self.qwen_api.chat_completion(prompt, enable_search=False)
            return analysis
        except Exception as e:
            logger.error(f"分析上下文失败: {str(e)}")
            raise AIIntegrationError(f"分析上下文失败: {str(e)}")
    
    def search_and_learn(self, topic):
        """搜索主题并生成学习材料
        
        使用千问模型的联网搜索功能搜索主题并生成详细的学习材料
        
        Args:
            topic: 学习主题
            
        Returns:
            学习材料
        """
        try:
            prompt = f"请搜索关于'{topic}'的详细信息，并生成一份适合学生学习的材料，包括定义、关键概念、应用场景等。"
            learning_material = self.qwen_api.chat_completion(prompt, enable_search=True)
            logger.info(f"生成学习材料成功: {topic}")
            return learning_material
        except Exception as e:
            logger.error(f"生成学习材料失败: {str(e)}")
            raise AIIntegrationError(f"生成学习材料失败: {str(e)}")
    
    def analyze_text(self, text):
        """分析文本，识别术语和问题
        
        使用千问模型直接分析文本，识别其中的专业术语和问题
        
        Args:
            text: 待分析的文本
            
        Returns:
            包含术语和问题的字典
        """
        try:
            prompt = f"请分析以下文本，识别其中的专业术语和问题：\n\n{text}\n\n请按照以下格式返回结果：\n术语：\n1. 术语1\n2. 术语2\n...\n问题：\n1. 问题1\n2. 问题2\n...\n\n注意：\n- 术语是指专业概念、专有名词等\n- 问题是指以问号结尾的疑问句\n- 请确保识别准确，不要遗漏重要术语和问题\n- 只返回识别结果，不要添加其他解释"
            
            result = self.qwen_api.chat_completion(prompt, enable_search=False)
            
            # 解析结果
            terms = []
            questions = []
            
            # 提取术语部分
            if "术语：" in result:
                terms_section = result.split("术语：")[1].split("问题：")[0].strip()
                for line in terms_section.split('\n'):
                    if line.strip() and (line.strip().startswith('1.') or line.strip().startswith('2.') or line.strip().startswith('3.') or line.strip().startswith('4.') or line.strip().startswith('5.')):
                        term = line.strip()[3:].strip()
                        if term:
                            terms.append(term)
            
            # 提取问题部分
            if "问题：" in result:
                questions_section = result.split("问题：")[1].strip()
                for line in questions_section.split('\n'):
                    if line.strip() and (line.strip().startswith('1.') or line.strip().startswith('2.') or line.strip().startswith('3.') or line.strip().startswith('4.') or line.strip().startswith('5.')):
                        question = line.strip()[3:].strip()
                        if question:
                            questions.append(question)
            
            logger.info(f"分析文本成功，识别到 {len(terms)} 个术语和 {len(questions)} 个问题")
            return {
                'terms': terms,
                'questions': questions
            }
        except Exception as e:
            logger.error(f"分析文本失败: {str(e)}")
            raise AIIntegrationError(f"分析文本失败: {str(e)}")

# 示例用法
# ai = AIIntegration()
# term_result = ai.process_term("人工智能")
# print(f"术语: {term_result['term']}")
# print(f"解释: {term_result['explanation']}")
# 
# question_result = ai.process_question("什么是人工智能？")
# print(f"问题: {question_result['question']}")
# print(f"答案: {question_result['answer']}")
# 
# learning_material = ai.search_and_learn("机器学习")
# print(f"学习材料: {learning_material}")
