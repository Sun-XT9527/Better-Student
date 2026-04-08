#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pyaudio
import wave
import base64
import threading
import time
import sounddevice as sd
import numpy as np
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
        self.audio_source = 'microphone'  # 默认为麦克风
        self.sd_stream = None
    
    def start_recording(self, callback=None, audio_source='microphone'):
        """开始录音
        
        Args:
            callback: 识别结果回调函数
            audio_source: 音频来源，可选值: 'microphone' (麦克风), 'system' (系统音频)
        """
        try:
            self.callback = callback
            self.audio_source = audio_source
            self.is_recording = True
            self.audio_data = []
            
            # 启动录音线程
            self.thread = threading.Thread(target=self._record)
            self.thread.daemon = True
            self.thread.start()
            
            logger.info(f"开始录音，音频来源: {audio_source}")
        except Exception as e:
            logger.error(f"启动录音失败: {str(e)}")
            raise SpeechRecognitionError(f"启动录音失败: {str(e)}")
    
    def stop_recording(self):
        """停止录音"""
        try:
            self.is_recording = False
            if self.thread:
                self.thread.join()
            
            # 关闭麦克风音频流
            if self.stream:
                self.stream.stop_stream()
                self.stream.close()
                self.stream = None
            
            # 关闭系统音频流
            if self.sd_stream:
                self.sd_stream.stop()
                self.sd_stream.close()
                self.sd_stream = None
            
            logger.info(f"停止录音，音频来源: {self.audio_source}")
        except Exception as e:
            logger.error(f"停止录音失败: {str(e)}")
            raise SpeechRecognitionError(f"停止录音失败: {str(e)}")
    
    def _record(self):
        """录音线程函数"""
        if self.audio_source == 'microphone':
            self._record_from_microphone()
        elif self.audio_source == 'system':
            self._record_from_system()
        else:
            logger.error(f"不支持的音频来源: {self.audio_source}")
            self.is_recording = False
    
    def _record_from_microphone(self):
        """从麦克风采集音频"""
        try:
            # 打开麦克风音频流
            self.stream = self.pa.open(
                format=pyaudio.paInt16,
                channels=config.AUDIO_CHANNELS,
                rate=config.AUDIO_SAMPLE_RATE,
                input=True,
                frames_per_buffer=config.AUDIO_CHUNK_SIZE
            )
            
            while self.is_recording:
                data = self.stream.read(config.AUDIO_CHUNK_SIZE)
                self.audio_data.append(data)
                
                # 每间隔一段时间进行一次语音识别
                if len(self.audio_data) * config.AUDIO_CHUNK_SIZE >= config.AUDIO_SAMPLE_RATE * config.RECOGNITION_INTERVAL:
                    self._recognize()
        except Exception as e:
            logger.error(f"从麦克风采集音频失败: {str(e)}")
            self.is_recording = False
    
    def _record_from_system(self):
        """从系统音频输出采集音频"""
        try:
            def callback(indata, frames, time, status):
                if status:
                    logger.warning(f"音频采集状态: {status}")
                # 将numpy数组转换为bytes
                data = indata.astype(np.int16).tobytes()
                self.audio_data.append(data)
                
                # 每间隔一段时间进行一次语音识别
                if len(self.audio_data) * config.AUDIO_CHUNK_SIZE >= config.AUDIO_SAMPLE_RATE * config.RECOGNITION_INTERVAL:
                    self._recognize()
            
            # 打开系统音频流
            self.sd_stream = sd.InputStream(
                samplerate=config.AUDIO_SAMPLE_RATE,
                channels=config.AUDIO_CHANNELS,
                dtype=np.int16,
                callback=callback
            )
            
            self.sd_stream.start()
            
            # 保持线程运行
            while self.is_recording:
                time.sleep(0.1)
        except Exception as e:
            logger.error(f"从系统音频采集失败: {str(e)}")
            self.is_recording = False
    
    def _recognize(self):
        """执行语音识别"""
        try:
            # 构建完整的音频数据
            audio_data = b''.join(self.audio_data)
            
            # 直接传递原始字节数据给API
            text = qwen_api.recognize_speech(audio_data)
            
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
            
            # 直接传递原始字节数据给API
            text = qwen_api.recognize_speech(audio_data)
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