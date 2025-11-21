#!/bin/bash

# 启动脚本

echo "正在启动 CAPTCHA 识别 API 服务..."

# 检查是否安装了 Docker
if ! command -v docker &> /dev/null; then
    echo "错误: 未安装 Docker"
    echo "请访问 https://docs.docker.com/get-docker/ 安装 Docker"
    exit 1
fi

# 检查是否安装了 Docker Compose
if ! command -v docker-compose &> /dev/null; then
    echo "警告: 未安装 Docker Compose，使用 docker build 和 docker run"
    
    # 构建镜像
    echo "构建 Docker 镜像..."
    docker build -t captcha-api .
    
    # 停止并删除旧容器
    docker stop captcha-api 2>/dev/null || true
    docker rm captcha-api 2>/dev/null || true
    
    # 运行容器
    echo "启动容器..."
    docker run -d \
        --name captcha-api \
        -p 7777:7777 \
        -e DEBUG=False \
        -e LOG_LEVEL=INFO \
        --restart unless-stopped \
        captcha-api
else
    # 使用 Docker Compose
    echo "使用 Docker Compose 启动服务..."
    docker-compose up -d --build
fi

echo ""
echo "✅ 服务启动成功！"
echo ""
echo "访问地址："
echo "  - API 首页: http://localhost:7777/"
echo "  - API 文档: http://localhost:7777/docs"
echo "  - 健康检查: http://localhost:7777/health"
echo ""
echo "查看日志: docker logs -f captcha-api"
echo "停止服务: docker stop captcha-api"
echo ""
