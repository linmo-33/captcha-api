import logging
import sys

def setup_logger(app):
    """配置日志 - 输出到控制台"""
    # 清除默认的处理器
    app.logger.handlers.clear()
    
    # 创建控制台处理器
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(getattr(logging, app.config['LOG_LEVEL']))
    
    # 设置格式
    formatter = logging.Formatter(app.config['LOG_FORMAT'])
    console_handler.setFormatter(formatter)
    
    # 添加处理器到 app.logger
    app.logger.addHandler(console_handler)
    app.logger.setLevel(getattr(logging, app.config['LOG_LEVEL']))
    
    # 防止日志重复
    app.logger.propagate = False
    
    return app.logger
