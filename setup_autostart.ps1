# Script PowerShell para configurar autostart de Air Touch Interface
# Ejecutar como administrador

# Obtener directorio actual
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$pythonExe = Join-Path $scriptDir "airtouch_env\Scripts\python.exe"
$startupScript = Join-Path $scriptDir "startup_auto.py"

Write-Host ""
Write-Host "================================================" -ForegroundColor Green
Write-Host "AIR TOUCH INTERFACE - SETUP AUTOSTART" -ForegroundColor Green
Write-Host "================================================" -ForegroundColor Green
Write-Host ""

# Verificar permisos de administrador
$currentUser = [System.Security.Principal.WindowsIdentity]::GetCurrent()
$principal = New-Object System.Security.Principal.WindowsPrincipal($currentUser)
$isAdmin = $principal.IsInRole([System.Security.Principal.WindowsBuiltInRole]::Administrator)

if (-not $isAdmin) {
    Write-Host "ERROR: Este script requiere permisos de administrador" -ForegroundColor Red
    Write-Host ""
    Write-Host "Por favor, ejecuta PowerShell como administrador y corre este script nuevamente."
    Write-Host ""
    Read-Host "Presiona Enter para salir"
    exit 1
}

# Verificar que exista Python
if (-not (Test-Path $pythonExe)) {
    Write-Host "ERROR: No se encontro Python en $pythonExe" -ForegroundColor Red
    Read-Host "Presiona Enter para salir"
    exit 1
}

# Verificar que exista el script
if (-not (Test-Path $startupScript)) {
    Write-Host "ERROR: No se encontro $startupScript" -ForegroundColor Red
    Read-Host "Presiona Enter para salir"
    exit 1
}

Write-Host "Configurando tarea programada..." -ForegroundColor Yellow
Write-Host ""

# Crear tarea programada
$action = New-ScheduledTaskAction -Execute $pythonExe -Argument $startupScript
$trigger = New-ScheduledTaskTrigger -AtLogOn
$settings = New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries

try {
    Register-ScheduledTask -TaskName "AirTouchInterface" `
        -Action $action `
        -Trigger $trigger `
        -Settings $settings `
        -RunLevel Highest `
        -Force | Out-Null
    
    Write-Host ""
    Write-Host "================================================" -ForegroundColor Green
    Write-Host "✅ AUTOSTART CONFIGURADO EXITOSAMENTE" -ForegroundColor Green
    Write-Host "================================================" -ForegroundColor Green
    Write-Host ""
    Write-Host "La aplicación se ejecutará automáticamente"
    Write-Host "cuando inicies sesión en Windows."
    Write-Host ""
    Write-Host "Próximas acciones:"
    Write-Host "1. Se mostrará un diálogo preguntando si"
    Write-Host "   deseas usar Air Touch Interface"
    Write-Host "2. Selecciona SÍ para usar directamente"
    Write-Host "   o NO para ajustes automáticos primero"
    Write-Host ""
    Write-Host "Para DESACTIVAR el autostart, ejecuta:"
    Write-Host "  Unregister-ScheduledTask -TaskName 'AirTouchInterface' -Confirm:`$false"
    Write-Host ""
    
} catch {
    Write-Host ""
    Write-Host "❌ ERROR al configurar autostart" -ForegroundColor Red
    Write-Host "Error: $_" -ForegroundColor Red
    Write-Host ""
}

Read-Host "Presiona Enter para salir"
