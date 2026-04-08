#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
搜索API模块 - 使用千问模型的联网搜索功能

注意：此模块现在作为千问API搜索功能的包装器，不再依赖外部搜索API。
所有搜索功能都通过千问模型的内置联网搜索工具实现。
"""

from src.api.qwen_api import qwen_api
from src.utils.logger import get_logger
from src.utils.error_handling import AIIntegrationError

logger = get_logger(__name__)

class SearchAPI:
    """搜索API类 - 使用千问模型的联网搜索功能"""
    
    def __init__(self):
        """初始化搜索API，使用千问API的联网搜索功能"""
        self.qwen_api = qwen_api
        logger.info("搜索API初始化完成，使用千问模型内置联网搜索功能")
    
    def search(self, query, num_results=5):
        """执行搜索并返回结果
        
        使用千问模型的联网搜索功能获取搜索结果
        
        Args:
            query: 搜索查询内容
            num_results: 期望的结果数量（千问模型会自动处理）
            
        Returns:
            搜索结果列表，包含标题、链接和摘要
        """
        try:
            # 使用千问API的搜索并总结功能
            search_result = self.qwen_api.search_and_summarize(query)
            
            # 将结果格式化为标准格式
            return [{
                "title": f"搜索结果: {query[:30]}...",
                "link": "",
                "snippet": search_result
            }]
        except Exception as e:
            logger.error(f"搜索失败: {str(e)}")
            raise AIIntegrationError(f"搜索失败: {str(e)}")
    
    def get_relevant_info(self, query):
        """获取相关信息，用于回答问题
        
        Args:
            query: 查询内容
            
        Returns:
            相关信息文本
        """
        try:
            # 使用千问API直接搜索并获取相关信息
            result = self.qwen_api.search_and_summarize(query)
            return result
        except Exception as e:
            logger.error(f"获取相关信息失败: {str(e)}")
            return ""
    
    def search_term_info(self, term):
        """搜索专业术语的相关信息
        
        Args:
            term: 专业术语
            
        Returns:
            术语的相关信息
        """
        try:
            query = f"{term} 专业术语解释 定义"
            result = self.qwen_api.search_and_summarize(query)
            return result
        except Exception as e:
            logger.error(f"搜索术语信息失败: {str(e)}")
            return ""

# 创建全局搜索API实例
search_api = SearchAPI()
