"""
Air Touch Interface - Control total del cursor con las manos.
Punto de entrada principal.
Optimizado para cámaras de baja calidad y interfaz amigable.
"""

import cv2
import time
import argparse
import sys
import numpy as np
from hand_tracker import HandTracker
from cursor_controller import CursorController
from gesture_engine import GestureEngine
from utils import load_config, draw_ui_overlay, play_sound

def main():
    try:
        # Banner de inicio
        print("\n" + "=" * 60)
        print("  🎯 AIR TOUCH INTERFACE v2.0")
        print("=" * 60)
        
        # Cargar configuración
        config = load_config("config.json")
        
        # Mostrar información de sesión
        last_adjustment = config.get("last_auto_adjustment", "Nunca")
        print(f"\n📅 Última calibración: {last_adjustment}")
        print(f"🔧 Modo detección: {'Alto' if config['performance']['detection_confidence'] >= 0.6 else 'Estándar' if config['performance']['detection_confidence'] >= 0.5 else 'Bajo'}")

        # Inicializar componentes
        print("\n⏳ Inicializando componentes...")
        print("  → Hand Tracker")
        tracker = HandTracker(
            max_num_hands=config.get("performance", {}).get("max_hands", 2),
            min_detection_confidence=config.get("performance", {}).get("detection_confidence", 0.5),
            min_tracking_confidence=config.get("performance", {}).get("tracking_confidence", 0.3)
        )
        
        print("  → Cursor Controller")
        cursor = CursorController(config)
        
        print("  → Gesture Engine")
        gesture = GestureEngine(config)

        # Cámara
        print("  → Cámara")
        cap = cv2.VideoCapture(config["camera"]["device_id"])
        
        # Configurar cámara para mejor rendimiento
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, config["camera"]["frame_width"])
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, config["camera"]["frame_height"])
        cap.set(cv2.CAP_PROP_FPS, config["camera"]["fps_target"])
        cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)  # Minimizar buffer para latencia baja
        
        # Mejorar autofoco si está disponible
        cap.set(cv2.CAP_PROP_AUTOFOCUS, 1)
        cap.set(cv2.CAP_PROP_AUTO_EXPOSURE, 1)

        if not cap.isOpened():
            print("❌ Error: No se pudo abrir la cámara.")
            sys.exit(1)

        print("✅ Todos los componentes inicializados")
        print("\n" + "=" * 60)

        # Variables de tiempo para FPS
        prev_time = time.time()
        fps = 0
        frame_count = 0
        detection_count = 0


        print("📋 INSTRUCCIONES:")
        print("=" * 60)
        print("  • Mueve la mano para mover el cursor")
        print("  • Empuja hacia la cámara para CLICK")
        print("  • Dos manos: SCROLL vertical")
        print("  • Presiona 'q' para SALIR")
        print("  • Presiona 'd' para DEBUG")
        print("  • Presiona 'c' para CALIBRACIÓN")
        print("=" * 60 + "\n")

        calibration_mode = False
        display_calibration = False
        calibration_timer = 0

        while True:
            ret, frame = cap.read()
            if not ret:
                print("⚠️  Frame no capturado.")
                break

            frame_count += 1

            # Flip horizontal si está configurado
            if config["camera"]["flip_horizontal"]:
                frame = cv2.flip(frame, 1)

            # Procesar manos
            processed_frame, hands = tracker.process_frame(frame)
            
            if hands:
                detection_count += 1

            # Modo calibración
            if calibration_mode:
                display_calibration = True
                calibration_timer = 10
            
            if display_calibration:
                cv2.putText(processed_frame, "CALIBRACION: Mueve tus manos en el frame", 
                           (20, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)
                calibration_timer -= 1
                if calibration_timer <= 0:
                    display_calibration = False
                    calibration_mode = False

            # Obtener acción del motor de gestos
            action = gesture.update(hands, processed_frame.shape)

            # Aplicar acciones al cursor
            if action:
                action_type = action["type"]
                # Para movimiento necesitamos la punta del índice de la mano principal
                main_hand = None
                for hand in hands:
                    if hand["handedness"] == "Right":
                        main_hand = hand
                        break
                if main_hand is None and hands:
                    main_hand = hands[0]

                finger_tip = None
                if main_hand:
                    finger_tip = main_hand["landmarks"][8][:2]  # solo x,y

                # Ejecutar acción
                if action_type == "MOVE":
                    cursor.update_cursor(finger_tip, processed_frame.shape, gesture.state)
                elif action_type == "CLICK":
                    if action["button"] == "left":
                        cursor.perform_left_click()
                        play_sound(config["audio"]["click_sound"])
                    elif action["button"] == "right":
                        cursor.perform_right_click()
                        play_sound(config["audio"]["click_sound"])
                elif action_type == "DOUBLE_CLICK":
                    cursor.perform_double_click()
                    play_sound(config["audio"]["click_sound"])
                elif action_type == "DRAG_START":
                    cursor.start_drag()
                elif action_type == "DRAG_END":
                    cursor.stop_drag()
                elif action_type == "SCROLL":
                    cursor.scroll(action["amount"])

            # Dibujar overlay
            is_touching = gesture.smooth_depth > config["touch"]["touch_depth_threshold"]
            draw_ui_overlay(processed_frame, gesture.state, fps,
                           gesture.smooth_depth, is_touching, config, hands)

            # FPS
            curr_time = time.time()
            fps = 1.0 / (curr_time - prev_time + 1e-6)
            prev_time = curr_time

            # Mostrar ventana
            cv2.imshow("Air Touch Interface", processed_frame)

            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                print("\n👋 Cerrando aplicación...")
                break
            elif key == ord('d'):
                config["debug"]["show_depth_graph"] = not config["debug"]["show_depth_graph"]
                state = "ON" if config["debug"]["show_depth_graph"] else "OFF"
                print(f"🔧 Debug: {state}")
            elif key == ord('c'):
                calibration_mode = True
                print("📏 Modo de calibración activado")

        # Estadísticas finales
        detection_rate = (detection_count / max(frame_count, 1)) * 100 if frame_count > 0 else 0
        print(f"\n📊 Estadísticas finales:")
        print(f"  • Frames procesados: {frame_count}")
        print(f"  • Detecciones de mano: {detection_count}")
        print(f"  • Tasa de detección: {detection_rate:.1f}%")
        print(f"  • FPS promedio: {fps:.1f}")

        cap.release()
        cv2.destroyAllWindows()
        cursor.stop_drag()
        print("✅ Aplicación cerrada correctamente.")

    except Exception as e:
        print(f"❌ Error crítico: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()