"""
-*- coding: utf-8 -*-
@Organization : SupaVision
@Author       : 18317
@Date Created : 29/12/2023
@Description  :
"""
import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path

LOG_FILE = Path(__file__).parent / 'scripts.log'

# 日志配置函数
def setup_logging(level=logging.INFO):
    # 创建 Logger
    logger = logging.getLogger()
    logger.setLevel(level)

    # 创建用于写入日志文件的 Handler
    file_handler = RotatingFileHandler(LOG_FILE, maxBytes=1024 * 1024 * 5, backupCount=5)
    file_handler.setLevel(level)
    file_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(file_formatter)

    # 创建用于控制台输出的 Handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(level)
    console_formatter = logging.Formatter('%(name)s - %(levelname)s - %(message)s')
    console_handler.setFormatter(console_formatter)

    # 添加 Handlers 到 Logger
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)



if __name__ == '__main__':
    setup_logging()
    # 测试日志输出
    logging.info("the info log")
    logging.error("the error log")
