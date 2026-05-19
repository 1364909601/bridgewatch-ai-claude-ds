@echo off
chcp 65001 >nul
title BridgeWatch AI - Backend

echo ========================================
echo  BridgeWatch AI - 后端启动脚本
echo ========================================
echo.

:: Navigate to backend directory
cd /d "%~dp0backend"

:: Activate virtual environment (optional - comment out if using global Python)
if exist venv\Scripts\activate.bat (
    echo [INFO] 激活虚拟环境...
    call venv\Scripts\activate.bat
) else (
    echo [INFO] 未找到虚拟环境，使用全局 Python
)

:: Install dependencies if needed
echo [INFO] 检查依赖...
pip install -r requirements.txt -q 2>nul

:: Start backend server
echo [INFO] 启动后端服务 (http://localhost:8000)...
echo.
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

pause
