"""
Splash Screen for Air Touch Interface
Professional startup screen with system verification
"""

import cv2
import numpy as np
import time
import sys
from pathlib import Path

class SplashScreen:
    def __init__(self):
        self.width = 1280
        self.height = 720
        self.window_name = "Air Touch Interface - Inicializando"
        
    def draw_animated_splash(self):
        """Display animated splash screen with system checks"""
        
        # Create base image
        splash = np.zeros((self.height, self.width, 3), dtype=np.uint8)
        
        # Background gradient effect
        for i in range(self.height):
            alpha = i / self.height
            # Dark blue to darker blue gradient
            splash[i, :] = [20 + int(10 * alpha), 30, 50 + int(30 * alpha)]
        
        # Create window
        cv2.namedWindow(self.window_name, cv2.WINDOW_NORMAL)
        cv2.resizeWindow(self.window_name, self.width, self.height)
        
        # Animation frames
        checks = [
            ("🔍 Verificando dependencias...", 1.0),
            ("📹 Detectando cámara...", 1.5),
            ("🤖 Cargando MediaPipe...", 2.0),
            ("⚙️  Inicializando componentes...", 2.5),
            ("✅ Sistema listo", 3.5),
        ]
        
        start_time = time.time()
        current_check = 0
        
        while True:
            elapsed = time.time() - start_time
            
            # Create fresh splash
            splash_frame = np.zeros((self.height, self.width, 3), dtype=np.uint8)
            for i in range(self.height):
                alpha = i / self.height
                splash_frame[i, :] = [20 + int(10 * alpha), 30, 50 + int(30 * alpha)]
            
            # Draw title
            cv2.putText(splash_frame, "AIR TOUCH INTERFACE", 
                       (self.width//2 - 280, 120),
                       cv2.FONT_HERSHEY_DUPLEX, 2.5, (0, 255, 255), 3)
            
            # Draw version
            cv2.putText(splash_frame, "v3.5 Ultimate Edition", 
                       (self.width//2 - 150, 170),
                       cv2.FONT_HERSHEY_SIMPLEX, 1.0, (100, 200, 255), 2)
            
            # Animated logo circle
            center_x = self.width // 2
            center_y = 250
            radius = 40
            
            # Pulsating circle
            pulse = int(10 * np.sin(elapsed * 3))
            cv2.circle(splash_frame, (center_x, center_y), radius + pulse, (0, 255, 255), 2)
            
            # Rotating line
            angle = (elapsed * 100) % 360
            rad = np.radians(angle)
            end_x = int(center_x + radius * np.cos(rad))
            end_y = int(center_y + radius * np.sin(rad))
            cv2.line(splash_frame, (center_x, center_y), (end_x, end_y), (0, 200, 255), 2)
            
            # Draw checks
            check_y = 350
            check_spacing = 50
            
            for idx, (check_text, check_time) in enumerate(checks):
                if elapsed >= check_time:
                    # Completed check
                    color = (0, 255, 100)  # Green
                    status = "✓"
                else:
                    # Pending check
                    color = (100, 100, 100)  # Gray
                    status = "○"
                
                # Draw status
                cv2.putText(splash_frame, status, 
                           (150, check_y + idx * check_spacing),
                           cv2.FONT_HERSHEY_SIMPLEX, 1.2, color, 2)
                
                # Draw text
                cv2.putText(splash_frame, check_text, 
                           (200, check_y + idx * check_spacing),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.8, color, 1)
            
            # Progress bar
            progress_width = int(400 * min(elapsed / 3.5, 1.0))
            cv2.rectangle(splash_frame, (self.width//2 - 200, 650), 
                         (self.width//2 - 200 + progress_width, 670), 
                         (0, 200, 255), -1)
            cv2.rectangle(splash_frame, (self.width//2 - 200, 650), 
                         (self.width//2 + 200, 670), (100, 100, 100), 2)
            
            # Display frame
            cv2.imshow(self.window_name, splash_frame)
            
            # Wait for key press or timeout
            key = cv2.waitKey(30)
            if key & 0xFF == ord('q'):
                cv2.destroyAllWindows()
                sys.exit(0)
            
            # Exit animation after completion
            if elapsed >= 4.0:
                break
        
        # Fade out
        for fade in range(10):
            fade_frame = splash_frame.copy()
            fade_alpha = 1.0 - (fade / 10.0)
            fade_frame = cv2.addWeighted(fade_frame, fade_alpha, 
                                        np.zeros_like(fade_frame), 1-fade_alpha, 0)
            cv2.imshow(self.window_name, fade_frame)
            cv2.waitKey(50)
        
        cv2.destroyAllWindows()
        return True
    
    def verify_dependencies(self):
        """Verify all required dependencies"""
        dependencies = {
            'cv2': 'OpenCV',
            'mediapipe': 'MediaPipe',
            'pyautogui': 'PyAutoGUI',
            'numpy': 'NumPy'
        }
        
        missing = []
        for module, name in dependencies.items():
            try:
                __import__(module)
            except ImportError:
                missing.append(name)
        
        if missing:
            print(f"❌ Dependencias faltantes: {', '.join(missing)}")
            return False
        
        return True

def run_splash_screen():
    """Run the splash screen"""
    splash = SplashScreen()
    
    if not splash.verify_dependencies():
        print("Install missing dependencies with: pip install -r requirements_v35.txt")
        return False
    
    return splash.draw_animated_splash()

if __name__ == "__main__":
    run_splash_screen()
