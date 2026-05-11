# Script PowerShell para configurar TODOSIN autostart

Write-Host ""
Write-Host "================================================" -ForegroundColor Green
Write-Host "AIR TOUCH INTERFACE - AUTOSTART QUICK SETUP" -ForegroundColor Green
Write-Host "================================================" -ForegroundColor Green
Write-Host ""

# Verificar permisos de admin
$currentUser = [System.Security.Principal.WindowsIdentity]::GetCurrent()
$principal = New-Object System.Security.Principal.WindowsPrincipal($currentUser)
$isAdmin = $principal.IsInRole([System.Security.Principal.WindowsBuiltInRole]::Administrator)

if (-not $isAdmin) {
    Write-Host "⚠️  REQUIERE PERMISOS DE ADMINISTRADOR" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "Por favor, ejecuta PowerShell como administrador:"
    Write-Host "1. Presiona Windows + X"
    Write-Host "2. Selecciona 'Windows PowerShell (admin)'"
    Write-Host "3. Corre este script nuevamente"
    Write-Host ""
    Read-Host "Presiona Enter para cerrar"
    exit 1
}

Write-Host "✅ Permisos de administrador detectados" -ForegroundColor Green
Write-Host ""

# Obtener directorio del script
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$pythonExe = Join-Path $scriptDir "airtouch_env\Scripts\python.exe"
$startupScript = Join-Path $scriptDir "startup_auto.py"

Write-Host "📁 Directorio: $scriptDir" -ForegroundColor Cyan
Write-Host "🐍 Python: $pythonExe" -ForegroundColor Cyan
Write-Host "📄 Startup: $startupScript" -ForegroundColor Cyan
Write-Host ""

# Verificar archivos
Write-Host "🔍 Verificando archivos..." -ForegroundColor Yellow
$filesOk = $true

if (-not (Test-Path $pythonExe)) {
    Write-Host "❌ No se encontró Python" -ForegroundColor Red
    $filesOk = $false
}

if (-not (Test-Path $startupScript)) {
    Write-Host "❌ No se encontró startup_auto.py" -ForegroundColor Red
    $filesOk = $false
}

if (-not $filesOk) {
    Write-Host ""
    Read-Host "Presiona Enter para salir"
    exit 1
}

Write-Host "✅ Todos los archivos encontrados" -ForegroundColor Green
Write-Host ""

# Ejecutar pruebas
Write-Host "🧪 Ejecutando pruebas..." -ForegroundColor Yellow
$testScript = Join-Path $scriptDir "test_startup.py"

if (Test-Path $testScript) {
    & $pythonExe $testScript
    Write-Host ""
} else {
    Write-Host "⚠️  Script de pruebas no encontrado" -ForegroundColor Yellow
}

# Configurar tarea
Write-Host ""
Write-Host "⚙️  Configurando tarea programada..." -ForegroundColor Yellow
Write-Host ""

$action = New-ScheduledTaskAction -Execute $pythonExe -Argument $startupScript
$trigger = New-ScheduledTaskTrigger -AtLogOn
$settings = New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries

try {
    $existingTask = Get-ScheduledTask -TaskName "AirTouchInterface" -ErrorAction SilentlyContinue
    if ($existingTask) {
        Write-Host "🔄 Actualizando tarea existente..." -ForegroundColor Yellow
        Unregister-ScheduledTask -TaskName "AirTouchInterface" -Confirm:$false | Out-Null
    }
    
    Register-ScheduledTask -TaskName "AirTouchInterface" `
        -Action $action `
        -Trigger $trigger `
        -Settings $settings `
        -RunLevel Highest `
        -Force | Out-Null
    
    Write-Host ""
    Write-Host "================================================" -ForegroundColor Green
    Write-Host "✅ AUTOSTART CONFIGURADO CORRECTAMENTE" -ForegroundColor Green
    Write-Host "================================================" -ForegroundColor Green
    Write-Host ""
    Write-Host "📋 Lo que sucederá ahora:" -ForegroundColor Cyan
    Write-Host "  1. Cuando inicies Windows se abrirá un diálogo"
    Write-Host "  2. Preguntará si quieres usar Air Touch Interface"
    Write-Host "  3. Si dices SÍ → Abre directamente"
    Write-Host "     Si dices NO → Ajustes automáticos primero"
    Write-Host ""
    Write-Host "🎯 Próximos pasos:" -ForegroundColor Cyan
    Write-Host "  1. Presiona cualquier tecla para cerrar esta ventana"
    Write-Host "  2. Reinicia tu PC"
    Write-Host "  3. ¡La app se abrirá automáticamente!"
    Write-Host ""
    Write-Host "🚫 Para desactivar:" -ForegroundColor Yellow
    Write-Host "  • Ejecuta: remove_autostart.bat"
    Write-Host "  • O ejecuta: Unregister-ScheduledTask -TaskName 'AirTouchInterface' -Confirm:`$false"
    Write-Host ""
    
} catch {
    Write-Host ""
    Write-Host "❌ ERROR al configurar autostart" -ForegroundColor Red
    Write-Host "Error: $_" -ForegroundColor Red
    Write-Host ""
    Write-Host "⚠️  Posibles causas:" -ForegroundColor Yellow
    Write-Host "  • Permisos insuficientes"
    Write-Host "  • Python no está instalado correctamente"
    Write-Host "  • Ruta incorrecta"
    Write-Host ""
}

Read-Host "Presiona Enter para salir"
