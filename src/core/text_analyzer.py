#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
import spacy
from src.api.qwen_api import qwen_api
from src.api.search_api import search_api
from src.utils.logger import get_logger
from src.utils.error_handling import TextAnalysisError

logger = get_logger(__name__)

class TextAnalyzer:
    def __init__(self):
        try:
            # 加载Spacy中文模型
            self.nlp = spacy.load("zh_core_web_sm")
        except Exception as e:
            logger.warning(f"加载Spacy模型失败，将使用基于规则的方法: {str(e)}")
            self.nlp = None
        
        # 问题模式正则表达式
        self.question_patterns = [
            r'什么是.*?[？?]',
            r'什么叫.*?[？?]',
            r'什么.*?[？?]',
            r'为什么.*?[？?]',
            r'怎么.*?[？?]',
            r'如何.*?[？?]',
            r'何时.*?[？?]',
            r'何地.*?[？?]',
            r'谁.*?[？?]',
            r'哪个.*?[？?]',
            r'哪些.*?[？?]',
            r'有什么.*?[？?]',
            r'为什么.*?[？?]',
            r'怎样.*?[？?]',
        ]
        
        # 专业术语特征词
        self.term_indicators = [
            '是指', '定义为', '称为', '叫做', '即', '就是',
            '所谓', '指的是', '意味着', '表示', '代表'
        ]
    
    def analyze_text(self, text):
        """分析文本，识别术语和问题"""
        try:
            results = {
                'terms': self.identify_terms(text),
                'questions': self.identify_questions(text)
            }
            return results
        except Exception as e:
            logger.error(f"文本分析失败: {str(e)}")
            raise TextAnalysisError(f"文本分析失败: {str(e)}")
    
    def identify_terms(self, text):
        """识别专业术语"""
        terms = []
        
        if self.nlp:
            # 使用Spacy进行命名实体识别
            doc = self.nlp(text)
            for ent in doc.ents:
                if ent.label_ in ['ORG', 'PERSON', 'GPE', 'LOC', 'PRODUCT', 'EVENT']:
                    terms.append(ent.text)
        
        # 基于规则的术语识别
        # 1. 识别包含术语特征词的短语
        for indicator in self.term_indicators:
            pattern = r'(\w+\s*)+' + re.escape(indicator) + r'(\w+\s*)+'
            matches = re.findall(pattern, text)
            for match in matches:
                # 提取术语部分（特征词之前的内容）
                term_candidate = match[0].strip()
                if term_candidate and len(term_candidate) > 1:
                    terms.append(term_candidate)
        
        # 2. 识别可能的专业术语（长度大于2的名词短语）
        pattern = r'[\u4e00-\u9fa5]{2,}'
        matches = re.findall(pattern, text)
        for match in matches:
            if len(match) > 2 and match not in terms:
                terms.append(match)
        
        # 去重
        terms = list(set(terms))
        logger.info(f"识别到术语: {terms}")
        return terms
    
    def identify_questions(self, text):
        """识别问题"""
        questions = []
        
        # 使用正则表达式匹配问题模式
        for pattern in self.question_patterns:
            matches = re.findall(pattern, text)
            questions.extend(matches)
        
        # 去重
        questions = list(set(questions))
        logger.info(f"识别到问题: {questions}")
        return questions
    
    def get_term_explanation(self, term):
        """获取术语解释"""
        try:
            explanation = qwen_api.get_term_explanation(term)
            logger.info(f"获取术语解释: {term} - {explanation[:50]}...")
            return explanation
        except Exception as e:
            logger.error(f"获取术语解释失败: {str(e)}")
            return f"无法获取{term}的解释"
    
    def answer_question(self, question, context=None):
        """回答问题"""
        try:
            # 获取相关信息
            relevant_info = search_api.get_relevant_info(question)
            
            # 构建上下文
            full_context = ""
            if context:
                full_context += f"上下文信息: {context}\n"
            if relevant_info:
                full_context += f"相关搜索信息: {relevant_info}\n"
            
            # 调用千问API生成答案
            answer = qwen_api.chat_completion(question, full_context)
            logger.info(f"生成问题答案: {question[:50]}... - {answer[:50]}...")
            return answer
        except Exception as e:
            logger.error(f"回答问题失败: {str(e)}")
            return f"无法回答该问题"

# 示例用法
# analyzer = TextAnalyzer()
# text = "什么是人工智能？人工智能是指模拟人类智能的技术。"
# results = analyzer.analyze_text(text)
# print(f"识别到的术语: {results['terms']}")
# print(f"识别到的问题: {results['questions']}")
# for term in results['terms']:
#     print(f"{term}: {analyzer.get_term_explanation(term)}")
# for question in results['questions']:
#     print(f"Q: {question}\nA: {analyzer.answer_question(question)}")