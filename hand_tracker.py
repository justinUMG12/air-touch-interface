"""
Detector de manos usando MediaPipe.
Extrae landmarks, calcula la bounding box y genera un valor de profundidad
basado en el tamaño aparente de la mano (más grande = más cerca).
Optimizado para cámaras de baja calidad con preprocesamiento de imagen.
"""

import cv2
import mediapipe as mp
import numpy as np
from utils import distance

class HandTracker:
    def __init__(self, static_image_mode=False, max_num_hands=2,
                 min_detection_confidence=0.5, min_tracking_confidence=0.3):
        """
        Inicializa el detector de manos.
        Para cámaras de baja calidad se usan confianzas reducidas (0.5 y 0.3).
        """
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            static_image_mode=static_image_mode,
            max_num_hands=max_num_hands,
            min_detection_confidence=min_detection_confidence,
            min_tracking_confidence=min_tracking_confidence
        )
        self.mp_drawing = mp.solutions.drawing_utils
        self.mp_drawing_styles = mp.solutions.drawing_styles
        # Buffer para suavizar detecciones
        self.last_hands = []

    def preprocess_frame(self, frame):
        """
        Preprocesa el frame para mejorar detección en cámaras de baja calidad:
        - Mejora de contraste (CLAHE)
        - Reducción de ruido bilateral
        - Aumento de nitidez
        """
        # Convertir a HSV para procesamiento independiente de iluminación
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV).astype(np.float32)
        h, s, v = cv2.split(hsv)
        
        # CLAHE (Contrast Limited Adaptive Histogram Equalization) en V
        clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8, 8))
        v = clahe.apply(v.astype(np.uint8))
        
        # Aumentar saturación ligeramente para piel detectada mejor
        s = np.clip(s * 1.15, 0, 255)
        
        hsv_proc = cv2.merge([h, s, v])
        frame_enhanced = cv2.cvtColor(hsv_proc.astype(np.uint8), cv2.COLOR_HSV2BGR)
        
        # Reducción de ruido bilateral (preserva bordes)
        frame_denoised = cv2.bilateralFilter(frame_enhanced, 9, 75, 75)
        
        # Aumento ligero de nitidez
        kernel = np.array([[-0.5, -0.5, -0.5],
                          [-0.5,  5.0, -0.5],
                          [-0.5, -0.5, -0.5]]) / 1.5
        frame_sharpened = cv2.filter2D(frame_denoised, -1, kernel)
        
        # Asegurar valores válidos
        frame_sharpened = np.clip(frame_sharpened, 0, 255).astype(np.uint8)
        
        return frame_sharpened

    def process_frame(self, frame):
        """
        Procesa un frame BGR, devuelve la imagen con los dibujos y la lista de manos.
        Cada mano es un dict con:
            - landmarks: lista de (x,y,z) normalizados
            - handedness: "Left"/"Right"
            - bbox: (x_min, y_min, x_max, y_max) en píxeles
            - center: (cx, cy)
            - depth_proxy: valor de profundidad estimado (0-1, mayor = más cerca)
        """
        try:
            # Preprocesar frame para mejorar detección
            frame_processed = self.preprocess_frame(frame)
            frame_rgb = cv2.cvtColor(frame_processed, cv2.COLOR_BGR2RGB)
            
            results = self.hands.process(frame_rgb)
            hands_data = []

            if results.multi_hand_landmarks:
                for hand_landmarks, handedness in zip(results.multi_hand_landmarks,
                                                      results.multi_handedness):
                    h, w, _ = frame.shape
                    # Extraer coordenadas
                    landmarks = []
                    for lm in hand_landmarks.landmark:
                        landmarks.append((lm.x * w, lm.y * h, lm.z))
                    
                    # Calcular bounding box
                    xs = [lm[0] for lm in landmarks]
                    ys = [lm[1] for lm in landmarks]
                    x_min, x_max = min(xs), max(xs)
                    y_min, y_max = min(ys), max(ys)
                    
                    # Agregar padding al bbox
                    padding = 15
                    x_min = max(0, x_min - padding)
                    x_max = min(w, x_max + padding)
                    y_min = max(0, y_min - padding)
                    y_max = min(h, y_max + padding)
                    
                    bbox = (x_min, y_min, x_max, y_max)
                    center = ((x_min+x_max)/2, (y_min+y_max)/2)

                    # Profundidad proxy
                    box_w = x_max - x_min
                    box_h = y_max - y_min
                    diagonal = np.sqrt(box_w**2 + box_h**2)
                    frame_diag = np.sqrt(w**2 + h**2)
                    depth_proxy = min(diagonal / frame_diag, 1.0)

                    hand_info = {
                        "landmarks": landmarks,
                        "handedness": handedness.classification[0].label,
                        "bbox": bbox,
                        "center": center,
                        "depth_proxy": depth_proxy
                    }
                    hands_data.append(hand_info)

                    # Dibujar landmarks con líneas más gruesas
                    self.mp_drawing.draw_landmarks(
                        frame,
                        hand_landmarks,
                        self.mp_hands.HAND_CONNECTIONS,
                        self.mp_drawing_styles.get_default_hand_landmarks_style(),
                        self.mp_drawing_styles.get_default_hand_connections_style()
                    )
                    
                    # Dibujar bounding box más visible
                    cv2.rectangle(frame, (int(x_min), int(y_min)), 
                                (int(x_max), int(y_max)), (0, 255, 0), 3)
                    # Dibujar centro
                    cv2.circle(frame, (int(center[0]), int(center[1])), 8, (255, 0, 0), -1)

                self.last_hands = hands_data
            else:
                # Mantener últimas manos detectadas brevemente para suavizado
                hands_data = self.last_hands

            return frame, hands_data

        except Exception as e:
            print(f"Error en hand_tracker: {e}")
            return frame, []