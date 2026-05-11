@echo off
REM ========================================
REM Air Touch Interface v3.5 - Ultimate Edition
REM New Professional Launcher
REM ========================================

cls

REM Colors and formatting
echo.
echo ========================================
echo     AIR TOUCH INTERFACE v3.5
echo     ULTIMATE EDITION
echo ========================================
echo.

REM Check Python
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python not found
    echo Please install Python 3.8+ from python.org
    pause
    exit /b 1
)

REM Activate virtual environment if it exists
if exist "airtouch_env\Scripts\activate.bat" (
    call airtouch_env\Scripts\activate.bat
) else (
    echo NOTE: Virtual environment not found
    echo Using system Python installation
    echo.
)

REM Run the new main application
echo Starting Air Touch Interface...
echo.

python main_new.py

REM Pause to show output if there was an error
if errorlevel 1 (
    echo.
    echo Press any key to close...
    pause
)

exit /b %errorlevel%
