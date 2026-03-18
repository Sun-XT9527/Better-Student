#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup
from src.utils.config import config
from src.utils.logger import get_logger
from src.utils.error_handling import AIIntegrationError

logger = get_logger(__name__)

class SearchAPI:
    def __init__(self):
        self.api_key = config.SEARCH_API_KEY
        self.search_engine = config.SEARCH_ENGINE
    
    def search(self, query, num_results=5):
        """执行搜索并返回结果"""
        try:
            if self.search_engine == 'google':
                return self._google_search(query, num_results)
            elif self.search_engine == 'bing':
                return self._bing_search(query, num_results)
            else:
                raise AIIntegrationError(f"不支持的搜索引擎: {self.search_engine}")
        except Exception as e:
            logger.error(f"Search error: {str(e)}")
            raise AIIntegrationError(f"搜索失败: {str(e)}")
    
    def _google_search(self, query, num_results):
        """Google搜索实现"""
        # 这里使用Google Custom Search API
        # 实际使用时需要替换为真实的API调用
        url = "https://www.googleapis.com/customsearch/v1"
        params = {
            "key": self.api_key,
            "cx": "your_search_engine_id",  # 需要设置搜索引擎ID
            "q": query,
            "num": num_results
        }
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        results = response.json()
        
        # 提取搜索结果
        search_results = []
        if "items" in results:
            for item in results["items"]:
                search_results.append({
                    "title": item.get("title", ""),
                    "link": item.get("link", ""),
                    "snippet": item.get("snippet", "")
                })
        
        return search_results
    
    def _bing_search(self, query, num_results):
        """Bing搜索实现"""
        # 这里使用Bing Search API
        # 实际使用时需要替换为真实的API调用
        url = "https://api.bing.microsoft.com/v7.0/search"
        headers = {
            "Ocp-Apim-Subscription-Key": self.api_key
        }
        params = {
            "q": query,
            "count": num_results
        }
        response = requests.get(url, headers=headers, params=params, timeout=10)
        response.raise_for_status()
        results = response.json()
        
        # 提取搜索结果
        search_results = []
        if "webPages" in results and "value" in results["webPages"]:
            for item in results["webPages"]["value"]:
                search_results.append({
                    "title": item.get("name", ""),
                    "link": item.get("url", ""),
                    "snippet": item.get("snippet", "")
                })
        
        return search_results
    
    def get_relevant_info(self, query):
        """获取相关信息，用于回答问题"""
        results = self.search(query, num_results=3)
        # 提取关键信息
        relevant_info = "\n".join([f"{item['title']}: {item['snippet']}" for item in results])
        return relevant_info

search_api = SearchAPI()