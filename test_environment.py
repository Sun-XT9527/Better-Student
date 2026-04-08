#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试环境配置脚本
用于验证Better-Student项目的环境配置和依赖安装情况
"""

import os
import sys
import importlib
from pathlib import Path

# 项目根目录
PROJECT_ROOT = Path(__file__).parent

# 测试依赖包
required_packages = [
    'pyaudio',
    'requests',
    'PyQt5',
    'nltk',
    'beautifulsoup4',
    'python-dotenv'  
]

# 测试环境变量
required_env_vars = [
    'QWEN_API_KEY',
    'QWEN_VOICE_MODEL',
    'QWEN_CHAT_MODEL'
]

def test_python_version():
    """测试Python版本"""
    print("=== 测试Python版本 ===")
    version = sys.version_info
    print(f"当前Python版本: {version.major}.{version.minor}.{version.micro}")
    if version.major >= 3 and version.minor >= 8:
        print("[OK] Python版本满足要求 (>=3.8)")
        return True
    else:
        print("[ERROR] Python版本不满足要求，需要3.8或更高版本")
        return False

def test_dependencies():
    """测试依赖包安装情况"""
    print("\n=== 测试依赖包 ===")
    installed = []
    missing = []
    
    for package in required_packages:
        try:
            importlib.import_module(package)
            installed.append(package)
            print(f"[OK] {package} 已安装")
        except ImportError:
            missing.append(package)
            print(f"[ERROR] {package} 未安装")
    
    if missing:
        print(f"\n[ERROR] 缺少以下依赖包: {', '.join(missing)}")
        print("请运行: pip install -r requirements.txt")
        return False
    else:
        print("\n[OK] 所有依赖包已安装")
        return True

def test_environment_variables():
    """测试环境变量配置"""
    print("\n=== 测试环境变量 ===")
    
    # 检查.env文件是否存在
    env_file = PROJECT_ROOT / '.env'
    if not env_file.exists():
        print("[ERROR] .env文件不存在")
        print("请从.env.example复制并配置.env文件")
        return False
    
    # 检查python-dotenv是否已安装
    try:
        from dotenv import load_dotenv
        load_dotenv(env_file)
    except ImportError:
        print("[ERROR] python-dotenv未安装，无法加载环境变量")
        print("请运行: pip install python-dotenv")
        return False
    
    configured = []
    missing = []
    
    for var in required_env_vars:
        value = os.getenv(var)
        if value and value != 'your_qwen_api_key' and value != 'your_search_api_key':
            configured.append(var)
            print(f"[OK] {var} 已配置")
        else:
            missing.append(var)
            print(f"[ERROR] {var} 未配置或使用默认值")
    
    if missing:
        print(f"\n[ERROR] 以下环境变量未正确配置: {', '.join(missing)}")
        print("请编辑.env文件并设置正确的值")
        return False
    else:
        print("\n[OK] 所有环境变量已正确配置")
        return True

def test_project_structure():
    """测试项目结构"""
    print("\n=== 测试项目结构 ===")
    
    required_dirs = [
        'src',
        'src/api',
        'src/core',
        'src/ui',
        'src/utils'
    ]
    
    required_files = [
        'src/main.py',
        'src/api/qwen_api.py',
        'src/api/search_api.py',
        'src/core/speech_recognition.py',
        'src/core/text_analyzer.py',
        'src/core/data_storage.py',
        'src/core/ai_integration.py',
        'src/core/term_manager.py',
        'src/ui/main_window.py',
        'src/ui/speech_panel.py',
        'src/ui/analysis_panel.py',
        'src/ui/term_panel.py',
        'src/ui/settings_panel.py',
        'src/utils/config.py',
        'src/utils/logger.py',
        'src/utils/error_handling.py',
        'requirements.txt',
        'setup.py',
        '.env.example'
    ]
    
    structure_ok = True
    
    for directory in required_dirs:
        dir_path = PROJECT_ROOT / directory
        if dir_path.exists() and dir_path.is_dir():
            print(f"[OK] 目录 {directory} 存在")
        else:
            print(f"[ERROR] 目录 {directory} 不存在")
            structure_ok = False
    
    for file in required_files:
        file_path = PROJECT_ROOT / file
        if file_path.exists() and file_path.is_file():
            print(f"[OK] 文件 {file} 存在")
        else:
            print(f"[ERROR] 文件 {file} 不存在")
            structure_ok = False
    
    if structure_ok:
        print("\n[OK] 项目结构完整")
    else:
        print("\n[ERROR] 项目结构不完整")
    
    return structure_ok



def main():
    """主测试函数"""
    print("开始测试Better-Student项目环境...\n")
    
    tests = [
        test_python_version,
        test_dependencies,
        test_project_structure,
        test_environment_variables
    ]
    
    results = []
    for test in tests:
        results.append(test())
    
    print("\n" + "="*60)
    print("测试结果汇总:")
    print("="*60)
    
    passed = sum(results)
    total = len(results)
    
    print(f"通过测试: {passed}/{total}")
    
    if all(results):
        print("\n[SUCCESS] 所有测试通过! 项目环境配置正确。")
        return 0
    else:
        print("\n[WARNING] 部分测试未通过，请根据提示进行修复。")
        return 1

if __name__ == "__main__":
    sys.exit(main())
