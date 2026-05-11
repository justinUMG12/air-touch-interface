# 🚀 START HERE - Inicio Rápido

## Para Usuarios Normales (SIN programación)

### ✅ PASO 1: Doble-click

Abre el archivo:
```
AirTouch_v35.bat
```

### ✅ PASO 2: Sigue las instrucciones

La aplicación te guiará automáticamente a través de:

1. 📊 **SPLASH SCREEN** - Verificación de sistema (automático)
2. 📹 **CÁMARA** - Selecciona tu cámara (usa ← → y ENTER)
3. ⚙️ **CONFIGURACIÓN** - Ajusta velocidad, sensibilidad, etc.
4. 🧪 **PRUEBA** - Verifica que todo funciona
5. ✨ **¡LISTO!** - Controla con las manos

### ✅ PASO 3: Disfruta

- Mueve la mano para mover el cursor
- Empuja hacia la cámara para CLICK
- Presiona `D` para debug
- Presiona `Q` para salir

---

## 🎯 ¿Qué Hacer?

### Moví la mano pero el cursor no se mueve
```
1. Verifica que la cámara esté bien posicionada
2. Intenta aumentar la "Velocidad" en configuración
3. Acerca la mano más a la cámara
```

### El click no funciona
```
1. Empuja la mano MÁS hacia la cámara
2. Aumenta "Sensibilidad de pulsación" en configuración
3. Espera a que aparezca el punto verde en la pantalla
```

### La pantalla ve borroso
```
1. Limpia el lente de la cámara
2. Mejora la iluminación
3. Asegúrate de que la cámara tenga enfoque automático
```

---

## ⚡ Atajo Rápido

Si ya configuraste todo y solo quieres ejecutar:

```bash
python main_new.py
```

---

## 📹 Visualización de Manos

Verás en la pantalla:
- 🔵 **Puntos azules/cian** = articulaciones
- 🔗 **Líneas** = conexiones entre dedos
- 🟠 **Naranja** = muñeca
- 🟢 **Verde** = dedos extendidos (lista para click)

---

## 🎮 Controles Durante Uso

| Tecla | Función |
|-------|---------|
| `D` | Debug mode |
| `C` | Recalibrar |
| `Q` | Salir |

---

## 💡 TIPS

✅ **Para mejor tracking:**
- Usa buena iluminación
- Posiciona la cámara a la altura de los ojos
- Mantén las manos visibles completamente
- No uses ropa con colores muy similares a la piel

✅ **Para mejor click:**
- Empuja hacia la cámara CON FUERZA
- Mantén los dedos índice y pulgar juntos
- Espera el feedback visual (línea verde)

✅ **Para mejor rendimiento:**
- Cierra otras aplicaciones
- No uses software de zoom/grabación
- Evita cambios rápidos de luz

---

## ❌ Si algo no funciona

### Error: "No se detectó cámara"
```
Solución: Conecta una cámara USB o webcam externa
```

### Error: "Python not found"
```
Solución: Descarga Python desde python.org
Instala con "Add Python to PATH"
```

### Cursor muy rápido
```
Solución: Abre configuración y reduce "Velocidad"
```

### Cursor muy lento
```
Solución: Abre configuración y aumenta "Velocidad"
```

### App se cierra sin razón
```
Solución: Ejecuta:
pip install -r requirements_v35.txt --force-reinstall
```

---

## 🎓 Información Técnica

- **Lenguaje**: Python 3.8+
- **Cámara**: Cualquier cámara USB
- **Detección**: MediaPipe (AI machine learning)
- **Sistema**: Windows 10/11
- **RAM**: 4GB mínimo, 8GB recomendado

---

## 📊 Próximos Pasos

Después de tu primer uso:

1. Experimenta con diferentes configuraciones
2. Lee `README_v35_NEW.md` para más detalles
3. Prueba los diferentes perfiles (Gaming, Precision, etc.)
4. Personaliza los parámetros según tu gusto

---

## ✅ ¡Listo!

Doble-click en `AirTouch_v35.bat` y ¡disfruta!

Si necesitas ayuda, abre la consola y mira los mensajes de error.

**¡Bienvenido a Air Touch Interface v3.5!** 🎉
