#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sqlite3
import os
import json
from datetime import datetime
from src.utils.config import config
from src.utils.logger import get_logger
from src.utils.error_handling import DataStorageError

logger = get_logger(__name__)

class DataStorage:
    def __init__(self):
        # 确保数据库目录存在
        db_dir = os.path.dirname(config.DATABASE_PATH)
        if db_dir and not os.path.exists(db_dir):
            os.makedirs(db_dir)
        
        self.db_path = config.DATABASE_PATH
        self._init_db()
    
    def _init_db(self):
        """初始化数据库"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # 创建语音转文字结果表
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS transcriptions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    text TEXT NOT NULL,
                    timestamp TEXT NOT NULL,
                    duration REAL,
                    metadata TEXT
                )
            ''')
            
            # 创建专业术语表
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS terms (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    term TEXT NOT NULL UNIQUE,
                    explanation TEXT NOT NULL,
                    context TEXT,
                    course TEXT,
                    is_mastered INTEGER DEFAULT 0,
                    created_at TEXT NOT NULL,
                    updated_at TEXT NOT NULL
                )
            ''')
            
            # 创建术语出现记录表
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS term_occurrences (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    term_id INTEGER,
                    transcription_id INTEGER,
                    position INTEGER,
                    timestamp TEXT NOT NULL,
                    FOREIGN KEY (term_id) REFERENCES terms(id),
                    FOREIGN KEY (transcription_id) REFERENCES transcriptions(id)
                )
            ''')
            
            conn.commit()
            conn.close()
            logger.info("数据库初始化完成")
        except Exception as e:
            logger.error(f"数据库初始化失败: {str(e)}")
            raise DataStorageError(f"数据库初始化失败: {str(e)}")
    
    def save_transcription(self, text, duration=None, metadata=None):
        """保存语音转文字结果"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            timestamp = datetime.now().isoformat()
            metadata_json = json.dumps(metadata) if metadata else None
            
            cursor.execute(
                "INSERT INTO transcriptions (text, timestamp, duration, metadata) VALUES (?, ?, ?, ?)",
                (text, timestamp, duration, metadata_json)
            )
            
            transcription_id = cursor.lastrowid
            conn.commit()
            conn.close()
            
            logger.info(f"保存转文字结果成功，ID: {transcription_id}")
            return transcription_id
        except Exception as e:
            logger.error(f"保存转文字结果失败: {str(e)}")
            raise DataStorageError(f"保存转文字结果失败: {str(e)}")
    
    def get_transcriptions(self, limit=100, offset=0):
        """获取转文字结果列表"""
        try:
            conn = sqlite3.connect(self.db_path)
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            
            cursor.execute(
                "SELECT * FROM transcriptions ORDER BY timestamp DESC LIMIT ? OFFSET ?",
                (limit, offset)
            )
            
            results = cursor.fetchall()
            conn.close()
            
            # 转换为字典列表
            transcriptions = []
            for row in results:
                transcription = dict(row)
                if transcription['metadata']:
                    transcription['metadata'] = json.loads(transcription['metadata'])
                transcriptions.append(transcription)
            
            return transcriptions
        except Exception as e:
            logger.error(f"获取转文字结果失败: {str(e)}")
            raise DataStorageError(f"获取转文字结果失败: {str(e)}")
    
    def save_term(self, term, explanation, context=None, course=None):
        """保存专业术语"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            timestamp = datetime.now().isoformat()
            
            # 检查术语是否已存在
            cursor.execute("SELECT id FROM terms WHERE term = ?", (term,))
            existing_term = cursor.fetchone()
            
            if existing_term:
                # 更新现有术语
                cursor.execute(
                    "UPDATE terms SET explanation = ?, context = ?, course = ?, updated_at = ? WHERE id = ?",
                    (explanation, context, course, timestamp, existing_term[0])
                )
                term_id = existing_term[0]
            else:
                # 插入新术语
                cursor.execute(
                    "INSERT INTO terms (term, explanation, context, course, created_at, updated_at) VALUES (?, ?, ?, ?, ?, ?)",
                    (term, explanation, context, course, timestamp, timestamp)
                )
                term_id = cursor.lastrowid
            
            conn.commit()
            conn.close()
            
            logger.info(f"保存术语成功，ID: {term_id}")
            return term_id
        except Exception as e:
            logger.error(f"保存术语失败: {str(e)}")
            raise DataStorageError(f"保存术语失败: {str(e)}")
    
    def get_terms(self, is_mastered=None):
        """获取专业术语列表"""
        try:
            conn = sqlite3.connect(self.db_path)
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            
            if is_mastered is not None:
                cursor.execute("SELECT * FROM terms WHERE is_mastered = ? ORDER BY term", (is_mastered,))
            else:
                cursor.execute("SELECT * FROM terms ORDER BY term")
            
            results = cursor.fetchall()
            conn.close()
            
            # 转换为字典列表
            terms = [dict(row) for row in results]
            return terms
        except Exception as e:
            logger.error(f"获取术语列表失败: {str(e)}")
            raise DataStorageError(f"获取术语列表失败: {str(e)}")
    
    def update_term_mastery(self, term_id, is_mastered):
        """更新术语掌握状态"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            timestamp = datetime.now().isoformat()
            
            cursor.execute(
                "UPDATE terms SET is_mastered = ?, updated_at = ? WHERE id = ?",
                (is_mastered, timestamp, term_id)
            )
            
            conn.commit()
            conn.close()
            
            logger.info(f"更新术语掌握状态成功，ID: {term_id}, 掌握状态: {is_mastered}")
        except Exception as e:
            logger.error(f"更新术语掌握状态失败: {str(e)}")
            raise DataStorageError(f"更新术语掌握状态失败: {str(e)}")
    
    def save_term_occurrence(self, term_id, transcription_id, position):
        """保存术语出现记录"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            timestamp = datetime.now().isoformat()
            
            cursor.execute(
                "INSERT INTO term_occurrences (term_id, transcription_id, position, timestamp) VALUES (?, ?, ?, ?)",
                (term_id, transcription_id, position, timestamp)
            )
            
            occurrence_id = cursor.lastrowid
            conn.commit()
            conn.close()
            
            logger.info(f"保存术语出现记录成功，ID: {occurrence_id}")
            return occurrence_id
        except Exception as e:
            logger.error(f"保存术语出现记录失败: {str(e)}")
            raise DataStorageError(f"保存术语出现记录失败: {str(e)}")
    
    def get_term_occurrences(self, term_id=None, transcription_id=None):
        """获取术语出现记录"""
        try:
            conn = sqlite3.connect(self.db_path)
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            
            if term_id:
                cursor.execute("SELECT * FROM term_occurrences WHERE term_id = ?", (term_id,))
            elif transcription_id:
                cursor.execute("SELECT * FROM term_occurrences WHERE transcription_id = ?", (transcription_id,))
            else:
                cursor.execute("SELECT * FROM term_occurrences")
            
            results = cursor.fetchall()
            conn.close()
            
            # 转换为字典列表
            occurrences = [dict(row) for row in results]
            return occurrences
        except Exception as e:
            logger.error(f"获取术语出现记录失败: {str(e)}")
            raise DataStorageError(f"获取术语出现记录失败: {str(e)}")

# 示例用法
# storage = DataStorage()
# storage.save_transcription("这是一段测试文本", 10.5, {"speaker": "test"})
# storage.save_term("人工智能", "人工智能是研究、开发用于模拟、延伸和扩展人的智能的理论、方法、技术及应用系统的一门新的技术科学")
# storage.update_term_mastery(1, 1)