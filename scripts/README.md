# BridgeWatch AI 数据库备份与恢复

## 备份

### 方式一：PostgreSQL（生产环境）

```bash
# 使用默认配置
./scripts/backup.sh

# 自定义数据库连接
DB_HOST=192.168.1.100 DB_NAME=bridgewatch ./scripts/backup.sh
```

### 方式二：Docker PostgreSQL

```bash
./scripts/backup.sh --docker
```

### 方式三：SQLite（开发环境）

```bash
./scripts/backup.sh --sqlite ./data/bridgewatch.db
```

### 定时备份（Docker 环境）

在 `docker-compose.yml` 中添加：

```yaml
db-backup:
  image: alpine:latest
  volumes:
    - ./backups:/backups
    - pgdata:/var/lib/postgresql/data:ro
  entrypoint: |
    sh -c "
    apk add --no-cache postgresql-client &&
    while true; do
      PGPASSWORD=postgres pg_dump -h postgres -U postgres -d bridgewatch -F c > /backups/bridgewatch_\$(date +%Y%m%d_%H%M%S).dump
      find /backups -name 'bridgewatch_*.dump' -mtime +30 -delete
      sleep 86400
    done
    "
```

## 恢复

```bash
# 恢复 PostgreSQL
./scripts/restore.sh ./backups/bridgewatch_pg_20260519_120000.sql.gz

# 恢复 SQLite
./scripts/restore.sh ./backups/bridgewatch_sqlite_20260519_120000.db.gz
```

## 备份文件

所有备份文件保存在 `backups/` 目录，命名格式：

```
bridgewatch_pg_YYYYMMDD_HHMMSS.sql.gz   # PostgreSQL
bridgewatch_sqlite_YYYYMMDD_HHMMSS.db.gz # SQLite
```

自动清理 30 天前的旧备份。
