#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QTextEdit, QLabel, QListWidget, QListWidgetItem, QSplitter
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QTextCursor
from src.core.text_analyzer import TextAnalyzer
from src.core.ai_integration import AIIntegration
from src.utils.logger import get_logger

logger = get_logger(__name__)

class AnalysisPanel(QWidget):
    def __init__(self):
        super().__init__()
        self.analyzer = TextAnalyzer()
        self.ai = AIIntegration()
        
        # 创建布局
        self.layout = QVBoxLayout(self)
        
        # 创建输入区域
        self.input_layout = QHBoxLayout()
        self.input_text = QTextEdit()
        self.input_text.setPlaceholderText("请输入要分析的文本...")
        self.analyze_button = QPushButton("分析")
        
        self.input_layout.addWidget(self.input_text)
        self.input_layout.addWidget(self.analyze_button)
        
        # 创建结果显示区域
        self.splitter = QSplitter(Qt.Vertical)
        
        # 分析结果
        self.analysis_result = QTextEdit()
        self.analysis_result.setReadOnly(True)
        self.analysis_result.setPlaceholderText("分析结果将显示在这里...")
        
        # 术语和问题列表
        self.list_widget = QListWidget()
        
        # 详细信息
        self.detail_text = QTextEdit()
        self.detail_text.setReadOnly(True)
        self.detail_text.setPlaceholderText("详细信息将显示在这里...")
        
        self.splitter.addWidget(self.analysis_result)
        self.splitter.addWidget(self.list_widget)
        self.splitter.addWidget(self.detail_text)
        self.splitter.setSizes([200, 150, 150])
        
        # 添加到布局
        self.layout.addLayout(self.input_layout)
        self.layout.addWidget(self.splitter)
        
        # 连接信号
        self.analyze_button.clicked.connect(self.analyze_text)
        self.list_widget.itemClicked.connect(self.show_detail)
    
    def analyze_text(self):
        """分析文本"""
        text = self.input_text.toPlainText().strip()
        if not text:
            return
        
        try:
            # 分析文本
            results = self.analyzer.analyze_text(text)
            
            # 显示分析结果
            self.analysis_result.clear()
            self.analysis_result.append("=== 分析结果 ===")
            self.analysis_result.append(f"识别到 {len(results['terms'])} 个术语")
            self.analysis_result.append(f"识别到 {len(results['questions'])} 个问题")
            self.analysis_result.append("")
            
            # 显示术语和问题列表
            self.list_widget.clear()
            
            # 添加术语
            for term in results['terms']:
                item = QListWidgetItem(f"术语: {term}")
                item.setData(Qt.UserRole, {'type': 'term', 'content': term})
                self.list_widget.addItem(item)
            
            # 添加问题
            for question in results['questions']:
                item = QListWidgetItem(f"问题: {question}")
                item.setData(Qt.UserRole, {'type': 'question', 'content': question})
                self.list_widget.addItem(item)
            
            logger.info("分析文本成功，识别到 %d 个术语和 %d 个问题" % (len(results['terms']), len(results['questions'])))
        except Exception as e:
            logger.error("分析文本失败: %s" % str(e))
            self.analysis_result.append("错误: 分析文本失败 - %s" % str(e))
    
    def show_detail(self, item):
        """显示详细信息"""
        data = item.data(Qt.UserRole)
        if not data:
            return
        
        try:
            self.detail_text.clear()
            
            if data['type'] == 'term':
                # 显示术语解释
                term = data['content']
                self.detail_text.append("=== 术语: %s ===" % term)
                explanation = self.analyzer.get_term_explanation(term)
                self.detail_text.append("解释: %s" % explanation)
            elif data['type'] == 'question':
                # 显示问题答案
                question = data['content']
                self.detail_text.append("=== 问题: %s ===" % question)
                answer = self.analyzer.answer_question(question)
                self.detail_text.append("答案: %s" % answer)
            
            self.detail_text.moveCursor(QTextCursor.End)
        except Exception as e:
            logger.error("获取详细信息失败: %s" % str(e))
            self.detail_text.append("错误: 获取详细信息失败 - %s" % str(e))

if __name__ == "__main__":
    import sys
    from PyQt5.QtWidgets import QApplication
    app = QApplication(sys.argv)
    panel = AnalysisPanel()
    panel.show()
    sys.exit(app.exec_())