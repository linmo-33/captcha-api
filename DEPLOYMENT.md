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
    ports:
      - "7777:7777"
    environment:
      - DEBUG=False
      - LOG_LEVEL=WARNING
    restart: always
```

### Kubernetes

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: captcha-api
spec:
  replicas: 3
  template:
    spec:
      containers:
      - name: captcha-api
        image: ghcr.io/linmo-33/captcha-api:latest
        ports:
        - containerPort: 7777
---
apiVersion: v1
kind: Service
metadata:
  name: captcha-api
spec:
  type: LoadBalancer
  ports:
  - port: 80
    targetPort: 7777
```

## 监控

- Actions: https://github.com/linmo-33/captcha-api/actions
- Packages: https://github.com/linmo-33/captcha-api/pkgs/container/captcha-api
