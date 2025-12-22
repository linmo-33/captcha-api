import os

class Config:
    """应用配置"""
    
    # 日志配置
    LOG_LEVEL = os.environ.get('LOG_LEVEL', 'INFO')
    LOG_FORMAT = '%(asctime)s [%(levelname)s] %(name)s - %(message)s'
    
    # API 认证（可选）
    API_KEYS = os.environ.get('API_KEYS', '')  # 逗号分隔的 API Keys
    
    # API配置
    MAX_BATCH_SIZE = int(os.environ.get('MAX_BATCH_SIZE', 20))
    DEFAULT_RATE_LIMIT = os.environ.get('DEFAULT_RATE_LIMIT', "30 per minute")
    
    # 图片处理配置
    MAX_IMAGE_SIZE = int(os.environ.get('MAX_IMAGE_SIZE', 5 * 1024 * 1024))  # 5MB
    ALLOWED_IMAGE_FORMATS = ['JPEG', 'PNG', 'BMP', 'GIF', 'WEBP']
    
    # 请求超时配置
    REQUEST_TIMEOUT = int(os.environ.get('REQUEST_TIMEOUT', 60))  # 秒
    
    # 服务器配置
    HOST = os.environ.get('HOST', '::')
    PORT = int(os.environ.get('PORT', 7777))
    DEBUG = os.environ.get('DEBUG', 'False').lower() == 'true'
    THREADED = True
