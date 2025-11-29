@echo off
REM Astrology Matcher - Installation Helper Batch Script
REM This script helps set up the API version with one click

echo.
echo ================================================================================
echo           ASTROLOGY MATCHER - INSTALLATION HELPER
echo ================================================================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Python is not installed!
    echo.
    echo Please install Python from: https://www.python.org/downloads/
    echo Make sure to check "Add Python to PATH" during installation
    echo.
    pause
    exit /b 1
)

echo [✓] Python found
python --version
echo.

REM Check Python version
for /f "tokens=2" %%i in ('python --version 2^>^&1') do set PYTHON_VERSION=%%i
echo [✓] Version: %PYTHON_VERSION%
echo.

REM Install requests library
echo ================================================================================
echo Installing required libraries...
echo ================================================================================
echo.

echo Installing 'requests' library...
pip install requests --upgrade

if %errorlevel% neq 0 (
    echo ERROR: Could not install requests library
    echo Please try manually: pip install requests
    pause
    exit /b 1
)

echo [✓] 'requests' library installed successfully
echo.

REM Verify installation
echo ================================================================================
echo Verifying installation...
echo ================================================================================
echo.

python -c "import requests; print('[OK] requests library verified')" >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Verification failed
    pause
    exit /b 1
)

echo [✓] All dependencies verified
echo.

REM Ask to run program
echo ================================================================================
echo Installation Complete!
echo ================================================================================
echo.
echo You can now run the astrology matcher with:
echo   python astrology_matcher_api.py
echo.
echo Available programs:
echo   - astrology_matcher.py          (Local version - no internet needed)
echo   - astrology_matcher_api.py      (API version - professional results)
echo.

set /p RUN="Would you like to run the API version now? (yes/no): "

if /i "%RUN%"=="yes" (
    cls
    python astrology_matcher_api.py
) else if /i "%RUN%"=="y" (
    cls
    python astrology_matcher_api.py
) else (
    echo.
    echo You can run the program anytime with:
    echo   python astrology_matcher_api.py
    echo.
    pause
)
