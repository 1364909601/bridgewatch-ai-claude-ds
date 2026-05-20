# BridgeWatch AI 部署指南

> 适用于 Linux 服务器生产环境部署。

---

## 1. 环境要求

| 组件 | 要求 |
|------|------|
| 操作系统 | Ubuntu 22.04+ / CentOS 8+ |
| CPU | 4 核（推荐 8 核用于推理） |
| 内存 | 8 GB（推荐 16 GB） |
| 磁盘 | 50 GB 可用空间 |
| Docker | 24.0+ |
| Docker Compose | 2.20+ |

---

## 2. 快速部署（Docker Compose）

```bash
# 1. 克隆代码
git clone https://github.com/1364909601/bridgewatch-ai-claude-ds.git
cd bridgewatch-ai-claude-ds

# 2. 配置环境变量
cp backend/.env.example backend/.env
# 编辑 backend/.env，修改以下配置：
#   - SECRET_KEY（改为随机字符串）
#   - DATABASE_URL（生产环境使用 PostgreSQL）
#   - CORS_ORIGINS（改为实际域名）
#   - SMTP_*（如需邮件通知）

# 3. 启动所有服务
cd backend
docker-compose up -d

# 4. 验证部署
curl http://localhost/api/health
# 返回 {"code":0,"message":"success",...}

# 5. 查看日志
docker-compose logs -f backend
```

---

## 3. 配置 HTTPS（SSL）

```bash
# 1. 获取 SSL 证书（以 Let's Encrypt 为例）
sudo apt install certbot
sudo certbot certonly --standalone -d your-domain.com

# 2. 创建证书目录
mkdir -p certs
cp /etc/letsencrypt/live/your-domain.com/fullchain.pem certs/
cp /etc/letsencrypt/live/your-domain.com/privkey.pem certs/

# 3. 使用 SSL 版本的 Nginx 配置
cp nginx/nginx-ssl.conf nginx/nginx.conf

# 4. 重启 frontend 容器
docker-compose restart frontend

# 5. 设置证书自动续期
crontab -e
# 添加：0 0 * * * certbot renew --quiet && docker-compose restart frontend
```

---

## 4. 数据库备份

```bash
# 手动备份
./scripts/backup.sh --docker

# 定时备份（添加到 crontab）
0 2 * * * cd /opt/bridgewatch && ./scripts/backup.sh --docker >> /var/log/bridgewatch-backup.log 2>&1
```

---

## 5. 日常运维

```bash
# 查看服务状态
docker-compose ps

# 查看日志
docker-compose logs -f --tail=100 backend

# 重启单个服务
docker-compose restart backend

# 更新到最新版本
git pull origin main
docker-compose up -d --build

# 监控入口
# - Grafana:  http://localhost:3000 (admin/admin)
# - Prometheus: http://localhost:9090
# - Loki:       http://localhost:3100

# 数据入口
# - 前端页面: http://localhost
# - API 文档: http://localhost:8000/docs (Swagger)
```

---

## 6. 系统架构

```
                         ┌──────────┐
                         │  Nginx   │ :80 / :443
                         └────┬─────┘
                              │
              ┌───────────────┼───────────────┐
              ▼               ▼               ▼
        ┌──────────┐    ┌──────────┐    ┌──────────┐
        │ Frontend │    │  Backend │    │  Grafana │ :3000
        │  (SPA)   │    │ :8000    │    └──────────┘
        └──────────┘    └────┬─────┘         │
                             │               ├── Prometheus :9090
              ┌──────────────┼──────┐        └── Loki :3100
              ▼              ▼      ▼
        ┌──────────┐  ┌──────────┐  ┌──────────┐
        │ Postgres │  │  Redis   │  │  MinIO   │ (可选)
        │ :5432    │  │ :6379    │  │          │
        └──────────┘  └──────────┘  └──────────┘
```

---

## 7. 故障处理

| 问题 | 排查方法 |
|------|----------|
| 服务无法启动 | `docker-compose logs` 查看错误日志 |
| 数据库连接失败 | 检查 PostgreSQL 是否健康：`docker-compose ps postgres` |
| 前端页面白屏 | 浏览器 F12 → Console 查看 API 请求是否被拦截 |
| 证书过期 | `certbot renew` 然后重启 frontend |
| 磁盘空间不足 | `docker system prune -af` 清理未使用的镜像和容器 |

---

## 8. 安全建议

- 修改默认密码（admin/admin123 → 强密码）
- 生产环境 `DEBUG=false`
- 配置防火墙，仅开放 80/443 端口
- 定期更新 Docker 镜像
- 启用审计日志（系统已内置）
