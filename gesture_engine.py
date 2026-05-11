"""
Motor de reconocimiento de gestos y estados:
- MOVE: movimiento normal del cursor.
- TOUCH: el dedo ha entrado en la zona de presión (empuje hacia adelante).
- CLICK: se completa un clic.
- DRAG: se mantiene la presión y se mueve.
- SCROLL: dos dedos deslizándose verticalmente.
"""

import time
import math
from collections import deque
from utils import distance, play_sound

class GestureEngine:
    def __init__(self, config):
        self.config = config
        # Profundidad suavizada de la mano principal
        self.smooth_depth = 0.0
        self.depth_buffer = deque(maxlen=5)

        # Parámetros de toque
        self.touch_threshold = config["touch"]["touch_depth_threshold"]
        self.release_hysteresis = config["touch"]["release_hysteresis"]
        self.tap_fast_ms = config["touch"]["tap_fast_time_ms"] / 1000.0
        self.hold_ms = config["touch"]["hold_time_ms"] / 1000.0
        self.double_tap_ms = config["touch"]["double_tap_interval_ms"] / 1000.0
        self.cooldown_ms = config["touch"]["cooldown_ms"] / 1000.0

        # Máquina de estados
        self.state = "MOVE"   # MOVE, TOUCH_DOWN, DRAG, SCROLL
        self.last_state = "MOVE"
        self.entry_time = None         # Momento en que se entró en zona de toque
        self.tap_triggered = False     # Si ya se lanzó el clic en esta entrada
        self.last_tap_time = 0         # Último instante en que se completó un clic
        self.double_tap_pending = False # Para detectar segundo toque

        # Para scroll
        self.scroll_active = False
        self.prev_scroll_y = None
        self.scroll_sensitivity = config["scroll"]["sensitivity"]
        self.scroll_delta_thresh = config["scroll"]["delta_threshold"]

        # Modo clic derecho
        self.right_click_mode = config["right_click"]["mode"]
        self.secondary_hand = config["right_click"]["secondary_hand"]

        # Sonidos
        self.sound_enabled = config["audio"]["enabled"]

    def update(self, hands, frame_shape):
        """
        Recibe la lista de manos detectadas y el tamaño del frame.
        Retorna una acción: dict con tipo y datos, o None.
        Tipos de acciones:
            {"type": "MOVE"}
            {"type": "CLICK", "button": "left"|"right"}
            {"type": "DOUBLE_CLICK"}
            {"type": "DRAG_START"}
            {"type": "DRAG_END"}
            {"type": "SCROLL", "amount": float}
        Además actualiza self.state para el cursor controller.
        """
        if not hands:
            self._reset_states()
            return None

        # Seleccionar mano dominante (por defecto derecha, usar la primera derecha detectada)
        main_hand = None
        secondary_hand = None
        for hand in hands:
            if hand["handedness"] == "Right":
                main_hand = hand
            else:
                secondary_hand = hand
        # Si no hay derecha, usar la izquierda como principal
        if main_hand is None and secondary_hand is not None:
            main_hand = secondary_hand
            secondary_hand = None  # No hay mano secundaria real

        if main_hand is None:
            return None

        # Profundidad suavizada de la mano principal
        raw_depth = main_hand["depth_proxy"]
        self.depth_buffer.append(raw_depth)
        self.smooth_depth = sum(self.depth_buffer) / len(self.depth_buffer)

        # Obtener punta del índice (landmark 8)
        index_tip = main_hand["landmarks"][8]
        # Punta del medio (landmark 12)
        middle_tip = main_hand["landmarks"][12] if len(main_hand["landmarks"]) > 12 else None

        # Detección de gestos según estado actual
        action = None

        # --- Lógica principal de toque y arrastre ---
        is_touching = self.smooth_depth > self.touch_threshold

        if is_touching and self.state in ("MOVE", "SCROLL"):
            # Acaba de entrar en la zona de toque
            self.state = "TOUCH_DOWN"
            self.entry_time = time.time()
            self.tap_triggered = False
            # Verificar rapidez de la entrada (diferencia de profundidad reciente)
            if len(self.depth_buffer) >= 3:
                recent_change = self.depth_buffer[-1] - self.depth_buffer[-3]
                # Umbral de velocidad: si la profundidad aumentó rápidamente
                if recent_change > 0.02:  # Ajustar según sensibilidad
                    self.tap_triggered = True
                    # Verificar doble toque
                    now = time.time()
                    if now - self.last_tap_time < self.double_tap_ms:
                        action = {"type": "DOUBLE_CLICK"}
                        self._play_click()
                        self.last_tap_time = 0  # reset para no repetir
                    else:
                        # Programar clic simple (se ejecutará al soltar o con cooldown)
                        self.last_tap_time = now
                        self.double_tap_pending = True  # Aún no lanzamos el clic hasta soltar
                else:
                    # Entrada lenta, posible arrastre
                    pass
            # Si no se detectó como rápido, se considerará arrastre después de hold_ms

        elif is_touching and self.state == "TOUCH_DOWN":
            # Permanece en la zona de toque
            if not self.tap_triggered and (time.time() - self.entry_time) > self.hold_ms:
                # Pasó el tiempo, iniciar arrastre
                self.state = "DRAG"
                action = {"type": "DRAG_START"}
                self._play_click()

        elif not is_touching and self.state in ("TOUCH_DOWN", "DRAG"):
            # Salió de la zona de toque
            if self.state == "TOUCH_DOWN" and self.tap_triggered:
                # Era un toque rápido normal, ahora soltó -> clic
                if self.double_tap_pending:
                    action = {"type": "CLICK", "button": "left"}
                    self._play_click()
                    self.double_tap_pending = False
            elif self.state == "DRAG":
                action = {"type": "DRAG_END"}
            self.state = "MOVE"
            self.entry_time = None
            self.tap_triggered = False

        # Cooldown para evitar múltiples toques accidentales
        if action and action["type"] in ("CLICK", "DOUBLE_CLICK"):
            if time.time() - self.last_tap_time < self.cooldown_ms:
                action = None  # Suprimir

        # --- Clic derecho (dos dedos) ---
        if self.right_click_mode == "two_fingers" and middle_tip is not None:
            # Detectar si ambos dedos (índice y medio) están en zona de toque al mismo tiempo
            # Usamos profundidad promedio de ambos, o simplemente que estén extendidos y en zona
            if is_touching and self._finger_extended(main_hand, 12):
                # Si no está ya en proceso de clic derecho
                if not hasattr(self, "_right_click_armed"):
                    self._right_click_armed = True
                    self._right_click_time = time.time()
                elif self._right_click_armed and (time.time() - self._right_click_time) > 0.1:
                    action = {"type": "CLICK", "button": "right"}
                    self._play_click()
                    self._right_click_armed = False
            else:
                self._right_click_armed = False

        # --- Scroll con dos dedos ---
        if self.config["scroll"]["enabled"] and middle_tip is not None and not is_touching:
            # Scroll si ambos dedos están extendidos
            if self._finger_extended(main_hand, 8) and self._finger_extended(main_hand, 12):
                # Usar la posición Y del dedo índice
                curr_y = index_tip[1]
                if self.prev_scroll_y is not None and not self.scroll_active:
                    # Iniciar scroll si el desplazamiento supera el umbral
                    delta = self.prev_scroll_y - curr_y
                    if abs(delta) > self.scroll_delta_thresh:
                        self.scroll_active = True
                        self.state = "SCROLL"
                if self.scroll_active:
                    if self.prev_scroll_y is not None:
                        delta = self.prev_scroll_y - curr_y
                        # Suavizar y escalar
                        amount = delta * self.scroll_sensitivity / 100.0
                        action = {"type": "SCROLL", "amount": amount}
                    self.prev_scroll_y = curr_y
                else:
                    self.prev_scroll_y = curr_y
            else:
                self.scroll_active = False
                self.prev_scroll_y = None
                if self.state == "SCROLL":
                    self.state = "MOVE"
        else:
            self.scroll_active = False
            self.prev_scroll_y = None
            if self.state == "SCROLL":
                self.state = "MOVE"

        # Actualizar last_state
        self.last_state = self.state

        # Acción por defecto: MOVE
        if action is None:
            action = {"type": "MOVE"}

        return action

    def _finger_extended(self, hand, tip_id):
        """
        Determina si un dedo está extendido comparando la punta con la articulación PIP.
        Simplificado: si la punta está por encima de la PIP en Y (para dedos hacia arriba).
        """
        lm = hand["landmarks"]
        # Para índice (8) comparamos con PIP (6), para medio (12) con PIP (10)
        if tip_id == 8:   # índice
            tip = lm[8]
            pip = lm[6]
        elif tip_id == 12: # medio
            tip = lm[12]
            pip = lm[10]
        else:
            return False
        # Extendido si la punta está más arriba (menor Y) que PIP
        return tip[1] < pip[1]

    def _play_click(self):
        if self.sound_enabled:
            play_sound(frequency=1000, duration=50)

    def _reset_states(self):
        self.state = "MOVE"
        self.scroll_active = False
        self.prev_scroll_y = None