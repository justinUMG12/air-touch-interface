@echo off
REM Air Touch Interface - Professional Launcher
REM Run this file to start the application with professional UI

setlocal enabledelayedexpansion

REM Check Python installation
python --version >nul 2>&1
if errorlevel 1 (
    echo.
    echo ============================================================
    echo ERROR: Python is not installed or not in PATH
    echo ============================================================
    echo.
    echo Please install Python 3.8+ and add it to your system PATH
    echo Download from: https://www.python.org/downloads/
    echo.
    pause
    exit /b 1
)

REM Navigate to script directory
cd /d "%~dp0"

REM Activate virtual environment if it exists
if exist "airtouch_env\Scripts\activate.bat" (
    call airtouch_env\Scripts\activate.bat
)

REM Run launcher
echo.
echo ============================================================
echo   AIR TOUCH INTERFACE v3.5 - PROFESSIONAL LAUNCHER
echo ============================================================
echo.

python launcher.py

if errorlevel 1 (
    echo.
    echo ============================================================
    echo ERROR: Launcher failed
    echo ============================================================
    echo.
    pause
    exit /b 1
)

pause
