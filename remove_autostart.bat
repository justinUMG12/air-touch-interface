@echo off
REM Script para DESACTIVAR el autostart de Air Touch Interface

echo.
echo ================================================
echo AIR TOUCH INTERFACE - REMOVE AUTOSTART
echo ================================================
echo.

echo Removiendo tarea programada...
echo.

schtasks /delete /tn "AirTouchInterface" /f

if %ERRORLEVEL% EQU 0 (
    echo.
    echo ================================================
    echo ✅ AUTOSTART REMOVIDO CORRECTAMENTE
    echo ================================================
    echo.
    echo Air Touch Interface ya NO se ejecutará
    echo automáticamente al iniciar sesión.
    echo.
    pause
) else (
    echo.
    echo ⚠️  Posible error al remover autostart
    echo (Podría no estar configurado)
    echo.
    pause
)
