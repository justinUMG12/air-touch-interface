"""
Enhanced Cursor Controller with Advanced Features
Includes adaptive smoothing, precision modes, accessibility features, and more.
"""

import pyautogui
import math
import time
from collections import deque
import numpy as np

pyautogui.FAILSAFE = False


class EnhancedCursorController:
    """Controlador de cursor avanzado con múltiples modos y características."""
    
    def __init__(self, config):
        # Configuración básica
        self.config = config
        self.sensitivity = config.get("cursor", {}).get("speed", 1.8)
        self.smoothing_factor = config.get("cursor", {}).get("smoothing", 0.5)
        self.move_threshold = config.get("cursor", {}).get("precision", 1)
        self.border_margin = 10
        self.screen_width, self.screen_height = pyautogui.size()
        
        # Posiciones suavizadas
        self.smooth_x = self.screen_width // 2
        self.smooth_y = self.screen_height // 2
        self.target_x = self.smooth_x
        self.target_y = self.smooth_y
        
        # Estado de botones
        self.left_pressed = False
        self.right_pressed = False
        
        # Historial para análisis adaptativo
        self.position_history = deque(maxlen=10)
        self.velocity_history = deque(maxlen=10)
        
        # Parámetros adaptativos
        self.adaptive_smoothing = config.get("adaptive", {}).get("dynamic_smoothing", True)
        self.current_smoothing = self.smoothing_factor
        self.stability_level = config.get("cursor", {}).get("stability", "medium")
        
        # Anti-jitter
        self.jitter_threshold = 2
        self.jitter_buffer = deque(maxlen=5)
        
        # Acceleration
        self.acceleration = config.get("cursor", {}).get("acceleration", 1.1)
        self.last_velocity = 0
        
        # Accessibility
        self.large_cursor_mode = config.get("accessibility", {}).get("cursor_size_large", False)
        self.cursor_size = "gigantic" if self.large_cursor_mode else "medium"
        
    def map_to_screen(self, finger_x, finger_y, frame_width, frame_height):
        """Mapea coordenadas de cámara a pantalla."""
        norm_x = 1.0 - (finger_x / frame_width)
        norm_y = finger_y / frame_height
        
        cx, cy = 0.5, 0.5
        dx = (norm_x - cx) * self.sensitivity
        dy = (norm_y - cy) * self.sensitivity
        
        screen_x = (cx + dx) * self.screen_width
        screen_y = (cy + dy) * self.screen_height
        
        # Limitar bordes
        screen_x = max(self.border_margin, min(self.screen_width - self.border_margin, screen_x))
        screen_y = max(self.border_margin, min(self.screen_height - self.border_margin, screen_y))
        
        return screen_x, screen_y
    
    def apply_jitter_reduction(self, x, y):
        """Reduce jitter en movimiento pequeño."""
        if len(self.jitter_buffer) > 0:
            avg_x = sum(pos[0] for pos in self.jitter_buffer) / len(self.jitter_buffer)
            avg_y = sum(pos[1] for pos in self.jitter_buffer) / len(self.jitter_buffer)
            
            if math.sqrt((x - avg_x)**2 + (y - avg_y)**2) < self.jitter_threshold:
                x = avg_x
                y = avg_y
        
        self.jitter_buffer.append((x, y))
        return x, y
    
    def apply_adaptive_smoothing(self):
        """Aplica suavizado adaptativo basado en velocidad."""
        if not self.adaptive_smoothing:
            return self.smoothing_factor
        
        if len(self.velocity_history) > 0:
            avg_velocity = sum(self.velocity_history) / len(self.velocity_history)
            
            # Aumentar smoothing si velocidad es alta (movimiento rápido)
            if avg_velocity > 50:
                self.current_smoothing = min(self.smoothing_factor * 1.3, 0.9)
            # Reducir smoothing si velocidad es baja (movimiento lento/preciso)
            elif avg_velocity < 10:
                self.current_smoothing = max(self.smoothing_factor * 0.7, 0.1)
            else:
                self.current_smoothing = self.smoothing_factor
        
        return self.current_smoothing
    
    def calculate_velocity(self):
        """Calcula velocidad del cursor."""
        if len(self.position_history) < 2:
            return 0
        
        prev_x, prev_y = self.position_history[-2]
        curr_x, curr_y = self.position_history[-1]
        
        velocity = math.sqrt((curr_x - prev_x)**2 + (curr_y - prev_y)**2)
        self.velocity_history.append(velocity)
        return velocity
    
    def update_cursor(self, finger_tip, frame_shape, gesture_state):
        """Actualiza posición del cursor con features avanzadas."""
        if gesture_state == "SCROLL":
            return
        
        if finger_tip is None:
            return
        
        frame_height, frame_width = frame_shape[:2]
        target_x, target_y = self.map_to_screen(finger_tip[0], finger_tip[1], 
                                                frame_width, frame_height)
        
        # Reducir jitter
        target_x, target_y = self.apply_jitter_reduction(target_x, target_y)
        
        # Aplicar suavizado adaptativo
        smoothing = self.apply_adaptive_smoothing()
        
        # Suavizado exponencial
        self.smooth_x += (target_x - self.smooth_x) * (1.0 - smoothing)
        self.smooth_y += (target_y - self.smooth_y) * (1.0 - smoothing)
        
        # Registrar en historial
        self.position_history.append((self.smooth_x, self.smooth_y))
        
        # Calcular velocidad
        self.calculate_velocity()
        
        # Mover cursor si cambio es significativo
        current_pos = pyautogui.position()
        dx = self.smooth_x - current_pos.x
        dy = self.smooth_y - current_pos.y
        
        distance = math.sqrt(dx**2 + dy**2)
        
        if distance > self.move_threshold:
            pyautogui.moveTo(self.smooth_x, self.smooth_y, duration=0.0)
    
    def perform_left_click(self):
        """Clic izquierdo."""
        pyautogui.click(button='left')
    
    def perform_double_click(self):
        """Doble clic."""
        pyautogui.doubleClick(button='left')
    
    def perform_right_click(self):
        """Clic derecho."""
        pyautogui.click(button='right')
    
    def start_drag(self):
        """Inicia arrastre."""
        if not self.left_pressed:
            pyautogui.mouseDown(button='left')
            self.left_pressed = True
    
    def stop_drag(self):
        """Finaliza arrastre."""
        if self.left_pressed:
            pyautogui.mouseUp(button='left')
            self.left_pressed = True
    
    def perform_scroll(self, direction, amount=3):
        """Ejecuta scroll."""
        if direction == "up":
            pyautogui.scroll(amount)
        elif direction == "down":
            pyautogui.scroll(-amount)
    
    def set_sensitivity(self, sensitivity):
        """Cambia sensibilidad."""
        self.sensitivity = sensitivity
    
    def set_smoothing(self, smoothing):
        """Cambia suavizado."""
        self.smoothing_factor = smoothing
        self.current_smoothing = smoothing
    
    def set_stability_level(self, level):
        """Cambia nivel de estabilidad."""
        self.stability_level = level
        
        stability_map = {
            "low": {"smoothing": 0.3, "jitter": 3},
            "medium": {"smoothing": 0.5, "jitter": 2},
            "high": {"smoothing": 0.7, "jitter": 1},
            "extreme": {"smoothing": 0.9, "jitter": 0.5}
        }
        
        params = stability_map.get(level, stability_map["medium"])
        self.smoothing_factor = params["smoothing"]
        self.jitter_threshold = params["jitter"]


class CursorPresets:
    """Presets de configuración de cursor."""
    
    GAMING = {
        "speed": 2.5,
        "smoothing": 0.3,
        "stability": "low",
        "acceleration": 1.2
    }
    
    PRECISION = {
        "speed": 1.2,
        "smoothing": 0.8,
        "stability": "high",
        "acceleration": 1.0
    }
    
    NAVIGATION = {
        "speed": 1.8,
        "smoothing": 0.5,
        "stability": "medium",
        "acceleration": 1.1
    }
    
    ACCESSIBILITY = {
        "speed": 1.0,
        "smoothing": 0.9,
        "stability": "extreme",
        "acceleration": 0.9
    }
    
    @classmethod
    def apply_preset(self, cursor_controller, preset_name):
        """Aplica un preset al cursor controller."""
        presets = {
            "gaming": self.GAMING,
            "precision": self.PRECISION,
            "navigation": self.NAVIGATION,
            "accessibility": self.ACCESSIBILITY
        }
        
        preset = presets.get(preset_name.lower(), presets["navigation"])
        
        cursor_controller.set_sensitivity(preset["speed"])
        cursor_controller.set_smoothing(preset["smoothing"])
        cursor_controller.set_stability_level(preset["stability"])
        cursor_controller.acceleration = preset["acceleration"]
