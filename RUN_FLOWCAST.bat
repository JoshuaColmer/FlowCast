@echo off
echo ========================================
echo    FlowCast Report Generator
echo ========================================
echo.

:: Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python from https://python.org
    pause
    exit /b 1
)

:: Check if dependencies are installed, install if not
echo Checking dependencies...
pip show streamlit >nul 2>&1
if errorlevel 1 (
    echo Installing required packages...
    pip install -r requirements.txt
)

echo.
echo Starting FlowCast...
echo.
echo The app will open in your web browser automatically.
echo To stop the app, close this window or press Ctrl+C
echo.

:: Run the streamlit app
streamlit run flowcast_app.py --server.headless=true

pause
