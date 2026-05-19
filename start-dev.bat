@echo off
chcp 65001 >nul
title BridgeWatch AI - Dev (Frontend + Backend)

echo ========================================
echo  BridgeWatch AI - 本地开发启动
echo ========================================
echo.

:: Start backend in a new window
echo [1/2] 启动后端服务...
start "BridgeWatch-Backend" cmd /c "%~dp0start-backend.bat"

:: Small delay to let backend start
timeout /t 3 /nobreak >nul

:: Start frontend in a new window
echo [2/2] 启动前端开发服务器...
start "BridgeWatch-Frontend" cmd /c "%~dp0start-frontend.bat"

echo.
echo ========================================
echo  前后端已启动！
echo  前端: http://localhost:5173
echo  后端: http://localhost:8000
echo  API 文档: http://localhost:8000/docs
echo ========================================
echo.
echo 关闭窗口即可停止服务。
echo.
pause
