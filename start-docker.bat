@echo off
chcp 65001 >nul
title BridgeWatch AI - Docker 部署

echo ========================================
echo  BridgeWatch AI - Docker 全栈部署
echo ========================================
echo.
echo  启动服务:
echo    - PostgreSQL 16
echo    - Redis 7
echo    - Backend (FastAPI)
echo    - Frontend (Nginx)
echo    - Prometheus
echo    - Grafana
echo.
echo ========================================

:: Navigate to backend directory (where docker-compose.yml lives)
cd /d "%~dp0backend"

:: Build and start all services
echo [INFO] 构建并启动 Docker 服务...
docker compose up --build -d

if %errorlevel% neq 0 (
    echo [ERROR] Docker 启动失败，请确保 Docker Desktop 已安装并运行。
    pause
    exit /b 1
)

echo.
echo [INFO] 服务启动完成！访问地址：
echo.
echo  前端:     http://localhost:80
echo  后端 API:  http://localhost:8000
echo  API 文档:  http://localhost:8000/docs
echo  Prometheus: http://localhost:9090
echo  Grafana:    http://localhost:3000 (admin/admin)
echo.
echo [INFO] 查看日志: docker compose logs -f
echo [INFO] 停止服务: docker compose down
echo.
pause
