"""
Camera Selector Module
Detect available cameras and allow user selection
"""

import cv2
import numpy as np
from collections import defaultdict

class CameraSelector:
    def __init__(self):
        self.available_cameras = []
        self.selected_camera = 0
        self.window_name = "📹 Seleccionar Cámara"
        self.width = 1280
        self.height = 720
        
    def detect_cameras(self, max_devices=10):
        """Detect all available cameras"""
        self.available_cameras = []
        
        for device_id in range(max_devices):
            cap = cv2.VideoCapture(device_id, cv2.CAP_DSHOW)
            
            if cap.isOpened():
                # Try to read a frame to verify it works
                ret, frame = cap.read()
                if ret and frame is not None:
                    # Get camera info
                    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
                    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
                    fps = int(cap.get(cv2.CAP_PROP_FPS))
                    
                    camera_info = {
                        'id': device_id,
                        'name': f"Cámara {len(self.available_cameras) + 1}",
                        'resolution': f"{width}x{height}",
                        'fps': fps,
                        'frame': frame.copy()
                    }
                    
                    self.available_cameras.append(camera_info)
                    
                cap.release()
        
        return len(self.available_cameras)
    
    def show_camera_preview(self, camera_id):
        """Show live preview from selected camera"""
        cap = cv2.VideoCapture(camera_id, cv2.CAP_DSHOW)
        
        if not cap.isOpened():
            return None
        
        # Set resolution
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
        cap.set(cv2.CAP_PROP_AUTOFOCUS, 1)
        cap.set(cv2.CAP_PROP_AUTO_EXPOSURE, 1)
        cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)
        
        for _ in range(5):  # Skip first frames
            cap.read()
        
        ret, frame = cap.read()
        cap.release()
        
        if ret:
            return frame
        return None
    
    def run_selection_interface(self):
        """Run interactive camera selection interface"""
        
        num_cameras = self.detect_cameras()
        
        if num_cameras == 0:
            print("❌ No cameras detected")
            return None
        
        if num_cameras == 1:
            print(f"✅ Found 1 camera: {self.available_cameras[0]['name']}")
            return self.available_cameras[0]['id']
        
        # Multi-camera selection interface
        selected_index = 0
        cv2.namedWindow(self.window_name, cv2.WINDOW_NORMAL)
        cv2.resizeWindow(self.window_name, self.width, self.height)
        
        print(f"✅ Found {num_cameras} cameras")
        print("Use ← → arrows to switch cameras")
        print("Press ENTER to confirm")
        print("Press Q to cancel")
        
        while True:
            # Get preview from selected camera
            camera_id = self.available_cameras[selected_index]['id']
            preview = self.show_camera_preview(camera_id)
            
            if preview is None:
                print(f"⚠️  Could not get preview from camera {camera_id}")
                continue
            
            # Create display frame
            display = cv2.resize(preview, (self.width, self.height))
            
            # Add semi-transparent overlay
            overlay = display.copy()
            cv2.rectangle(overlay, (0, 0), (self.width, 150), (0, 0, 0), -1)
            cv2.rectangle(overlay, (0, self.height - 200), (self.width, self.height), (0, 0, 0), -1)
            
            alpha = 0.7
            display = cv2.addWeighted(overlay, alpha, display, 1 - alpha, 0)
            
            # Header
            header = f"Seleccionando Cámara ({selected_index + 1}/{num_cameras})"
            cv2.putText(display, header, 
                       (50, 50),
                       cv2.FONT_HERSHEY_DUPLEX, 1.5, (0, 255, 255), 2)
            
            camera_info = self.available_cameras[selected_index]
            cv2.putText(display, f"ID: {camera_info['id']}", 
                       (50, 90),
                       cv2.FONT_HERSHEY_SIMPLEX, 1.0, (100, 200, 255), 1)
            cv2.putText(display, f"Resolución: {camera_info['resolution']}", 
                       (50, 130),
                       cv2.FONT_HERSHEY_SIMPLEX, 1.0, (100, 200, 255), 1)
            
            # Instructions at bottom
            cv2.putText(display, "INSTRUCCIONES:", 
                       (50, self.height - 150),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 200, 150), 1)
            cv2.putText(display, "← → Cambiar cámara", 
                       (50, self.height - 110),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, (150, 150, 150), 1)
            cv2.putText(display, "ENTER Confirmar", 
                       (50, self.height - 70),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 100), 1)
            cv2.putText(display, "Q Cancelar", 
                       (50, self.height - 30),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 100, 255), 1)
            
            # Add green border to current selection
            cv2.rectangle(display, (10, 10), (self.width - 10, self.height - 10), 
                         (0, 255, 100), 3)
            
            cv2.imshow(self.window_name, display)
            
            # Wait for key press
            key = cv2.waitKey(100) & 0xFF
            
            if key == ord('q'):  # Quit
                cv2.destroyAllWindows()
                return None
            
            elif key == 13:  # Enter
                cv2.destroyAllWindows()
                return camera_id
            
            elif key == 83 or key == ord('d'):  # Right arrow or 'd'
                selected_index = (selected_index + 1) % num_cameras
            
            elif key == 81 or key == ord('a'):  # Left arrow or 'a'
                selected_index = (selected_index - 1) % num_cameras
        
        cv2.destroyAllWindows()
        return None
    
    def quick_test_camera(self, camera_id):
        """Quick test if camera works"""
        cap = cv2.VideoCapture(camera_id)
        
        if not cap.isOpened():
            return False
        
        # Try to read a few frames
        for _ in range(5):
            ret, frame = cap.read()
            if not ret:
                cap.release()
                return False
        
        cap.release()
        return True

def select_camera_interactive():
    """Run camera selection"""
    selector = CameraSelector()
    return selector.run_selection_interface()

if __name__ == "__main__":
    camera_id = select_camera_interactive()
    if camera_id is not None:
        print(f"✅ Selected camera: {camera_id}")
    else:
        print("❌ No camera selected")
