# CAPTCHA 识别 API

基于 ddddocr 的验证码识别服务，支持多种验证码类型识别。

## 功能特性

### 核心功能
- 🔐 滑块验证码识别
- 📝 OCR文字识别（支持批量）
- 🎯 目标检测
- 🧮 计算类验证码
- ✂️ 图片分割
- 👆 点选验证码


## 项目结构

```
.
├── app/
│   ├── __init__.py          # 应用工厂
│   ├── config.py            # 配置文件
│   ├── routes/              # 路由模块
│   │   ├── __init__.py
│   │   ├── captcha_routes.py   # 验证码识别路由
│   │   └── system_routes.py    # 系统路由
│   ├── services/            # 业务逻辑
│   │   ├── __init__.py
│   │   └── captcha_service.py  # 验证码服务
│   └── utils/               # 工具函数
│       ├── __init__.py
│       ├── image_processor.py  # 图片处理
│       ├── logger.py           # 日志配置
│       └── stats.py            # 统计功能
├── run.py                   # 应用入口
├── requirements.txt         # 依赖包
├── Dockerfile              # Docker配置
└── README.md               # 项目文档
```

## 快速开始

### 使用 Docker（推荐）

**从 GitHub Container Registry 拉取：**
```bash
docker pull ghcr.io/linmo-33/captcha-api:latest
docker run -d -p 7777:7777 --name captcha-api ghcr.io/linmo-33/captcha-api:latest
```


### 本地运行

1. 安装依赖：
```bash
pip install -r requirements.txt
```

2. 运行服务：
```bash
python run.py
```

3. 访问服务：
```
API首页: http://localhost:7777/
API文档: http://localhost:7777/docs
健康检查: http://localhost:7777/health
统计信息: http://localhost:7777/stats
```

### Docker 运行

**方式一：使用启动脚本（推荐）**

Windows:
```bash
start.bat
```

Linux/Mac:
```bash
chmod +x start.sh
./start.sh
```

**方式二：使用 Docker Compose**
```bash
docker-compose up -d --build
```

**方式三：手动 Docker 命令**
```bash
# 构建镜像
docker build -t captcha-api .

# 运行容器
docker run -d \
  --name captcha-api \
  -p 7777:7777 \
  -e DEBUG=False \
  -e LOG_LEVEL=INFO \
  --restart unless-stopped \
  captcha-api

# 查看日志
docker logs -f captcha-api

# 停止服务
docker stop captcha-api
```

## API 端点

### 系统端点
- `GET /` - API首页
- `GET /health` - 健康检查
- `GET /stats` - 统计信息
- `GET /docs` - API文档

### 识别端点
- `POST /classification` - OCR文字识别
- `POST /batch/classification` - 批量OCR识别
- `POST /capcode` - 滑块验证码识别
- `POST /slideComparison` - 滑块对比
- `POST /detection` - 目标检测
- `POST /calculate` - 计算类验证码
- `POST /crop` - 图片分割
- `POST /select` - 点选验证码

## 使用方式

### API调用

#### OCR识别
```bash
curl -X POST http://localhost:7777/classification \
  -H "Content-Type: application/json" \
  -d '{
    "image": "base64_string_or_url",
    "preprocess": true
  }'
```

#### 滑块识别
```bash
curl -X POST http://localhost:7777/capcode \
  -H "Content-Type: application/json" \
  -d '{
    "slidingImage": "base64_or_url",
    "backImage": "base64_or_url",
    "simpleTarget": true,
    "preprocess": false
  }'
```

#### 批量识别
```bash
curl -X POST http://localhost:7777/batch/classification \
  -H "Content-Type: application/json" \
  -d '{
    "images": ["image1", "image2"],
    "preprocess": false
  }'
```

## 配置说明

在 `app/config.py` 中可以修改：
- 日志级别和格式
- API速率限制
- 批量处理最大数量
- 服务器端口和主机

## 技术栈

- Flask - Web框架
- ddddocr - 验证码识别
- OpenCV - 图像处理
- Pillow - 图像增强
- Flask-Limiter - 速率限制
- Flasgger - API文档

## 环境变量配置

复制 `.env.example` 为 `.env` 并根据需要修改：

```bash
cp .env.example .env
```

可配置项：
- `HOST` - 服务监听地址（默认: ::）
- `PORT` - 服务端口（默认: 7777）
- `DEBUG` - 调试模式（默认: False）
- `LOG_LEVEL` - 日志级别（默认: INFO，可选: DEBUG/INFO/WARNING/ERROR）
- `MAX_BATCH_SIZE` - 批量处理最大数量（默认: 20）
- `MAX_IMAGE_SIZE` - 图片最大大小（默认: 5MB）
- `REQUEST_TIMEOUT` - 请求超时时间（默认: 10秒）

**注意**: 日志输出到控制台，不保存到文件。使用 `docker logs` 查看容器日志。

## 常见问题

### 1. 端口被占用
修改 `app/config.py` 中的 `PORT` 配置

### 2. 识别率低
- 在请求中设置 `"preprocess": true` 启用图片预处理
- 确保图片清晰度足够
- 检查图片格式是否支持

### 3. 请求被限制
- 检查速率限制配置
- 等待一段时间后重试
- 考虑部署多个实例

## 发布新版本

创建新的版本标签会自动触发 Docker 镜像构建：

```bash
# 创建标签
git tag -a v1.0.0 -m "Release version 1.0.0"

# 推送标签
git push origin v1.0.0
```

GitHub Actions 会自动构建并推送镜像到：
- GitHub Container Registry: `ghcr.io/linmo-33/captcha-api:v1.0.0`
- Docker Hub: `your-username/captcha-api:v1.0.0`

## CI/CD

标签推送时自动构建 Docker 镜像：
- ✅ 自动构建并推送到 GitHub Container Registry
- ✅ 支持多架构（amd64, arm64）
- ✅ 自动生成版本标签（latest, v1.0.0, v1.0, v1）

## Docker 管理命令

```bash
# 查看容器状态
docker ps

# 实时查看日志（推荐）
docker logs -f captcha-api

# 查看最近 100 行日志
docker logs --tail 100 captcha-api

# 查看带时间戳的日志
docker logs -f --timestamps captcha-api

# 进入容器
docker exec -it captcha-api bash

# 重启服务
docker restart captcha-api

# 停止服务
docker stop captcha-api

# 删除容器
docker rm captcha-api

# 删除镜像
docker rmi captcha-api
```

## 安全说明

- 所有图片大小限制为 5MB
- URL 图片下载有 10 秒超时限制
- 计算类验证码使用安全的 AST 求值，不使用 eval()
- Docker 容器使用非 root 用户运行
- 建议在生产环境中设置 `DEBUG=False`

## 部署指南

详细的部署说明请查看 [DEPLOYMENT.md](DEPLOYMENT.md)

## 贡献指南

欢迎提交 Issue 和 Pull Request！

## 许可证

MIT License
