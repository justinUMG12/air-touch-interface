@echo off
REM ========================================
REM Air Touch Interface v3.5
REM Complete Setup and Initialization Script
REM ========================================

cls
echo.
echo ========================================
echo   AIR TOUCH INTERFACE v3.5 SETUP
echo   Complete Installation & Configuration
echo ========================================
echo.

REM Check Python
echo Checking Python installation...
python --version >nul 2>&1
if errorlevel 1 (
    echo.
    echo ERROR: Python not found!
    echo.
    echo Please download Python 3.8+ from: https://www.python.org/downloads/
    echo Make sure to check "Add Python to PATH" during installation
    echo.
    pause
    exit /b 1
)

for /f "tokens=2" %%i in ('python --version 2^>^&1') do set PYTHON_VERSION=%%i
echo OK: Python %PYTHON_VERSION% found
echo.

REM Create virtual environment if it doesn't exist
if not exist "airtouch_env\" (
    echo.
    echo Creating virtual environment...
    python -m venv airtouch_env
    if errorlevel 1 (
        echo ERROR: Failed to create virtual environment
        pause
        exit /b 1
    )
    echo OK: Virtual environment created
) else (
    echo OK: Virtual environment already exists
)

echo.
echo Activating virtual environment...
call airtouch_env\Scripts\activate.bat

echo.
echo Installing dependencies...
echo (This may take a few minutes...)
echo.

pip install -r requirements_v35_final.txt
if errorlevel 1 (
    echo.
    echo ERROR: Dependency installation failed
    echo Try running: pip install --upgrade pip
    pause
    exit /b 1
)

echo.
echo Validating system...
python validate_system.py
if errorlevel 1 (
    echo.
    echo WARNING: System validation found issues
    echo Please fix the errors above before running the application
    pause
    exit /b 1
)

echo.
echo ========================================
echo   SETUP COMPLETE!
echo ========================================
echo.
echo You can now run the application:
echo.
echo   Option 1: Double-click AirTouch_v35.bat
echo   Option 2: Run: python main_new.py
echo.
echo For help, read: START_HERE.md
echo.
pause
