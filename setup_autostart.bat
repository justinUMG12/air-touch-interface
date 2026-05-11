@echo off
REM Script de configuración para autostart de Air Touch Interface
REM Ejecuta startup_auto.py automáticamente al encender la PC

setlocal enabledelayedexpansion

echo.
echo ================================================
echo AIR TOUCH INTERFACE - SETUP AUTOSTART
echo ================================================
echo.

REM Obtener la ruta actual
set SCRIPT_DIR=%~dp0
set PYTHON_EXE=%SCRIPT_DIR%airtouch_env\Scripts\python.exe
set STARTUP_SCRIPT=%SCRIPT_DIR%startup_auto.py

echo Directorio: %SCRIPT_DIR%
echo Python: %PYTHON_EXE%
echo Script: %STARTUP_SCRIPT%
echo.

REM Verificar que exista el archivo de python
if not exist "%PYTHON_EXE%" (
    echo ERROR: No se encontro Python en el entorno virtual
    echo Verifica que airtouch_env este instalado correctamente
    pause
    exit /b 1
)

REM Verificar que exista el script de startup
if not exist "%STARTUP_SCRIPT%" (
    echo ERROR: No se encontro startup_auto.py
    pause
    exit /b 1
)

echo Configurando tarea programada...
echo.

REM Crear tarea que se ejecute al iniciar sesión del usuario
schtasks /create /tn "AirTouchInterface" /tr ^
    "\"%PYTHON_EXE%\" \"%STARTUP_SCRIPT%\"" ^
    /sc onlogon /rl highest /f

if %ERRORLEVEL% EQU 0 (
    echo.
    echo ================================================
    echo ✅ AUTOSTART CONFIGURADO EXITOSAMENTE
    echo ================================================
    echo.
    echo La aplicación se ejecutará automáticamente
    echo cuando inicies sesión en Windows.
    echo.
    echo Próximas acciones:
    echo 1. Se mostrará un diálogo preguntando si
    echo    deseas usar Air Touch Interface
    echo 2. Selecciona SÍ para usar directamente
    echo    o NO para ajustes automáticos primero
    echo.
    echo Para DESACTIVAR el autostart, ejecuta:
    echo   schtasks /delete /tn "AirTouchInterface" /f
    echo.
    pause
) else (
    echo.
    echo ❌ ERROR al configurar autostart
    echo.
    echo Es posible que necesites permisos de administrador.
    echo Intenta ejecutar este script como administrador.
    echo.
    pause
    exit /b 1
)
