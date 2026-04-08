#!/usr/bin/env python3
import sys
import os

# 添加项目根目录到 Python 路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# 导入并运行主模块
from src.main import main

if __name__ == "__main__":
    main()