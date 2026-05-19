@echo off
chcp 65001 >nul
title BridgeWatch AI - Frontend

echo ========================================
echo  BridgeWatch AI - 前端启动脚本
echo ========================================
echo.

:: Navigate to frontend directory
cd /d "%~dp0bridgewatch-ai"

:: Check if node_modules exists
if not exist node_modules (
    echo [INFO] 安装前端依赖...
    call npm install
)

:: Start frontend dev server
echo [INFO] 启动前端开发服务器 (http://localhost:5173)...
echo.
npm run dev

pause
