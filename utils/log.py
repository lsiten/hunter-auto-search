"""
日志配置模块
"""
import sys
from loguru import logger
from conf import LOG_LEVEL, LOG_FORMAT


def setup_logger():
    """配置 logger"""
    # 移除默认 handler
    logger.remove()
    
    # 添加控制台 handler
    logger.add(
        sys.stdout,
        level=LOG_LEVEL,
        format=LOG_FORMAT,
        colorize=True,
    )
    
    return logger


# 初始化 logger
log = setup_logger()

__all__ = ["log"]
