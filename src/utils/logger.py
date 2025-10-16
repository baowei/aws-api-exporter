import logging
import sys

def setup_logger(name='aws-api-exporter', level=logging.INFO):
    """
    设置日志记录器
    
    Args:
        name: 日志记录器名称
        level: 日志级别
    
    Returns:
        配置好的日志记录器
    """
    logger = logging.getLogger(name)
    logger.setLevel(level)
    
    # 创建控制台处理器
    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(level)
    
    # 创建格式化器
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    
    # 添加处理器到日志记录器
    logger.addHandler(handler)
    
    return logger