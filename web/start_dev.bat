@echo off
echo Starting FlowCast Development Environment...
echo.

:: Start backend in a new window
echo Starting backend server...
start "FlowCast Backend" cmd /k "cd /d %~dp0backend && python main.py"

:: Wait a moment for backend to start
timeout /t 3 /nobreak > nul

:: Start frontend in a new window
echo Starting frontend dev server...
start "FlowCast Frontend" cmd /k "cd /d %~dp0frontend && npm run dev"

echo.
echo FlowCast is starting...
echo   Backend: http://localhost:8000
echo   Frontend: http://localhost:5173
echo.
echo Close the terminal windows to stop the servers.
