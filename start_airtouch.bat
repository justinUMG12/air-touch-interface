@echo off
REM Air Touch Interface - Quick Start
REM Simplified launcher - double-click to run

setlocal enabledelayedexpansion

REM Navigate to script directory
cd /d "%~dp0"

REM Activate virtual environment if it exists
if exist "airtouch_env\Scripts\activate.bat" (
    call airtouch_env\Scripts\activate.bat
)

REM Run directly (skip launcher menu)
python main.py

if errorlevel 1 (
    echo.
    echo ERROR: Application failed
    echo Check logs for details
    echo.
    pause
    exit /b 1
)
