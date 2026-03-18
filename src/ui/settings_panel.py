#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QLineEdit, QComboBox, QSpinBox, QGroupBox, QFormLayout
from PyQt5.QtCore import Qt
from src.utils.config import config
from src.utils.logger import get_logger
import os
import pyaudio

logger = get_logger(__name__)

class SettingsPanel(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout(self)
        
        # 创建API设置组
        self.api_group = QGroupBox("API设置")
        self.api_layout = QFormLayout()
        
        self.qwen_api_key_label = QLabel("千问API密钥:")
        self.qwen_api_key_input = QLineEdit()
        self.qwen_api_key_input.setEchoMode(QLineEdit.Password)
        
        self.search_api_key_label = QLabel("搜索API密钥:")
        self.search_api_key_input = QLineEdit()
        self.search_api_key_input.setEchoMode(QLineEdit.Password)
        
        self.api_layout.addRow(self.qwen_api_key_label, self.qwen_api_key_input)
        self.api_layout.addRow(self.search_api_key_label, self.search_api_key_input)
        self.api_group.setLayout(self.api_layout)
        
        # 创建音频设置组
        self.audio_group = QGroupBox("音频设置")
        self.audio_layout = QFormLayout()
        
        self.audio_device_label = QLabel("音频设备:")
        self.audio_device_combo = QComboBox()
        self._populate_audio_devices()
        
        self.sample_rate_label = QLabel("采样率:")
        self.sample_rate_spin = QSpinBox()
        self.sample_rate_spin.setRange(8000, 48000)
        self.sample_rate_spin.setValue(config.AUDIO_SAMPLE_RATE)
        
        self.channels_label = QLabel("声道数:")
        self.channels_spin = QSpinBox()
        self.channels_spin.setRange(1, 2)
        self.channels_spin.setValue(config.AUDIO_CHANNELS)
        
        self.chunk_size_label = QLabel("缓冲区大小:")
        self.chunk_size_spin = QSpinBox()
        self.chunk_size_spin.setRange(256, 4096)
        self.chunk_size_spin.setValue(config.AUDIO_CHUNK_SIZE)
        
        self.audio_layout.addRow(self.audio_device_label, self.audio_device_combo)
        self.audio_layout.addRow(self.sample_rate_label, self.sample_rate_spin)
        self.audio_layout.addRow(self.channels_label, self.channels_spin)
        self.audio_layout.addRow(self.chunk_size_label, self.chunk_size_spin)
        self.audio_group.setLayout(self.audio_layout)
        
        # 创建识别设置组
        self.recognition_group = QGroupBox("识别设置")
        self.recognition_layout = QFormLayout()
        
        self.timeout_label = QLabel("超时时间(秒):")
        self.timeout_spin = QSpinBox()
        self.timeout_spin.setRange(1, 30)
        self.timeout_spin.setSingleStep(0.5)
        self.timeout_spin.setValue(config.RECOGNITION_TIMEOUT)
        
        self.interval_label = QLabel("识别间隔(秒):")
        self.interval_spin = QSpinBox()
        self.interval_spin.setRange(0.1, 5)
        self.interval_spin.setSingleStep(0.1)
        self.interval_spin.setValue(config.RECOGNITION_INTERVAL)
        
        self.recognition_layout.addRow(self.timeout_label, self.timeout_spin)
        self.recognition_layout.addRow(self.interval_label, self.interval_spin)
        self.recognition_group.setLayout(self.recognition_layout)
        
        # 创建按钮
        self.button_layout = QHBoxLayout()
        self.save_button = QPushButton("保存设置")
        self.reset_button = QPushButton("重置")
        
        self.button_layout.addWidget(self.save_button)
        self.button_layout.addWidget(self.reset_button)
        
        # 添加到布局
        self.layout.addWidget(self.api_group)
        self.layout.addWidget(self.audio_group)
        self.layout.addWidget(self.recognition_group)
        self.layout.addLayout(self.button_layout)
        
        # 连接信号
        self.save_button.clicked.connect(self.save_settings)
        self.reset_button.clicked.connect(self.reset_settings)
        
        # 加载当前设置
        self.load_settings()
    
    def _populate_audio_devices(self):
        """填充音频设备列表"""
        try:
            pa = pyaudio.PyAudio()
            for i in range(pa.get_device_count()):
                device_info = pa.get_device_info_by_index(i)
                if device_info['maxInputChannels'] > 0:
                    self.audio_device_combo.addItem("%s (Index: %d)" % (device_info['name'], i))
            pa.terminate()
        except Exception as e:
            logger.error("获取音频设备失败: %s" % str(e))
    
    def load_settings(self):
        """加载设置"""
        # 加载API密钥（实际应用中应该从安全的地方加载）
        # 这里只是示例，实际应用中应该使用环境变量或加密存储
        pass
    
    def save_settings(self):
        """保存设置"""
        try:
            # 保存API密钥（实际应用中应该保存到安全的地方）
            qwen_api_key = self.qwen_api_key_input.text()
            search_api_key = self.search_api_key_input.text()
            
            # 更新配置
            config.AUDIO_SAMPLE_RATE = self.sample_rate_spin.value()
            config.AUDIO_CHANNELS = self.channels_spin.value()
            config.AUDIO_CHUNK_SIZE = self.chunk_size_spin.value()
            config.RECOGNITION_TIMEOUT = self.timeout_spin.value()
            config.RECOGNITION_INTERVAL = self.interval_spin.value()
            
            # 实际应用中应该将设置保存到文件或数据库
            logger.info("保存设置成功")
        except Exception as e:
            logger.error("保存设置失败: %s" % str(e))
    
    def reset_settings(self):
        """重置设置"""
        # 重置输入框
        self.qwen_api_key_input.clear()
        self.search_api_key_input.clear()
        
        # 重置音频设置
        self.sample_rate_spin.setValue(16000)
        self.channels_spin.setValue(1)
        self.chunk_size_spin.setValue(1024)
        
        # 重置识别设置
        self.timeout_spin.setValue(5)
        self.interval_spin.setValue(0.5)
        
        logger.info("重置设置成功")

if __name__ == "__main__":
    import sys
    from PyQt5.QtWidgets import QApplication
    app = QApplication(sys.argv)
    panel = SettingsPanel()
    panel.show()
    sys.exit(app.exec_())