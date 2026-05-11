# 🚀 AUTOSTART - Air Touch Interface

## ¿Qué es?
Autostart permite que Air Touch Interface se ejecute automáticamente cuando enciendes tu PC.

---

## 🎯 Características

✅ **Autoencendimiento** - Se inicia automáticamente con Windows
✅ **Diálogo Interactivo** - Pregunta si deseas usar la app
✅ **Ajustes Automáticos** - Calibración automática si lo deseas
✅ **Fácil Desactivación** - Un script para desactivar

---

## ⚙️ CONFIGURACIÓN (Windows 10/11)

### Opción 1: Script Batch (Fácil)
1. **Haz clic derecho** en `setup_autostart.bat`
2. Selecciona **"Ejecutar como administrador"**
3. El script configurará todo automáticamente

### Opción 2: PowerShell (Alternativa)
1. Abre **PowerShell como administrador**
2. Navega a la carpeta del proyecto:
   ```powershell
   cd "C:\Users\HP15C0008LA\Desktop\air_touch_interface"
   ```
3. Ejecuta:
   ```powershell
   .\setup_autostart.ps1
   ```

---

## 🎮 ¿Cómo Funciona?

### Cuando Inicias Windows:
1. **Se abre un diálogo** preguntando:
   > "¿Deseas usar Air Touch Interface ahora?"

2. **Si haces clic SÍ:**
   - ✅ La aplicación se abre normalmente
   - ✅ Todo funciona como siempre

3. **Si haces clic NO:**
   - 🔧 Se realizan ajustes automáticos:
     - Calibración automática de cámara
     - Optimización de parámetros
     - Guardado de configuración
   - ✅ Luego se abre la aplicación

### Timeout:
- Si **no haces clic en 15 segundos**, abre automáticamente

---

## 📊 Mejoras Implementadas

### startup_auto.py
```
✅ Diálogo de confirmación
✅ Ajustes automáticos
✅ Logging detallado
✅ Manejo de errores
✅ Timestamp de calibración
```

### main.py (Mejorado)
```
✅ Banner mejorado
✅ Información de sesión
✅ Logs por componente
✅ Estadísticas de calibración
```

---

## 🛠️ DESACTIVAR AUTOSTART

### Opción 1: Doble clic
Simplemente ejecuta: **`remove_autostart.bat`**

### Opción 2: Manual (PowerShell)
```powershell
Unregister-ScheduledTask -TaskName "AirTouchInterface" -Confirm:$false
```

---

## 🔍 VERIFICACIÓN

Para verificar que está configurado:

### En Windows (Programador de tareas):
1. Presiona `Windows + R`
2. Escribe: `taskschd.msc`
3. Busca: **"AirTouchInterface"**
4. Deberías verlo en la lista

### En PowerShell:
```powershell
Get-ScheduledTask -TaskName "AirTouchInterface" | Select-Object *
```

---

## 🐛 PROBLEMAS?

### No aparece el diálogo
- Verifica que tkinter esté instalado
- Prueba cerrando la app y ejecutando manualmente

### Autostart no se ejecuta
- Abre PowerShell como **administrador**
- Ejecuta: `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser`

### Quiero desactivarlo
- Ejecuta `remove_autostart.bat` o el comando de desactivación

---

## 📋 ARCHIVOS CREADOS

```
startup_auto.py          ← Script principal de autostart
setup_autostart.bat      ← Configurar (Batch)
setup_autostart.ps1      ← Configurar (PowerShell)
remove_autostart.bat     ← Desactivar
AUTOSTART_README.md      ← Este archivo
```

---

## 🚀 PRÓXIMOS PASOS

1. **Configura el autostart:**
   ```
   Doble clic → setup_autostart.bat
   ```

2. **Reinicia tu PC**

3. **Al encender, aparecerá el diálogo**

4. **¡Disfruta!**

---

## 📊 Información de Sesión

Una vez que autostart esté configurado, verás en cada inicio:

```
============================================================
  🎯 AIR TOUCH INTERFACE v2.0
============================================================

📅 Última calibración: 2026-05-11 14:30:00
🔧 Modo detección: Estándar

⏳ Inicializando componentes...
  → Hand Tracker
  → Cursor Controller
  → Gesture Engine
  → Cámara
✅ Todos los componentes inicializados
```

---

**¿Preguntas?** Revisa `QUICKSTART.md` o `IMPROVEMENTS.md`

**¡Autostart listo para usar! 🎉**
