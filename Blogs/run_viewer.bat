@echo off
REM YouTube Channel Video Viewer - Batch Launcher
REM Double-click this file to run the application

echo.
echo ========================================
echo YouTube Channel Video Viewer
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo.
    echo Please install Python from: https://www.python.org
    echo Make sure to check "Add Python to PATH" during installation
    echo.
    pause
    exit /b 1
)

REM Check if requirements are installed
python -c "import PIL, requests, yt_dlp, bs4" >nul 2>&1
if errorlevel 1 (
    echo Installing required packages...
    pip install -q pillow requests yt-dlp beautifulsoup4
    if errorlevel 1 (
        echo ERROR: Failed to install packages
        echo Please run in PowerShell:
        echo pip install -r requirements.txt
        echo.
        pause
        exit /b 1
    )
    echo Packages installed successfully!
    echo.
)

REM Run the application
echo Starting YouTube Channel Video Viewer...
echo.

python youtube_channel_viewer.py

if errorlevel 1 (
    echo.
    echo ERROR: Application failed to start
    echo.
    pause
)

exit /b 0
