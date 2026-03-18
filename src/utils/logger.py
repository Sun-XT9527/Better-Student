import os
import logging
from src.utils.config import config

# 确保日志目录存在
log_dir = os.path.dirname(config.LOG_FILE)
if log_dir and not os.path.exists(log_dir):
    os.makedirs(log_dir)

# 配置日志
logging.basicConfig(
    level=getattr(logging, config.LOG_LEVEL),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(config.LOG_FILE),
        logging.StreamHandler()
    ]
)

# 创建日志记录器
def get_logger(name):
    return logging.getLogger(name)

# 示例用法
# logger = get_logger(__name__)
# logger.info('This is an info message')
# logger.error('This is an error message')