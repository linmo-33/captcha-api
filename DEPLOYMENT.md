# 部署指南

## 快速发布

```bash
# 创建版本标签
git tag -a v1.0.0 -m "Release v1.0.0"

# 推送标签（自动触发构建）
git push origin v1.0.0
```

GitHub Actions 会自动构建并推送镜像到 GitHub Container Registry。

## 使用镜像

```bash
# 拉取镜像
docker pull ghcr.io/linmo-33/captcha-api:latest

# 运行
docker run -d -p 7777:7777 ghcr.io/linmo-33/captcha-api:latest
```



## 生产部署

### Docker Compose

```yaml
version: '3.8'

services:
  captcha-api:
    image: ghcr.io/linmo-33/captcha-api:latest
    container_name: captcha-api
    ports:
      - "7777:7777"
    environment:
      - DEBUG=False
      - LOG_LEVEL=WARNING
      - MAX_BATCH_SIZE=20
    restart: always
    logging:
      driver: "json-file"
      options:
        max-size: "10m"
        max-file: "3"
```
