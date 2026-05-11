"""
Control del cursor usando PyAutoGUI.
Implementa movimiento suave con suavizado exponencial,
mapeo de coordenadas y acciones de clic, arrastre y scroll.
"""

import pyautogui
import math
import time

# Desactivar el fallo de seguridad de PyAutoGUI (esquina superior izquierda)
pyautogui.FAILSAFE = False

class CursorController:
    def __init__(self, config):
        self.sensitivity = config["cursor"]["sensitivity"]
        self.smoothing_factor = config["cursor"]["smoothing_factor"]
        self.move_threshold = config["cursor"]["move_threshold_pixels"]
        self.border_margin = config["cursor"]["border_margin"]
        self.screen_width, self.screen_height = pyautogui.size()
        # Valores suavizados actuales (posición en pantalla)
        self.smooth_x = self.screen_width // 2
        self.smooth_y = self.screen_height // 2
        # Última posición objetivo sin suavizar
        self.target_x = self.smooth_x
        self.target_y = self.smooth_y
        # Estado de botones
        self.left_pressed = False
        self.right_pressed = False
        # Scroll acumulado
        self.scroll_accum = 0.0

    def map_to_screen(self, finger_x, finger_y, frame_width, frame_height):
        """
        Convierte coordenadas normalizadas de la mano (en píxeles de la cámara)
        a coordenadas de pantalla.
        """
        # Invertir horizontalmente para movimiento natural como espejo
        norm_x = 1.0 - (finger_x / frame_width)
        norm_y = finger_y / frame_height
        # Aplicar sensibilidad (estilo aceleración)
        # Transformación: centro de la cámara -> centro de pantalla
        cx, cy = 0.5, 0.5
        dx = (norm_x - cx) * self.sensitivity
        dy = (norm_y - cy) * self.sensitivity
        screen_x = (cx + dx) * self.screen_width
        screen_y = (cy + dy) * self.screen_height
        # Limitar bordes
        screen_x = max(self.border_margin, min(self.screen_width - self.border_margin, screen_x))
        screen_y = max(self.border_margin, min(self.screen_height - self.border_margin, screen_y))
        return screen_x, screen_y

    def update_cursor(self, finger_tip, frame_shape, gesture_state):
        """
        Actualiza la posición del cursor basado en el dedo índice.
        finger_tip: (x, y) en píxeles del frame.
        frame_shape: (height, width)
        gesture_state: cadena con el estado actual ('MOVE', 'DRAG', etc.)
                      Solo movemos si no estamos en SCROLL.
        """
        if gesture_state == "SCROLL":
            return  # No mover cursor durante scroll

        if finger_tip is None:
            return

        frame_height, frame_width = frame_shape[:2]
        target_x, target_y = self.map_to_screen(finger_tip[0], finger_tip[1], frame_width, frame_height)

        # Suavizado exponencial
        self.smooth_x += (target_x - self.smooth_x) * (1.0 - self.smoothing_factor)
        self.smooth_y += (target_y - self.smooth_y) * (1.0 - self.smoothing_factor)

        # Si el movimiento es mayor que el umbral, mover el cursor
        dx = self.smooth_x - pyautogui.position().x
        dy = self.smooth_y - pyautogui.position().y
        if math.sqrt(dx**2 + dy**2) > self.move_threshold:
            pyautogui.moveTo(self.smooth_x, self.smooth_y, duration=0.0)

    def perform_left_click(self):
        """Ejecuta un clic izquierdo."""
        pyautogui.click(button='left')

    def perform_double_click(self):
        """Ejecuta doble clic izquierdo."""
        pyautogui.doubleClick(button='left')

    def perform_right_click(self):
        """Ejecuta clic derecho."""
        pyautogui.click(button='right')

    def start_drag(self):
        """Presiona el botón izquierdo (inicio de arrastre)."""
        if not self.left_pressed:
            pyautogui.mouseDown(button='left')
            self.left_pressed = True

    def stop_drag(self):
        """Libera el botón izquierdo (fin de arrastre)."""
        if self.left_pressed:
            pyautogui.mouseUp(button='left')
            self.left_pressed = False

    def scroll(self, amount):
        """
        Realiza scroll vertical suave acumulando desplazamientos.
        amount: positivo -> scroll up (contenido baja), negativo -> scroll down.
        """
        self.scroll_accum += amount
        scroll_units = int(self.scroll_accum)
        if scroll_units != 0:
            pyautogui.scroll(scroll_units)
            self.scroll_accum -= scroll_units