"""
Professional Theme System for Air Touch Interface v3.5
Supports multiple themes: Modern Dark, Light, Neon Futuristic, Minimal, Sci-Fi
"""

import cv2
import numpy as np
from enum import Enum


class ThemeType(Enum):
    """Enum para tipos de temas."""
    MODERN_DARK = "modern_dark"
    MODERN_LIGHT = "modern_light"
    NEON_FUTURISTIC = "neon_futuristic"
    MINIMAL = "minimal"
    SCI_FI = "sci_fi"


class Theme:
    """Clase base para temas."""
    
    def __init__(self):
        self.name = "Base Theme"
        self.colors = {}
        self.transparency = 0.8
        
    def draw_cursor(self, frame, x, y, size="medium"):
        """Dibuja el cursor."""
        raise NotImplementedError
    
    def draw_hud(self, frame, fps, detection_rate):
        """Dibuja el HUD."""
        raise NotImplementedError
    
    def draw_tracking_overlay(self, frame, hands):
        """Dibuja overlay de tracking."""
        raise NotImplementedError


class ModernDarkTheme(Theme):
    """Tema oscuro moderno profesional."""
    
    def __init__(self):
        super().__init__()
        self.name = "Modern Dark"
        self.colors = {
            "primary": (0, 212, 255),      # Cyan
            "secondary": (255, 64, 129),   # Pink
            "accent": (0, 255, 136),       # Green
            "warning": (0, 165, 255),      # Orange
            "error": (68, 68, 255),        # Red
            "bg": (30, 30, 46),            # Dark gray
            "text": (255, 255, 255),       # White
            "text_secondary": (176, 176, 176)  # Gray
        }
    
    def draw_cursor(self, frame, x, y, size="medium"):
        """Dibuja cursor moderno oscuro."""
        sizes = {"small": 15, "medium": 25, "large": 35, "gigantic": 50}
        radius = sizes.get(size, 25)
        
        # Outer ring
        cv2.circle(frame, (int(x), int(y)), radius, self.colors["primary"], 2)
        
        # Inner dot
        cv2.circle(frame, (int(x), int(y)), radius // 3, self.colors["primary"], -1)
        
        # Crosshair
        cv2.line(frame, (int(x) - radius, int(y)), (int(x) + radius, int(y)), 
                self.colors["primary"], 1)
        cv2.line(frame, (int(x), int(y) - radius), (int(x), int(y) + radius), 
                self.colors["primary"], 1)
    
    def draw_hud(self, frame, fps, detection_rate, hand_count=0):
        """Dibuja HUD profesional."""
        h, w = frame.shape[:2]
        
        # FPS en esquina superior derecha
        fps_text = f"FPS: {fps:.1f}"
        cv2.putText(frame, fps_text, (w - 150, 30),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, self.colors["primary"], 2)
        
        # Detection rate
        det_text = f"Detection: {detection_rate:.1f}%"
        cv2.putText(frame, det_text, (w - 220, 60),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, self.colors["accent"], 2)
        
        # Hand count
        hand_text = f"Hands: {hand_count}"
        cv2.putText(frame, hand_text, (w - 150, 90),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, self.colors["secondary"], 2)
        
        # Bottom banner
        banner_height = 40
        overlay = frame.copy()
        cv2.rectangle(overlay, (0, h - banner_height), (w, h),
                     self.colors["bg"], -1)
        cv2.addWeighted(overlay, 0.3, frame, 0.7, 0, frame)
        
        cv2.line(frame, (0, h - banner_height), (w, h - banner_height),
                self.colors["primary"], 2)
        
        info = "🎯 Air Touch Interface v3.5 | Press 'q' to quit"
        cv2.putText(frame, info, (10, h - 10),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.5, self.colors["text"], 1)
    
    def draw_tracking_overlay(self, frame, hands):
        """Dibuja líneas de tracking."""
        for hand in hands:
            landmarks = hand.get("landmarks", [])
            
            # Dibujar esqueleto de mano
            connections = [
                (0, 1), (1, 2), (2, 3), (3, 4),      # Thumb
                (0, 5), (5, 6), (6, 7), (7, 8),      # Index
                (5, 9), (9, 10), (10, 11), (11, 12), # Middle
                (9, 13), (13, 14), (14, 15), (15, 16), # Ring
                (13, 17), (17, 18), (18, 19), (19, 20) # Pinky
            ]
            
            for start, end in connections:
                if start < len(landmarks) and end < len(landmarks):
                    p1 = landmarks[start]
                    p2 = landmarks[end]
                    cv2.line(frame, (int(p1[0]), int(p1[1])), 
                            (int(p2[0]), int(p2[1])),
                            self.colors["primary"], 1)
            
            # Dibujar puntos
            for landmark in landmarks[:5]:  # Solo primeros 5 puntos
                cv2.circle(frame, (int(landmark[0]), int(landmark[1])), 3,
                          self.colors["accent"], -1)


class NeonFuturisticTheme(Theme):
    """Tema futurista neon con efectos sci-fi."""
    
    def __init__(self):
        super().__init__()
        self.name = "Neon Futuristic"
        self.colors = {
            "primary": (0, 255, 255),      # Cyan brillante
            "secondary": (255, 0, 255),    # Magenta
            "accent": (0, 255, 0),         # Verde neon
            "warning": (0, 165, 255),      # Orange
            "error": (0, 0, 255),          # Red
            "bg": (0, 0, 0),               # Negro puro
            "text": (0, 255, 255),         # Cyan
        }
    
    def draw_cursor(self, frame, x, y, size="medium"):
        """Dibuja cursor neon futurista."""
        sizes = {"small": 12, "medium": 22, "large": 32, "gigantic": 45}
        radius = sizes.get(size, 22)
        
        # Glow effect (multiple circles)
        for i in range(3, 0, -1):
            alpha = 0.1 * i
            overlay = frame.copy()
            cv2.circle(overlay, (int(x), int(y)), radius + i*3, 
                      self.colors["primary"], 1)
            cv2.addWeighted(overlay, alpha, frame, 1 - alpha, 0, frame)
        
        # Main cursor
        cv2.circle(frame, (int(x), int(y)), radius, self.colors["primary"], 2)
        cv2.circle(frame, (int(x), int(y)), radius // 4, self.colors["primary"], -1)
    
    def draw_hud(self, frame, fps, detection_rate, hand_count=0):
        """Dibuja HUD neon futurista."""
        h, w = frame.shape[:2]
        
        # Corners effect
        corner_size = 30
        cv2.line(frame, (0, 0), (corner_size, 0), self.colors["primary"], 2)
        cv2.line(frame, (0, 0), (0, corner_size), self.colors["primary"], 2)
        cv2.line(frame, (w-1, 0), (w-1-corner_size, 0), self.colors["primary"], 2)
        cv2.line(frame, (w-1, 0), (w-1, corner_size), self.colors["primary"], 2)
        
        # Text with glow
        fps_text = f">>> FPS: {fps:.1f} <<<"
        cv2.putText(frame, fps_text, (w - 200, 30),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, self.colors["secondary"], 2)
        
        det_text = f"[DETECTION: {detection_rate:.1f}%]"
        cv2.putText(frame, det_text, (w - 250, 60),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, self.colors["accent"], 2)


class MinimalTheme(Theme):
    """Tema minimalista limpio."""
    
    def __init__(self):
        super().__init__()
        self.name = "Minimal"
        self.colors = {
            "primary": (200, 200, 200),    # Gris claro
            "secondary": (100, 100, 100),  # Gris oscuro
            "accent": (50, 50, 50),        # Negro
            "bg": (255, 255, 255),         # Blanco
            "text": (0, 0, 0),             # Negro
        }
    
    def draw_cursor(self, frame, x, y, size="medium"):
        """Dibuja cursor minimalista."""
        sizes = {"small": 10, "medium": 18, "large": 28, "gigantic": 40}
        radius = sizes.get(size, 18)
        
        cv2.circle(frame, (int(x), int(y)), radius, self.colors["accent"], 1)
        cv2.circle(frame, (int(x), int(y)), 2, self.colors["accent"], -1)
    
    def draw_hud(self, frame, fps, detection_rate, hand_count=0):
        """Dibuja HUD minimalista."""
        h, w = frame.shape[:2]
        
        fps_text = f"FPS: {fps:.1f}"
        cv2.putText(frame, fps_text, (10, 30),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.5, self.colors["accent"], 1)


class SciiFiTheme(Theme):
    """Tema inspirado en ciencia ficción futurista."""
    
    def __init__(self):
        super().__init__()
        self.name = "Sci-Fi"
        self.colors = {
            "primary": (0, 255, 200),      # Cyan turquesa
            "secondary": (255, 100, 0),    # Orange
            "accent": (200, 50, 200),      # Purple
            "warning": (255, 200, 0),      # Yellow
            "error": (255, 50, 50),        # Red
            "bg": (20, 20, 40),            # Dark blue
            "text": (0, 255, 200),         # Cyan
        }
    
    def draw_cursor(self, frame, x, y, size="medium"):
        """Dibuja cursor sci-fi."""
        sizes = {"small": 14, "medium": 24, "large": 34, "gigantic": 48}
        radius = sizes.get(size, 24)
        
        # Rotating effect (simulated with static crosshair)
        cv2.circle(frame, (int(x), int(y)), radius, self.colors["primary"], 1)
        
        # Crosshair rotated
        angle = np.pi / 4
        for _ in range(2):
            dx1, dy1 = int(np.cos(angle) * radius), int(np.sin(angle) * radius)
            dx2, dy2 = int(np.cos(angle + np.pi) * radius), int(np.sin(angle + np.pi) * radius)
            cv2.line(frame, (int(x) + dx1, int(y) + dy1), 
                    (int(x) + dx2, int(y) + dy2), self.colors["accent"], 1)
            angle += np.pi / 2
        
        cv2.circle(frame, (int(x), int(y)), 3, self.colors["primary"], -1)


class ThemeManager:
    """Administra temas disponibles."""
    
    THEMES = {
        ThemeType.MODERN_DARK.value: ModernDarkTheme,
        ThemeType.MODERN_LIGHT.value: ModernDarkTheme,  # Can use similar
        ThemeType.NEON_FUTURISTIC.value: NeonFuturisticTheme,
        ThemeType.MINIMAL.value: MinimalTheme,
        ThemeType.SCI_FI.value: SciiFiTheme,
    }
    
    def __init__(self):
        self.current_theme = self.load_theme(ThemeType.MODERN_DARK.value)
    
    def load_theme(self, theme_name):
        """Carga un tema por nombre."""
        theme_class = self.THEMES.get(theme_name, ModernDarkTheme)
        self.current_theme = theme_class()
        return self.current_theme
    
    def get_theme(self):
        """Obtiene el tema actual."""
        return self.current_theme
    
    def list_available_themes(self):
        """Lista todos los temas disponibles."""
        return list(self.THEMES.keys())


# Instancia global
_theme_manager = None


def get_theme_manager():
    """Obtiene el administrador de temas global."""
    global _theme_manager
    if _theme_manager is None:
        _theme_manager = ThemeManager()
    return _theme_manager


def set_theme(theme_name):
    """Establece el tema actual."""
    manager = get_theme_manager()
    manager.load_theme(theme_name)
