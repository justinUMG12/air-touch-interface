"""
Enhanced Hand Tracker with Multi-Hand Support and Adaptive Detection
Supports automatic hand dominance detection, low-light mode, and precision tracking.
"""

import cv2
import mediapipe as mp
import numpy as np
from collections import deque


class EnhancedHandTracker:
    """Detector de manos mejorado con características avanzadas."""
    
    def __init__(self, config):
        self.mp_hands = mp.solutions.hands
        
        # Parámetros de detección
        hand_config = config.get("hand_tracking", {})
        self.dominant_hand = hand_config.get("dominant_hand", "auto")
        self.tracking_mode = hand_config.get("tracking_mode", "smooth")
        self.low_light_mode = hand_config.get("low_light_mode", False)
        self.precision_mode = hand_config.get("precision_mode", False)
        self.gaming_mode = hand_config.get("gaming_mode", False)
        
        # Confianzas de detección
        if self.low_light_mode:
            min_detection = 0.4
            min_tracking = 0.2
        elif self.precision_mode:
            min_detection = 0.7
            min_tracking = 0.5
        elif self.gaming_mode:
            min_detection = 0.4
            min_tracking = 0.2
        else:
            min_detection = config.get("hand_tracking", {}).get("hand_detection_confidence", 0.5)
            min_tracking = config.get("hand_tracking", {}).get("tracking_confidence", 0.3)
        
        self.hands = self.mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=config.get("hand_tracking", {}).get("max_hands", 2),
            min_detection_confidence=min_detection,
            min_tracking_confidence=min_tracking
        )
        
        # Buffers para suavizado
        self.depth_buffer = deque(maxlen=5)
        self.hand_history = deque(maxlen=3)
        
    def preprocess_frame(self, frame):
        """Preprocesa frame para mejor detección."""
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV).astype(np.float32)
        h, s, v = cv2.split(hsv)
        
        # CLAHE en V
        clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8, 8))
        v = clahe.apply(v.astype(np.uint8))
        
        # Ajustar saturación
        s = np.clip(s * 1.15, 0, 255)
        
        hsv_proc = cv2.merge([h, s, v])
        frame_enhanced = cv2.cvtColor(hsv_proc.astype(np.uint8), cv2.COLOR_HSV2BGR)
        
        # Denoise
        frame_denoised = cv2.bilateralFilter(frame_enhanced, 9, 75, 75)
        
        # Sharpening
        kernel = np.array([[-0.5, -0.5, -0.5],
                          [-0.5,  5.0, -0.5],
                          [-0.5, -0.5, -0.5]]) / 1.5
        frame_sharpened = cv2.filter2D(frame_denoised, -1, kernel)
        
        frame_sharpened = np.clip(frame_sharpened, 0, 255).astype(np.uint8)
        
        return frame_sharpened
    
    def process_frame(self, frame):
        """Procesa frame y detecta manos."""
        frame_processed = self.preprocess_frame(frame)
        frame_rgb = cv2.cvtColor(frame_processed, cv2.COLOR_BGR2RGB)
        
        results = self.hands.process(frame_rgb)
        hands_data = []
        
        if results.multi_hand_landmarks:
            h, w = frame.shape[:2]
            
            for hand_landmarks, handedness in zip(
                results.multi_hand_landmarks,
                results.multi_handedness
            ):
                # Extraer landmarks
                landmarks = []
                for lm in hand_landmarks.landmark:
                    landmarks.append((lm.x * w, lm.y * h, lm.z))
                
                # Calcular bounding box
                xs = [lm[0] for lm in landmarks]
                ys = [lm[1] for lm in landmarks]
                x_min, x_max = min(xs), max(xs)
                y_min, y_max = min(ys), max(ys)
                
                # Centro
                cx = (x_min + x_max) / 2
                cy = (y_min + y_max) / 2
                
                # Profundidad (basada en tamaño aparente)
                hand_size = (x_max - x_min) * (y_max - y_min)
                max_possible_size = w * h * 0.3  # 30% de pantalla máximo
                depth = min(hand_size / max_possible_size, 1.0)
                
                # Suavizar profundidad
                self.depth_buffer.append(depth)
                smooth_depth = sum(self.depth_buffer) / len(self.depth_buffer)
                
                hand_data = {
                    "landmarks": landmarks,
                    "handedness": handedness.classification[0].label,
                    "confidence": handedness.classification[0].score,
                    "bbox": (x_min, y_min, x_max, y_max),
                    "center": (cx, cy),
                    "depth_proxy": smooth_depth
                }
                
                hands_data.append(hand_data)
        
        # Aplicar filtro de dominancia
        hands_data = self.select_dominant_hand(hands_data)
        
        # Guardar en historial
        self.hand_history.append(hands_data)
        
        return frame, hands_data
    
    def select_dominant_hand(self, hands):
        """Selecciona mano(s) basado en configuración."""
        if len(hands) == 0:
            return hands
        
        if self.dominant_hand == "left":
            left_hands = [h for h in hands if h["handedness"] == "Left"]
            return left_hands if left_hands else hands[:1]
        
        elif self.dominant_hand == "right":
            right_hands = [h for h in hands if h["handedness"] == "Right"]
            return right_hands if right_hands else hands[:1]
        
        elif self.dominant_hand == "auto":
            # Preferir mano derecha, pero fallback a izquierda
            right_hands = [h for h in hands if h["handedness"] == "Right"]
            if right_hands:
                return [right_hands[0]] + [h for h in hands if h["handedness"] == "Left"]
            return hands
        
        return hands
    
    def get_dominant_hand(self, hands):
        """Obtiene la mano dominante para control."""
        if not hands:
            return None
        
        # Si hay configuración explícita
        if self.dominant_hand == "left":
            for hand in hands:
                if hand["handedness"] == "Left":
                    return hand
        elif self.dominant_hand == "right":
            for hand in hands:
                if hand["handedness"] == "Right":
                    return hand
        
        # Auto mode: primera mano detectada
        return hands[0] if hands else None
    
    def get_secondary_hand(self, hands):
        """Obtiene la mano secundaria (para scroll, etc)."""
        if len(hands) < 2:
            return None
        
        return hands[1]
    
    def enable_low_light_mode(self, enable=True):
        """Activa modo de baja luz."""
        self.low_light_mode = enable
    
    def enable_precision_mode(self, enable=True):
        """Activa modo precisión."""
        self.precision_mode = enable
    
    def enable_gaming_mode(self, enable=True):
        """Activa modo gaming."""
        self.gaming_mode = enable
    
    def set_dominant_hand(self, hand):
        """Establece mano dominante."""
        if hand in ["left", "right", "auto"]:
            self.dominant_hand = hand


class HandDetectionOptimizer:
    """Optimizador de detección de manos."""
    
    def __init__(self, logger=None):
        self.logger = logger
        self.failed_frames = 0
        self.total_frames = 0
        
    def analyze_tracking_quality(self, hands, frame_shape):
        """Analiza calidad del tracking."""
        quality = {
            "hands_detected": len(hands),
            "confidence": 0,
            "stability": "unknown"
        }
        
        if hands:
            avg_confidence = sum(h.get("confidence", 0) for h in hands) / len(hands)
            quality["confidence"] = avg_confidence
            
            if avg_confidence > 0.8:
                quality["stability"] = "excellent"
            elif avg_confidence > 0.6:
                quality["stability"] = "good"
            elif avg_confidence > 0.4:
                quality["stability"] = "fair"
            else:
                quality["stability"] = "poor"
        
        return quality
    
    def suggest_adjustments(self, quality):
        """Sugiere ajustes basado en calidad."""
        suggestions = []
        
        if quality["hands_detected"] == 0:
            suggestions.append("No hands detected - move closer or improve lighting")
        elif quality["confidence"] < 0.5:
            suggestions.append("Low detection confidence - improve lighting or adjust camera angle")
        
        return suggestions
