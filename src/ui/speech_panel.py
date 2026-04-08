#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QTextEdit, QLabel, QProgressBar, QSplitter, QToolTip, QComboBox
from PyQt5.QtCore import Qt, QThread, pyqtSignal, QPoint
from PyQt5.QtGui import QTextCursor, QTextCharFormat, QMouseEvent
from src.core.speech_recognition import SpeechRecognizer
from src.core.data_storage import DataStorage
from src.core.term_manager import TermManager
from src.utils.logger import get_logger

logger = get_logger(__name__)

class SpeechPanel(QWidget):
    def __init__(self):
        super().__init__()
        self.recognizer = SpeechRecognizer()
        self.storage = DataStorage()
        self.term_manager = TermManager()
        self.is_recording = False
        self.transcription_id = None
        
        # 创建布局
        self.layout = QVBoxLayout(self)
        
        # 创建控制按钮
        self.control_layout = QHBoxLayout()
        
        # 音频来源选择
        self.audio_source_label = QLabel("音频来源:")
        self.audio_source_combo = QComboBox()
        self.audio_source_combo.addItem("麦克风", "microphone")
        self.audio_source_combo.addItem("系统音频", "system")
        
        self.start_button = QPushButton("开始录音")
        self.stop_button = QPushButton("停止录音")
        self.stop_button.setEnabled(False)
        
        self.control_layout.addWidget(self.audio_source_label)
        self.control_layout.addWidget(self.audio_source_combo)
        self.control_layout.addWidget(self.start_button)
        self.control_layout.addWidget(self.stop_button)
        
        # 创建进度条
        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setValue(0)
        
        # 创建文本显示区域
        self.splitter = QSplitter(Qt.Vertical)
        
        # 实时转文字结果
        self.transcription_text = QTextEdit()
        self.transcription_text.setReadOnly(True)
        self.transcription_text.setPlaceholderText("语音转文字结果将显示在这里...")
        self.transcription_text.setAcceptRichText(True)
        
        # 分析结果
        self.analysis_text = QTextEdit()
        self.analysis_text.setReadOnly(True)
        self.analysis_text.setPlaceholderText("分析结果将显示在这里...")
        
        self.splitter.addWidget(self.transcription_text)
        self.splitter.addWidget(self.analysis_text)
        self.splitter.setSizes([300, 200])
        
        # 添加到布局
        self.layout.addLayout(self.control_layout)
        self.layout.addWidget(self.progress_bar)
        self.layout.addWidget(self.splitter)
        
        # 连接信号
        self.start_button.clicked.connect(self.start_recording)
        self.stop_button.clicked.connect(self.stop_recording)
        
        # 启用鼠标跟踪
        self.transcription_text.setMouseTracking(True)
        self.transcription_text.mouseMoveEvent = self.on_mouse_move
    
    def start_recording(self):
        """开始录音"""
        try:
            self.is_recording = True
            self.start_button.setEnabled(False)
            self.stop_button.setEnabled(True)
            self.progress_bar.setValue(50)
            self.transcription_text.clear()
            self.analysis_text.clear()
            
            # 获取选择的音频来源
            audio_source = self.audio_source_combo.currentData()
            
            # 开始录音
            self.recognizer.start_recording(callback=self.on_recognize, audio_source=audio_source)
            logger.info(f"开始录音，音频来源: {audio_source}")
        except Exception as e:
            logger.error("开始录音失败: %s" % str(e))
            self.analysis_text.append("错误: 开始录音失败 - %s" % str(e))
    
    def stop_recording(self):
        """停止录音"""
        try:
            self.is_recording = False
            self.start_button.setEnabled(True)
            self.stop_button.setEnabled(False)
            self.progress_bar.setValue(0)
            
            # 停止录音
            self.recognizer.stop_recording()
            logger.info("停止录音")
        except Exception as e:
            logger.error("停止录音失败: %s" % str(e))
            self.analysis_text.append("错误: 停止录音失败 - %s" % str(e))
    
    def on_recognize(self, text):
        """处理识别结果"""
        if text:
            # 保存转文字结果
            if not self.transcription_id:
                self.transcription_id = self.storage.save_transcription(text)
            else:
                # 更新现有记录
                pass
            
            # 处理术语
            try:
                terms = self.term_manager.process_terms_in_text(text, self.transcription_id)
                if terms:
                    # 标记术语并显示
                    marked_text = self._mark_terms(text, terms)
                    self.transcription_text.append(marked_text)
                    self.transcription_text.moveCursor(QTextCursor.End)
                    
                    term_names = [term['term'] for term in terms]
                    self.analysis_text.append("识别到术语: %s" % term_names)
                    self.analysis_text.moveCursor(QTextCursor.End)
                else:
                    # 无术语，直接显示
                    self.transcription_text.append(text)
                    self.transcription_text.moveCursor(QTextCursor.End)
            except Exception as e:
                logger.error("处理术语失败: %s" % str(e))
                self.transcription_text.append(text)
                self.transcription_text.moveCursor(QTextCursor.End)
                self.analysis_text.append("错误: 处理术语失败 - %s" % str(e))
    
    def _mark_terms(self, text, terms):
        """标记文本中的术语"""
        # 按术语长度排序，长术语优先
        sorted_terms = sorted(terms, key=lambda x: len(x['term']), reverse=True)
        
        # 标记术语
        for term_info in sorted_terms:
            term = term_info['term']
            is_mastered = term_info['is_mastered']
            explanation = term_info['explanation']
            
            # 根据掌握状态设置不同的颜色和样式
            if is_mastered:
                # 已掌握：绿色，无下划线
                replacement = f"<span style='color: green;' title='{explanation}'>{term}</span>"
            else:
                # 未掌握：蓝色，有下划线
                replacement = f"<span style='color: blue; text-decoration: underline;' title='{explanation}'>{term}</span>"
            
            # 替换文本中的术语
            text = text.replace(term, replacement)
        
        return text
    
    def on_mouse_move(self, event):
        """处理鼠标移动事件"""
        # 获取鼠标位置
        pos = event.pos()
        
        # 获取鼠标所在位置的文本光标
        cursor = self.transcription_text.cursorForPosition(pos)
        cursor.select(QTextCursor.WordUnderCursor)
        
        # 获取选中的单词
        word = cursor.selectedText()
        if word:
            # 检查是否是术语
            term_info = self.term_manager.get_term(word)
            if term_info:
                # 显示术语解释
                QToolTip.showText(event.globalPos(), term_info['explanation'], self.transcription_text)
            else:
                # 隐藏工具提示
                QToolTip.hideText()

if __name__ == "__main__":
    import sys
    from PyQt5.QtWidgets import QApplication
    app = QApplication(sys.argv)
    panel = SpeechPanel()
    panel.show()
    sys.exit(app.exec_())