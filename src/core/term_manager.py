#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from src.core.data_storage import DataStorage
from src.core.ai_integration import AIIntegration
from src.utils.logger import get_logger
from src.utils.error_handling import TermManagerError

logger = get_logger(__name__)

class TermManager:
    def __init__(self):
        self.storage = DataStorage()
        self.ai = AIIntegration()
    
    def add_term(self, term, explanation=None, context=None, course=None):
        """添加专业术语"""
        try:
            # 如果没有提供解释，自动获取
            if not explanation:
                term_info = self.ai.process_term(term)
                explanation = term_info['explanation']
            
            # 保存术语
            term_id = self.storage.save_term(term, explanation, context, course)
            logger.info(f"添加术语成功: {term}, ID: {term_id}")
            return term_id
        except Exception as e:
            logger.error(f"添加术语失败: {str(e)}")
            raise TermManagerError(f"添加术语失败: {str(e)}")
    
    def get_term(self, term):
        """获取术语信息"""
        try:
            terms = self.storage.get_terms()
            for t in terms:
                if t['term'] == term:
                    return t
            return None
        except Exception as e:
            logger.error(f"获取术语失败: {str(e)}")
            raise TermManagerError(f"获取术语失败: {str(e)}")
    
    def get_all_terms(self, is_mastered=None):
        """获取所有术语"""
        try:
            return self.storage.get_terms(is_mastered)
        except Exception as e:
            logger.error(f"获取术语列表失败: {str(e)}")
            raise TermManagerError(f"获取术语列表失败: {str(e)}")
    
    def update_term_mastery(self, term_id, is_mastered):
        """更新术语掌握状态"""
        try:
            self.storage.update_term_mastery(term_id, is_mastered)
            logger.info(f"更新术语掌握状态成功: ID {term_id}, 掌握状态: {is_mastered}")
        except Exception as e:
            logger.error(f"更新术语掌握状态失败: {str(e)}")
            raise TermManagerError(f"更新术语掌握状态失败: {str(e)}")
    
    def mark_term_mastered(self, term_id):
        """标记术语为已掌握"""
        self.update_term_mastery(term_id, 1)
    
    def mark_term_unmastered(self, term_id):
        """标记术语为未掌握"""
        self.update_term_mastery(term_id, 0)
    
    def record_term_occurrence(self, term, transcription_id, position):
        """记录术语出现"""
        try:
            # 检查术语是否已存在
            existing_term = self.get_term(term)
            if not existing_term:
                # 不存在则添加
                term_id = self.add_term(term)
            else:
                term_id = existing_term['id']
            
            # 记录出现位置
            occurrence_id = self.storage.save_term_occurrence(term_id, transcription_id, position)
            logger.info(f"记录术语出现成功: {term}, 转录ID: {transcription_id}, 位置: {position}")
            return occurrence_id
        except Exception as e:
            logger.error(f"记录术语出现失败: {str(e)}")
            raise TermManagerError(f"记录术语出现失败: {str(e)}")
    
    def get_term_occurrences(self, term_id=None, transcription_id=None):
        """获取术语出现记录"""
        try:
            return self.storage.get_term_occurrences(term_id, transcription_id)
        except Exception as e:
            logger.error(f"获取术语出现记录失败: {str(e)}")
            raise TermManagerError(f"获取术语出现记录失败: {str(e)}")
    
    def process_terms_in_text(self, text, transcription_id):
        """处理文本中的术语"""
        try:
            from src.core.text_analyzer import TextAnalyzer
            analyzer = TextAnalyzer()
            
            # 识别术语
            terms = analyzer.identify_terms(text)
            
            # 处理每个术语
            processed_terms = []
            for term in terms:
                # 记录术语出现
                position = text.find(term)
                if position != -1:
                    # 确保术语存在于数据库中
                    self.record_term_occurrence(term, transcription_id, position)
                    
                    # 获取术语信息
                    term_info = self.get_term(term)
                    if term_info:
                        processed_terms.append(term_info)
            
            logger.info(f"处理文本中的术语成功，识别到 {len(terms)} 个术语")
            return processed_terms
        except Exception as e:
            logger.error(f"处理文本中的术语失败: {str(e)}")
            raise TermManagerError(f"处理文本中的术语失败: {str(e)}")

# 示例用法
# term_manager = TermManager()
# term_manager.add_term("人工智能", "人工智能是研究、开发用于模拟、延伸和扩展人的智能的理论、方法、技术及应用系统的一门新的技术科学")
# term_manager.mark_term_mastered(1)
# terms = term_manager.get_all_terms()
# print(f"所有术语: {[t['term'] for t in terms]}")