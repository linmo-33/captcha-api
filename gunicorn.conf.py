"""Gunicorn 配置文件"""
import os

# 服务器配置
bind = f"[::]:{os.getenv('PORT', 7777)}"
workers = int(os.getenv('WORKERS', 1))  # 默认 1 个 worker，节省内存
worker_class = 'gevent'
worker_connections = 1000
timeout = 120
keepalive = 5

# 进程管理
max_requests = 1000  # 每个 worker 处理 1000 个请求后重启，释放内存
max_requests_jitter = 50  # 随机抖动，避免同时重启
preload_app = True  # 预加载应用，共享内存

# 日志配置
accesslog = '-'
errorlog = '-'
loglevel = os.getenv('LOG_LEVEL', 'info').lower()

# 访问日志格式（过滤健康检查）
access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s"'

def on_starting(server):
    """服务启动时"""
    print("🚀 CAPTCHA API 服务启动中...")

def when_ready(server):
    """服务就绪时"""
    print(f"✅ CAPTCHA API 服务已就绪 - http://localhost:{os.getenv('PORT', 7777)}")
    print(f"📊 Workers: {workers} | Connections: {worker_connections}")

def on_exit(server):
    """服务退出时"""
    print("👋 CAPTCHA API 服务已停止")

# 过滤健康检查日志
def filter_health_check(record):
    """过滤 /health 请求的日志"""
    return '/health' not in record.getMessage()

# 应用日志过滤器
import logging
logging.getLogger('gunicorn.access').addFilter(filter_health_check)
