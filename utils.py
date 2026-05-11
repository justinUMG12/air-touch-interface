"""
Utilidades generales: carga de configuración, suavizado, distancias,
reproducción de sonidos y dibujo en la imagen.
Optimizado para cámaras de baja calidad.
"""

import json
import math
from collections import deque
import time
import os
import winsound  # Solo Windows, para beeps simples

def load_config(path="config.json"):
    """Carga el archivo de configuración JSON y devuelve un diccionario."""
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def play_sound(sound_path=None, frequency=800, duration=100):
    """
    Reproduce un sonido. Si existe el archivo .wav lo usa;
    en caso contrario genera un beep con la frecuencia y duración dadas.
    """
    try:
        if sound_path and os.path.exists(sound_path):
            volume = 0.7
            winsound.PlaySound(sound_path, winsound.SND_FILENAME | winsound.SND_ASYNC)
        else:
            winsound.Beep(frequency, duration)
    except:
        pass  # Silently fail if sound not available

def distance(a, b):
    """Distancia euclidiana entre dos puntos (x,y) o (x,y,z)."""
    if len(a) < 2 or len(b) < 2:
        return 0
    dx = a[0] - b[0]
    dy = a[1] - b[1]
    dz = (a[2] - b[2]) if (len(a) > 2 and len(b) > 2) else 0
    return math.sqrt(dx*dx + dy*dy + dz*dz)

def moving_average_smoother(window_size=5):
    """
    Devuelve un callable que suaviza un valor mediante media móvil.
    Uso:
        smoother = moving_average_smoother(5)
        smooth_val = smoother(new_raw_value)
    """
    buffer = deque(maxlen=window_size)
    def smooth(value):
        buffer.append(value)
        return sum(buffer) / len(buffer)
    return smooth

def draw_ui_overlay(frame, state, fps, depth_val, is_touching, config, hands=None):
    """
    Dibuja indicadores visuales sobre el frame:
    estado (MOVE, TOUCH, etc.), FPS, barra de profundidad.
    Optimizado para baja calidad de cámara.
    """
    import cv2
    import numpy as np
    h, w, _ = frame.shape

    # Fondo semi-transparente para texto superior
    overlay = frame.copy()
    cv2.rectangle(overlay, (0, 0), (400, 90), (0, 0, 0), -1)
    cv2.addWeighted(overlay, 0.3, frame, 0.7, 0, frame)

    # Estado actual - más visible
    state_color = (0, 255, 0) if state == "MOVE" else (255, 165, 0) if state == "TOUCH_DOWN" else (0, 0, 255)
    cv2.putText(frame, f"Estado: {state}", (15, 35),
                cv2.FONT_HERSHEY_SIMPLEX, 0.8, state_color, 2)
    
    # FPS
    if config["debug"]["show_fps"]:
        fps_color = (0, 255, 0) if fps > 20 else (255, 165, 0) if fps > 10 else (0, 0, 255)
        cv2.putText(frame, f"FPS: {int(fps)}", (15, 65),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, fps_color, 2)

    # Manos detectadas
    if hands is not None:
        hands_text = f"Manos: {len(hands)}"
        hands_color = (0, 255, 0) if len(hands) > 0 else (0, 0, 255)
        cv2.putText(frame, hands_text, (280, 35),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, hands_color, 2)

    # Barra de profundidad mejorada (zona de toque)
    bar_x = w - 50
    bar_top = 100
    bar_bottom = h - 60
    bar_height = bar_bottom - bar_top
    bar_width = 20
    
    # Fondo de la barra
    cv2.rectangle(frame, (bar_x - bar_width//2, bar_top), 
                  (bar_x + bar_width//2, bar_bottom), (60, 60, 60), -1)
    cv2.rectangle(frame, (bar_x - bar_width//2, bar_top), 
                  (bar_x + bar_width//2, bar_bottom), (150, 150, 150), 2)
    
    # Indicador de profundidad actual
    if depth_val is not None:
        depth_y = int(bar_bottom - depth_val * bar_height)
        depth_y = max(bar_top, min(bar_bottom, depth_y))
        color = (0, 255, 0) if not is_touching else (0, 0, 255)
        cv2.circle(frame, (bar_x, depth_y), 12, color, -1)
        cv2.circle(frame, (bar_x, depth_y), 12, (255, 255, 255), 2)

    # Línea del umbral de toque
    touch_y = int(bar_bottom - config["touch"]["touch_depth_threshold"] * bar_height)
    cv2.line(frame, (bar_x - bar_width - 5, touch_y), (bar_x + bar_width + 5, touch_y), 
             (255, 0, 0), 3)
    cv2.putText(frame, "TOUCH", (bar_x - 45, touch_y + 5),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 1)

    # Indicador de "toque activo" más visible
    if is_touching:
        # Círculo pulsante
        radius = 25
        cv2.circle(frame, (60, h - 60), radius, (0, 0, 255), 3)
        cv2.circle(frame, (60, h - 60), radius - 5, (0, 0, 255), -1)
        cv2.putText(frame, "PRESIONANDO", (100, h - 55),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)
    
    # Instrucciones en la esquina inferior
    instructions = [
        "q: Salir | d: Debug | c: Calibrar",
    ]
    for i, text in enumerate(instructions):
        cv2.putText(frame, text, (15, h - 15 - (i * 25)),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (200, 200, 200), 1)

    return frame