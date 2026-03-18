#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
from PyQt5.QtWidgets import QApplication
from src.ui.main_window import MainWindow
from src.utils.logger import get_logger

logger = get_logger(__name__)

def main():
    """主函数"""
    try:
        logger.info("启动Better-Student应用")
        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        sys.exit(app.exec_())
    except Exception as e:
        logger.error("应用启动失败: %s" % str(e))
        print("应用启动失败: %s" % str(e))
        sys.exit(1)

if __name__ == "__main__":
    main()