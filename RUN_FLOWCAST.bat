@echo off
setlocal EnableDelayedExpansion
title FlowCast by Books and Balances
color 0B

echo.
echo  ========================================
echo       FlowCast by Books and Balances
echo    Financial Health Check in 60 Seconds
echo  ========================================
echo.

:: Check if Node.js is installed
node --version >nul 2>&1
if errorlevel 1 goto :INSTALL_NODE
goto :CHECK_PYTHON

:INSTALL_NODE
echo [INFO] Node.js not found. Installing automatically...
echo.
winget --version >nul 2>&1
if errorlevel 1 goto :INSTALL_NODE_MANUAL
echo [INFO] Installing Node.js via Windows Package Manager...
winget install OpenJS.NodeJS.LTS --accept-source-agreements --accept-package-agreements
goto :NODE_INSTALLED

:INSTALL_NODE_MANUAL
echo [INFO] Downloading Node.js installer...
powershell -Command "Invoke-WebRequest -Uri 'https://nodejs.org/dist/v20.11.0/node-v20.11.0-x64.msi' -OutFile '%TEMP%\nodejs_installer.msi'"
echo [INFO] Running Node.js installer - please follow the prompts...
msiexec /i "%TEMP%\nodejs_installer.msi"
goto :NODE_INSTALLED

:NODE_INSTALLED
echo [INFO] Refreshing environment...
call refreshenv >nul 2>&1
node --version >nul 2>&1
if errorlevel 1 goto :NODE_RESTART_NEEDED
echo [OK] Node.js installed successfully!
echo.
goto :CHECK_PYTHON

:NODE_RESTART_NEEDED
echo.
echo [WARNING] Node.js installed but requires a restart.
echo Please close this window and run the script again.
echo.
pause
exit /b 1

:CHECK_PYTHON
python --version >nul 2>&1
if errorlevel 1 goto :INSTALL_PYTHON
goto :SETUP_APP

:INSTALL_PYTHON
echo [INFO] Python not found. Installing automatically...
echo.
winget --version >nul 2>&1
if errorlevel 1 goto :INSTALL_PYTHON_MANUAL
echo [INFO] Installing Python via Windows Package Manager...
winget install Python.Python.3.12 --accept-source-agreements --accept-package-agreements
goto :PYTHON_INSTALLED

:INSTALL_PYTHON_MANUAL
echo [INFO] Downloading Python installer...
powershell -Command "Invoke-WebRequest -Uri 'https://www.python.org/ftp/python/3.12.0/python-3.12.0-amd64.exe' -OutFile '%TEMP%\python_installer.exe'"
echo [INFO] Running Python installer...
"%TEMP%\python_installer.exe" /passive InstallAllUsers=0 PrependPath=1
goto :PYTHON_INSTALLED

:PYTHON_INSTALLED
echo [INFO] Refreshing environment...
call refreshenv >nul 2>&1
python --version >nul 2>&1
if errorlevel 1 goto :PYTHON_RESTART_NEEDED
echo [OK] Python installed successfully!
echo.
goto :SETUP_APP

:PYTHON_RESTART_NEEDED
echo.
echo [WARNING] Python installed but requires a restart.
echo Please close this window and run the script again.
echo.
pause
exit /b 1

:SETUP_APP

:: Install backend dependencies if needed
echo [INFO] Checking backend dependencies...
cd /d "%~dp0web\backend"
python -c "import fastapi" >nul 2>&1
if errorlevel 1 (
    echo [INFO] Installing backend packages...
    pip install -r requirements.txt
)

:: Install frontend dependencies if needed
echo [INFO] Checking frontend dependencies...
cd /d "%~dp0web\frontend"
if not exist "node_modules" (
    echo [INFO] Installing frontend packages...
    npm install
)

:: Start backend server in background
echo [INFO] Starting backend server...
cd /d "%~dp0web\backend"
start /B "" python main.py

:: Wait for backend to start
timeout /t 3 /nobreak > nul

:: Start frontend and open browser
echo [INFO] Starting frontend...
echo.
echo  ========================================
echo   FlowCast is running!
echo   Opening browser to: http://localhost:5173
echo  ========================================
echo.
echo  Close this window to stop the servers.
echo.

cd /d "%~dp0web\frontend"

:: Open browser after a short delay
start "" cmd /c "timeout /t 2 /nobreak > nul && start http://localhost:5173"

:: Run frontend (this keeps the window open)
npm run dev
