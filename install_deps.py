#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import subprocess
import sys

# 依赖列表
deps = [
    'pyaudio==0.2.14',
    'requests==2.31.0',
    'PyQt5==5.15.10',
    'nltk==3.8.1',
    'beautifulsoup4==4.12.2',
    'python-dotenv==1.0.0',
    'sounddevice==0.4.6',
    'dashscope==1.25.15',
    'openai==2.30.0',
    'numpy==1.26.4',
    'pandas==2.2.1'
]

def install_dependencies():
    """安装依赖项"""
    print("开始安装依赖项...")
    for dep in deps:
        print(f"安装: {dep}")
        result = subprocess.run(
            [sys.executable, '-m', 'pip', 'install', dep],
            capture_output=True,
            text=True
        )
        if result.returncode != 0:
            print(f"安装 {dep} 失败: {result.stderr}")
        else:
            print(f"安装 {dep} 成功")
    print("依赖项安装完成!")

if __name__ == "__main__":
    install_dependencies()
