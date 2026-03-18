#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QVBoxLayout, QHBoxLayout, QTabWidget, QMenuBar, QMenu, QAction, QStatusBar
from PyQt5.QtCore import Qt
from src.ui.speech_panel import SpeechPanel
from src.ui.analysis_panel import AnalysisPanel
from src.ui.term_panel import TermPanel
from src.ui.settings_panel import SettingsPanel
from src.utils.config import config

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle(f"{config.APP_NAME} v{config.APP_VERSION}")
        self.setGeometry(100, 100, 1000, 700)
        
        # 创建中心部件
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        
        # 创建主布局
        self.main_layout = QVBoxLayout(self.central_widget)
        
        # 创建标签页
        self.tab_widget = QTabWidget()
        self.main_layout.addWidget(self.tab_widget)
        
        # 创建各个面板
        self.speech_panel = SpeechPanel()
        self.analysis_panel = AnalysisPanel()
        self.term_panel = TermPanel()
        self.settings_panel = SettingsPanel()
        
        # 添加标签页
        self.tab_widget.addTab(self.speech_panel, "语音识别")
        self.tab_widget.addTab(self.analysis_panel, "文本分析")
        self.tab_widget.addTab(self.term_panel, "术语管理")
        self.tab_widget.addTab(self.settings_panel, "设置")
        
        # 创建菜单栏
        self.create_menu_bar()
        
        # 创建状态栏
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage("就绪")
    
    def create_menu_bar(self):
        """创建菜单栏"""
        menu_bar = QMenuBar(self)
        self.setMenuBar(menu_bar)
        
        # 文件菜单
        file_menu = QMenu("文件", self)
        menu_bar.addMenu(file_menu)
        
        exit_action = QAction("退出", self)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)
        
        # 帮助菜单
        help_menu = QMenu("帮助", self)
        menu_bar.addMenu(help_menu)
        
        about_action = QAction("关于", self)
        about_action.triggered.connect(self.show_about)
        help_menu.addAction(about_action)
    
    def show_about(self):
        """显示关于对话框"""
        from PyQt5.QtWidgets import QMessageBox
        QMessageBox.about(self, "关于", "%s v%s\n\n一个基于Python的语音转文字与智能分析软件，帮助学生更高效地学习和理解课程内容。" % (config.APP_NAME, config.APP_VERSION))
    
    def closeEvent(self, event):
        """关闭事件"""
        # 停止录音
        self.speech_panel.stop_recording()
        event.accept()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())