# 使用基础镜像
FROM python:3.9-slim

# 设置环境变量
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    DEBIAN_FRONTEND=noninteractive

# 安装系统依赖和构建工具
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    gcc \
    g++ \
    libglib2.0-0 \
    libsm6 \
    libxrender1 \
    libxext6 \
    libgomp1 \
    libgl1 \
    && apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# 设置工作目录
WORKDIR /app

# 先复制依赖文件（利用 Docker 缓存）
COPY requirements.txt .

# 分步安装依赖，避免内存问题
RUN pip install --no-cache-dir --upgrade pip setuptools wheel && \
    pip install --no-cache-dir numpy>=1.24.0,<2.0.0 && \
    pip install --no-cache-dir opencv-python-headless>=4.8.0 && \
    pip install --no-cache-dir Pillow>=10.0.0 && \
    pip install --no-cache-dir ddddocr>=1.4.0 && \
    pip install --no-cache-dir Flask>=2.3.0 Flask-Limiter>=3.3.0 flasgger>=0.9.7 && \
    pip install --no-cache-dir requests>=2.31.0 urllib3>=1.26.0 && \
    pip install --no-cache-dir gunicorn>=21.2.0 gevent>=23.9.0

# 复制项目文件
COPY . .

# 创建非 root 用户
RUN useradd -m -u 1000 appuser && \
    chown -R appuser:appuser /app

# 切换到非 root 用户
USER appuser

# 暴露端口
EXPOSE 7777

# 健康检查
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD python -c "import requests; requests.get('http://localhost:7777/health', timeout=5)"

# 运行项目
CMD ["gunicorn", "-c", "gunicorn.conf.py", "run:app"]