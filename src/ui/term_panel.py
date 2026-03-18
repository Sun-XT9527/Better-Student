#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QTextEdit, QLabel, QListWidget, QListWidgetItem, QSplitter, QCheckBox
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QTextCursor
from src.core.term_manager import TermManager
from src.utils.logger import get_logger

logger = get_logger(__name__)

class TermPanel(QWidget):
    def __init__(self):
        super().__init__()
        self.term_manager = TermManager()
        
        # 创建布局
        self.layout = QVBoxLayout(self)
        
        # 创建控制按钮
        self.control_layout = QHBoxLayout()
        self.refresh_button = QPushButton("刷新")
        self.add_term_button = QPushButton("添加术语")
        
        self.control_layout.addWidget(self.refresh_button)
        self.control_layout.addWidget(self.add_term_button)
        
        # 创建术语列表和详情区域
        self.splitter = QSplitter(Qt.Horizontal)
        
        # 术语列表
        self.term_list = QListWidget()
        
        # 术语详情
        self.detail_layout = QVBoxLayout()
        self.detail_widget = QWidget()
        
        self.term_label = QLabel("术语:")
        self.term_text = QTextEdit()
        self.term_text.setReadOnly(True)
        
        self.explanation_label = QLabel("解释:")
        self.explanation_text = QTextEdit()
        self.explanation_text.setReadOnly(True)
        
        self.mastered_checkbox = QCheckBox("已掌握")
        
        self.detail_layout.addWidget(self.term_label)
        self.detail_layout.addWidget(self.term_text)
        self.detail_layout.addWidget(self.explanation_label)
        self.detail_layout.addWidget(self.explanation_text)
        self.detail_layout.addWidget(self.mastered_checkbox)
        
        self.detail_widget.setLayout(self.detail_layout)
        
        self.splitter.addWidget(self.term_list)
        self.splitter.addWidget(self.detail_widget)
        self.splitter.setSizes([200, 400])
        
        # 添加到布局
        self.layout.addLayout(self.control_layout)
        self.layout.addWidget(self.splitter)
        
        # 连接信号
        self.refresh_button.clicked.connect(self.refresh_terms)
        self.add_term_button.clicked.connect(self.add_term)
        self.term_list.itemClicked.connect(self.show_term_detail)
        self.mastered_checkbox.stateChanged.connect(self.update_mastery)
        
        # 初始加载术语
        self.refresh_terms()
    
    def refresh_terms(self):
        """刷新术语列表"""
        try:
            terms = self.term_manager.get_all_terms()
            self.term_list.clear()
            
            for term in terms:
                item = QListWidgetItem(term['term'])
                item.setData(Qt.UserRole, term)
                # 根据掌握状态设置不同的颜色
                if term['is_mastered']:
                    item.setForeground(Qt.green)
                else:
                    item.setForeground(Qt.black)
                self.term_list.addItem(item)
            
            logger.info("刷新术语列表成功，共 %d 个术语" % len(terms))
        except Exception as e:
            logger.error("刷新术语列表失败: %s" % str(e))
    
    def show_term_detail(self, item):
        """显示术语详情"""
        term = item.data(Qt.UserRole)
        if not term:
            return
        
        self.term_text.setText(term['term'])
        self.explanation_text.setText(term['explanation'])
        self.mastered_checkbox.setChecked(term['is_mastered'])
        
        # 保存当前术语ID，用于更新掌握状态
        self.current_term_id = term['id']
    
    def update_mastery(self, state):
        """更新术语掌握状态"""
        if hasattr(self, 'current_term_id'):
            try:
                is_mastered = 1 if state == Qt.Checked else 0
                self.term_manager.update_term_mastery(self.current_term_id, is_mastered)
                logger.info("更新术语掌握状态成功: ID %d, 掌握状态: %d" % (self.current_term_id, is_mastered))
                # 刷新列表
                self.refresh_terms()
            except Exception as e:
                logger.error("更新术语掌握状态失败: %s" % str(e))
    
    def add_term(self):
        """添加术语"""
        from PyQt5.QtWidgets import QDialog, QLineEdit, QTextEdit, QPushButton, QVBoxLayout, QHBoxLayout
        
        dialog = QDialog(self)
        dialog.setWindowTitle("添加术语")
        
        layout = QVBoxLayout(dialog)
        
        term_label = QLabel("术语:")
        term_input = QLineEdit()
        
        explanation_label = QLabel("解释:")
        explanation_input = QTextEdit()
        
        button_layout = QHBoxLayout()
        ok_button = QPushButton("确定")
        cancel_button = QPushButton("取消")
        
        button_layout.addWidget(ok_button)
        button_layout.addWidget(cancel_button)
        
        layout.addWidget(term_label)
        layout.addWidget(term_input)
        layout.addWidget(explanation_label)
        layout.addWidget(explanation_input)
        layout.addLayout(button_layout)
        
        def on_ok():
            term = term_input.text().strip()
            explanation = explanation_input.toPlainText().strip()
            if term:
                try:
                    self.term_manager.add_term(term, explanation)
                    logger.info("添加术语成功: %s" % term)
                    self.refresh_terms()
                    dialog.accept()
                except Exception as e:
                    logger.error("添加术语失败: %s" % str(e))
            else:
                pass
        
        ok_button.clicked.connect(on_ok)
        cancel_button.clicked.connect(dialog.reject)
        
        dialog.exec_()

if __name__ == "__main__":
    import sys
    from PyQt5.QtWidgets import QApplication
    app = QApplication(sys.argv)
    panel = TermPanel()
    panel.show()
    sys.exit(app.exec_())