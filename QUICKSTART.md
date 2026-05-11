# 🎯 GUÍA RÁPIDA DE INICIO - Air Touch Interface

## Problema Solucionado ✅
```
Error: AttributeError: module 'mediapipe' has no attribute 'solutions'
Solución: MediaPipe 0.10.14 correctamente instalado
```

---

## Inicio Rápido en 3 Pasos

### 1️⃣ Activar Entorno Virtual
```powershell
.\airtouch_env\Scripts\activate.ps1
```

### 2️⃣ Ejecutar Aplicación
```powershell
python main.py
```

### 3️⃣ ¡Usar!
- Mueve la mano para mover el cursor
- Empuja hacia la cámara para hacer clic
- Dos dedos = scroll

---

## 🎮 Controles
| Acción | Resultado |
|--------|-----------|
| `Mover mano` | Mover cursor |
| `Empujar adelante` | Clic izquierdo |
| `Mantener + Mover` | Arrastrar |
| `Dos dedos + Mover Y` | Scroll |
| **Presiona 'q'** | **Salir** |
| **Presiona 'd'** | **Debug on/off** |
| **Presiona 'c'** | **Calibrar** |

---

## 🔧 Configuración para Tu Cámara

Si NO funciona bien, abre `config.json` y prueba:

### Cámara Muy Mala (Borrosa/Oscura)
```json
"detection_confidence": 0.4,
"tracking_confidence": 0.2,
"touch_depth_threshold": 0.32,
"sensitivity": 2.0
```

### Cámara Normal
✅ Usar configuración actual (ya está optimizada)

### Cámara Buena
```json
"detection_confidence": 0.6,
"tracking_confidence": 0.4,
"touch_depth_threshold": 0.38
```

---

## 📊 Mejoras Implementadas

✅ **Imagen**: Preprocesamiento CLAHE + Bilateral Filter
✅ **Detección**: Confianza bajada para cámaras malas
✅ **Sonidos**: Feedback en clicks
✅ **UI**: Indicadores visuales mejorados
✅ **Suavizado**: Buffer de detecciones
✅ **Errores**: Manejo robusto

---

## 🆘 Problemas?

| Problema | Solución |
|----------|----------|
| No detecta mano | ↓ detection_confidence a 0.4 |
| Cursor muy lento | ↑ sensitivity a 2.0 |
| Muy sensible | ↓ move_threshold_pixels a 0 |
| Fondo interfiere | ✅ Ya está resuelto |

---

## 📝 Especificaciones
- **MediaPipe:** 0.10.14
- **Python:** 3.12
- **OpenCV:** 4.13
- **PyAutoGUI:** 0.9.54

---

**¡Lista para usar!** 🚀
