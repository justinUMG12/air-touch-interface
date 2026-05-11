"""
Test Screen Module
Interactive test screen to verify tracking and click before main system
"""

import cv2
import numpy as np
from hand_visualizer import HandVisualizer
from hand_tracker import HandTracker
import time

class TestScreen:
    def __init__(self, camera_id=0, config=None):
        self.camera_id = camera_id
        self.config = config or {}
        self.width = 1280
        self.height = 720
        self.window_name = "🧪 PANTALLA DE PRUEBA - Air Touch Interface"
        
        # Initialize visualizer
        self.visualizer = HandVisualizer()
        self.tracker = HandTracker(max_num_hands=2)
        
        # Test state
        self.click_test_active = False
        self.click_zones = []
        self.test_stage = 0  # 0: Intro, 1: Tracking test, 2: Click test
        
        # Performance tracking
        self.fps = 0
        self.frame_count = 0
        self.start_time = time.time()
        self.click_detections = 0
    
    def draw_test_instructions(self, frame, stage):
        """Draw test instructions"""
        h, w = frame.shape[:2]
        
        overlay = frame.copy()
        
        if stage == 0:
            # Intro stage
            cv2.rectangle(overlay, (w//2-300, h//2-150), (w//2+300, h//2+150), 
                         (10, 10, 30), -1)
            cv2.addWeighted(overlay, 0.8, frame, 0.2, 0, frame)
            
            cv2.putText(frame, "PANTALLA DE PRUEBA", 
                       (w//2-200, h//2-100),
                       cv2.FONT_HERSHEY_DUPLEX, 1.5, (0, 255, 255), 2)
            
            cv2.putText(frame, "Presiona ESPACIO para comenzar", 
                       (w//2-200, h//2-40),
                       cv2.FONT_HERSHEY_SIMPLEX, 1.0, (100, 200, 255), 1)
            
            cv2.putText(frame, "Q para cancelar", 
                       (w//2-150, h//2+20),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.8, (100, 100, 200), 1)
        
        elif stage == 1:
            # Tracking test
            cv2.rectangle(overlay, (20, 20), (w-20, 100), (10, 10, 30), -1)
            cv2.addWeighted(overlay, 0.8, frame, 0.2, 0, frame)
            
            cv2.putText(frame, "📍 PRUEBA DE TRACKING", 
                       (40, 60),
                       cv2.FONT_HERSHEY_DUPLEX, 1.2, (0, 255, 255), 2)
            
            cv2.putText(frame, "Mueve las manos frente a la cámara", 
                       (40, 640),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.9, (100, 200, 255), 1)
            
            cv2.putText(frame, "Presiona ESPACIO para siguiente", 
                       (40, 680),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 100), 1)
        
        elif stage == 2:
            # Click test
            cv2.rectangle(overlay, (20, 20), (w-20, 100), (10, 10, 30), -1)
            cv2.addWeighted(overlay, 0.8, frame, 0.2, 0, frame)
            
            cv2.putText(frame, "👆 PRUEBA DE CLICK", 
                       (40, 60),
                       cv2.FONT_HERSHEY_DUPLEX, 1.2, (0, 255, 255), 2)
            
            cv2.putText(frame, "Realiza clicks en los cuadrados (empuja hacia cámara)", 
                       (40, 640),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.9, (100, 200, 255), 1)
            
            cv2.putText(frame, "Presiona ESPACIO para continuar", 
                       (40, 680),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 100), 1)
        
        return frame
    
    def draw_click_zones(self, frame):
        """Draw clickable test zones"""
        h, w = frame.shape[:2]
        
        # Define zones
        zones = [
            {'x': 150, 'y': 200, 'size': 100, 'color': (0, 255, 255)},
            {'x': w//2 - 50, 'y': 200, 'size': 100, 'color': (255, 0, 255)},
            {'x': w - 200, 'y': 200, 'size': 100, 'color': (0, 200, 255)},
        ]
        
        for zone in zones:
            x, y = zone['x'], zone['y']
            size = zone['size']
            color = zone['color']
            
            # Draw square
            cv2.rectangle(frame, (x, y), (x + size, y + size), color, 3)
            
            # Draw center point
            cv2.circle(frame, (x + size//2, y + size//2), 5, color, -1)
        
        return frame, zones
    
    def draw_performance_stats(self, frame, num_hands=0):
        """Draw performance statistics"""
        self.frame_count += 1
        current_time = time.time()
        elapsed = current_time - self.start_time
        
        if elapsed > 0:
            self.fps = self.frame_count / elapsed
        
        # Draw stats
        stats = f"FPS: {self.fps:.1f} | Manos detectadas: {num_hands} | Clicks: {self.click_detections}"
        
        cv2.putText(frame, stats, 
                   (20, frame.shape[0] - 20),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 100), 1)
        
        return frame
    
    def run_test(self):
        """Run the test screen"""
        cap = cv2.VideoCapture(self.camera_id)
        
        if not cap.isOpened():
            print("❌ Could not open camera")
            return False
        
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, self.width)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self.height)
        cap.set(cv2.CAP_PROP_AUTOFOCUS, 1)
        cap.set(cv2.CAP_PROP_AUTO_EXPOSURE, 1)
        cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)
        
        cv2.namedWindow(self.window_name, cv2.WINDOW_NORMAL)
        cv2.resizeWindow(self.window_name, self.width, self.height)
        
        print("🧪 Test screen started")
        print("  ← Press SPACE to proceed between stages")
        print("  ← Press Q to cancel")
        
        stage = 0
        proceed = False
        test_complete = False
        
        while True:
            ret, frame = cap.read()
            if not ret:
                print("⚠️  Could not read frame")
                break
            
            frame = cv2.flip(frame, 1)
            
            # Process hand tracking
            results = self.visualizer.process_frame(frame)
            
            # Draw based on stage
            if stage == 0:
                # Intro stage
                frame = self.draw_test_instructions(frame, 0)
            
            elif stage == 1:
                # Tracking test - show hand visualization
                frame = self.visualizer.draw_full_visualization(frame, results)
                frame = self.draw_test_instructions(frame, 1)
                
                if results.hand_landmarks:
                    frame = self.draw_performance_stats(frame, len(results.hand_landmarks))
            
            elif stage == 2:
                # Click test
                frame = self.visualizer.draw_full_visualization(frame, results)
                frame, zones = self.draw_click_zones(frame)
                frame = self.draw_test_instructions(frame, 2)
                
                if results.hand_landmarks:
                    # Simulate click detection (would be integrated with cursor_controller)
                    frame = self.draw_performance_stats(frame, len(results.hand_landmarks))
                    
                    # Draw instruction for completing test
                    cv2.putText(frame, f"Click: {self.click_detections}/3", 
                               (20, 680),
                               cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 100), 1)
            
            cv2.imshow(self.window_name, frame)
            
            # Handle keyboard input
            key = cv2.waitKey(30) & 0xFF
            
            if key == ord('q'):
                print("❌ Test cancelled")
                cap.release()
                cv2.destroyAllWindows()
                return False
            
            elif key == 32:  # Space
                if stage < 2:
                    stage += 1
                    self.frame_count = 0
                    self.start_time = time.time()
                    print(f"✅ Moving to stage {stage + 1}")
                else:
                    # Test complete
                    test_complete = True
                    break
        
        cap.release()
        cv2.destroyAllWindows()
        
        if test_complete:
            print("✅ Test completed successfully!")
            return True
        return False

def run_test_screen(camera_id=0, config=None):
    """Run the test screen"""
    test = TestScreen(camera_id, config)
    return test.run_test()

if __name__ == "__main__":
    run_test_screen()
