@echo off
REM Kundali AI GUI Launcher
REM This script installs dependencies and launches the GUI

echo.
echo ========================================
echo   Kundali AI - GUI Launcher
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.8+ from https://www.python.org/
    pause
    exit /b 1
)

REM Check if pip is available
pip --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: pip is not available
    pause
    exit /b 1
)

REM Install/Upgrade requirements
echo Installing dependencies...
pip install -q --upgrade pip
pip install -r requirements.txt

if errorlevel 1 (
    echo ERROR: Failed to install dependencies
    pause
    exit /b 1
)

echo.
echo ========================================
echo   Launching Kundali AI GUI...
echo ========================================
echo.

REM Launch the GUI application
python kundali_gui.py

if errorlevel 1 (
    echo.
    echo ERROR: Failed to launch application
    pause
    exit /b 1
)

exit /b 0
