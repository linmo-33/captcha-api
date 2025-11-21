@echo off
chcp 65001 >nul
echo 正在启动 CAPTCHA 识别 API 服务...
echo.

REM 检查 Docker 是否安装
docker --version >nul 2>&1
if errorlevel 1 (
    echo 错误: 未安装 Docker
    echo 请访问 https://docs.docker.com/get-docker/ 安装 Docker
    pause
    exit /b 1
)

REM 检查 Docker Compose 是否安装
docker-compose --version >nul 2>&1
if errorlevel 1 (
    echo 警告: 未安装 Docker Compose，使用 docker build 和 docker run
    echo.
    
    REM 构建镜像
    echo 构建 Docker 镜像...
    docker build -t captcha-api .
    
    REM 停止并删除旧容器
    docker stop captcha-api >nul 2>&1
    docker rm captcha-api >nul 2>&1
    
    REM 运行容器
    echo 启动容器...
    docker run -d ^
        --name captcha-api ^
        -p 7777:7777 ^
        -e DEBUG=False ^
        -e LOG_LEVEL=INFO ^
        --restart unless-stopped ^
        captcha-api
) else (
    REM 使用 Docker Compose
    echo 使用 Docker Compose 启动服务...
    docker-compose up -d --build
)

echo.
echo ✅ 服务启动成功！
echo.
echo 访问地址：
echo   - API 首页: http://localhost:7777/
echo   - API 文档: http://localhost:7777/docs
echo   - 健康检查: http://localhost:7777/health
echo.
echo 查看日志: docker logs -f captcha-api
echo 停止服务: docker stop captcha-api
echo.
pause
