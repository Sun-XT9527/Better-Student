#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pyaudio
import wave
import base64
import threading
import time
from src.api.qwen_api import qwen_api
from src.utils.config import config
from src.utils.logger import get_logger
from src.utils.error_handling import SpeechRecognitionError

logger = get_logger(__name__)

class SpeechRecognizer:
    def __init__(self):
        self.pa = pyaudio.PyAudio()
        self.stream = None
        self.is_recording = False
        self.audio_data = []
        self.thread = None
        self.callback = None
    
    def start_recording(self, callback=None):
        """开始录音"""
        try:
            self.callback = callback
            self.is_recording = True
            self.audio_data = []
            
            # 打开音频流
            self.stream = self.pa.open(
                format=pyaudio.paInt16,
                channels=config.AUDIO_CHANNELS,
                rate=config.AUDIO_SAMPLE_RATE,
                input=True,
                frames_per_buffer=config.AUDIO_CHUNK_SIZE
            )
            
            # 启动录音线程
            self.thread = threading.Thread(target=self._record)
            self.thread.daemon = True
            self.thread.start()
            
            logger.info("开始录音")
        except Exception as e:
            logger.error(f"启动录音失败: {str(e)}")
            raise SpeechRecognitionError(f"启动录音失败: {str(e)}")
    
    def stop_recording(self):
        """停止录音"""
        try:
            self.is_recording = False
            if self.thread:
                self.thread.join()
            if self.stream:
                self.stream.stop_stream()
                self.stream.close()
            logger.info("停止录音")
        except Exception as e:
            logger.error(f"停止录音失败: {str(e)}")
            raise SpeechRecognitionError(f"停止录音失败: {str(e)}")
    
    def _record(self):
        """录音线程函数"""
        while self.is_recording:
            data = self.stream.read(config.AUDIO_CHUNK_SIZE)
            self.audio_data.append(data)
            
            # 每间隔一段时间进行一次语音识别
            if len(self.audio_data) * config.AUDIO_CHUNK_SIZE >= config.AUDIO_SAMPLE_RATE * config.RECOGNITION_INTERVAL:
                self._recognize()
    
    def _recognize(self):
        """执行语音识别"""
        try:
            # 构建完整的音频数据
            audio_data = b''.join(self.audio_data)
            
            # 转换为base64编码
            audio_base64 = base64.b64encode(audio_data).decode('utf-8')
            
            # 调用千问API进行语音识别
            text = qwen_api.recognize_speech(audio_base64)
            
            # 清空音频数据，准备下一次识别
            self.audio_data = []
            
            # 调用回调函数处理识别结果
            if self.callback and text:
                self.callback(text)
                
        except Exception as e:
            logger.error(f"语音识别失败: {str(e)}")
            # 继续录音，不中断
    
    def recognize_file(self, file_path):
        """识别音频文件"""
        try:
            with wave.open(file_path, 'rb') as wf:
                audio_data = wf.readframes(wf.getnframes())
            
            # 转换为base64编码
            audio_base64 = base64.b64encode(audio_data).decode('utf-8')
            
            # 调用千问API进行语音识别
            text = qwen_api.recognize_speech(audio_base64)
            return text
        except Exception as e:
            logger.error(f"识别音频文件失败: {str(e)}")
            raise SpeechRecognitionError(f"识别音频文件失败: {str(e)}")
    
    def __del__(self):
        """清理资源"""
        if self.stream:
            self.stream.stop_stream()
            self.stream.close()
        self.pa.terminate()

# 示例用法
# def on_recognize(text):
#     print(f"识别结果: {text}")
# 
# recognizer = SpeechRecognizer()
# recognizer.start_recording(callback=on_recognize)
# time.sleep(10)  # 录音10秒
# recognizer.stop_recording()