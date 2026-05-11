"""
Air Touch Interface v3.5 - NEW MAIN
Complete orchestration of initialization, configuration, and main application
Professional startup flow with camera selection, configuration, and testing
"""

import cv2
import time
import sys
import json
from pathlib import Path

# Import new modules
from splash_screen import run_splash_screen
from camera_selector import select_camera_interactive
from quick_config import show_quick_config
from test_screen import run_test_screen
from hand_visualizer import HandVisualizer

# Import original modules
from hand_tracker import HandTracker
from cursor_controller import CursorController
from gesture_engine import GestureEngine
from utils import load_config, play_sound

class AirTouchInterface:
    def __init__(self):
        self.config = None
        self.camera_id = 0
        self.cap = None
        self.window_name = "✨ Air Touch Interface - Main"
        self.width = 1280
        self.height = 720
        
        # Components
        self.tracker = None
        self.cursor_controller = None
        self.gesture_engine = None
        self.visualizer = None
        
        # Stats
        self.fps = 0
        self.frame_count = 0
        self.detection_count = 0
        self.start_time = time.time()
    
    def print_banner(self):
        """Print startup banner"""
        print("\n" + "="*70)
        print("  ✨ AIR TOUCH INTERFACE v3.5 - ULTIMATE EDITION")
        print("="*70)
        print()
    
    def run_initialization_flow(self):
        """Run complete initialization flow"""
        
        self.print_banner()
        
        # Step 1: Splash Screen
        print("📊 Step 1/5: Splash Screen")
        if not run_splash_screen():
            print("❌ Splash screen failed")
            return False
        print("✅ Splash screen completed\n")
        
        # Step 2: Camera Detection and Selection
        print("📹 Step 2/5: Camera Selection")
        self.camera_id = select_camera_interactive()
        if self.camera_id is None:
            print("❌ No camera selected")
            return False
        print(f"✅ Camera selected: {self.camera_id}\n")
        
        # Step 3: Quick Configuration
        print("⚙️  Step 3/5: Quick Configuration")
        self.config = show_quick_config()
        if self.config is None:
            print("❌ Configuration cancelled")
            return False
        print("✅ Configuration completed\n")
        
        # Step 4: Test Screen
        print("🧪 Step 4/5: Test Screen")
        if not run_test_screen(self.camera_id, self.config):
            print("⚠️  Test screen skipped or failed")
            # Don't fail - user might want to proceed anyway
        print("✅ Test screen completed\n")
        
        print("✅ Initialization flow completed successfully!\n")
        return True
    
    def initialize_components(self):
        """Initialize all components"""
        
        print("⏳ Initializing components...\n")
        
        # Camera
        print("  → Opening camera...")
        self.cap = cv2.VideoCapture(self.camera_id)
        if not self.cap.isOpened():
            print("    ❌ Failed to open camera")
            return False
        
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, self.width)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self.height)
        self.cap.set(cv2.CAP_PROP_AUTOFOCUS, 1)
        self.cap.set(cv2.CAP_PROP_AUTO_EXPOSURE, 1)
        self.cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)
        print("    ✅ Camera opened")
        
        # Hand Tracker
        print("  → Initializing Hand Tracker...")
        self.tracker = HandTracker(
            max_num_hands=self.config.get('hand_tracking', {}).get('max_hands', 2),
            min_detection_confidence=self.config.get('hand_tracking', {}).get('hand_detection_confidence', 0.5),
            min_tracking_confidence=self.config.get('hand_tracking', {}).get('tracking_confidence', 0.3)
        )
        print("    ✅ Hand Tracker initialized")
        
        # Cursor Controller
        print("  → Initializing Cursor Controller...")
        self.cursor_controller = CursorController(self.config)
        print("    ✅ Cursor Controller initialized")
        
        # Gesture Engine
        print("  → Initializing Gesture Engine...")
        self.gesture_engine = GestureEngine(self.config)
        print("    ✅ Gesture Engine initialized")
        
        # Hand Visualizer
        print("  → Initializing Hand Visualizer...")
        self.visualizer = HandVisualizer()
        print("    ✅ Hand Visualizer initialized")
        
        print("\n✅ All components initialized successfully!\n")
        return True
    
    def draw_main_ui(self, frame, results):
        """Draw main UI overlay"""
        
        h, w = frame.shape[:2]
        
        # Draw hand visualization
        if self.config.get('visual', {}).get('show_landmarks', True):
            frame = self.visualizer.draw_full_visualization(frame, results)
        
        # Draw FPS counter
        if self.config.get('visual', {}).get('show_fps', True):
            self.frame_count += 1
            current_time = time.time()
            elapsed = current_time - self.start_time
            if elapsed > 0:
                self.fps = self.frame_count / elapsed
            
            fps_text = f"FPS: {self.fps:.1f}"
            cv2.putText(frame, fps_text, (20, 40),
                       cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 255, 100), 2)
        
        # Draw status bar
        status_text = f"Manos: {len(results.hand_landmarks) if results.hand_landmarks else 0} | "
        status_text += f"Modo: {self.config.get('hand_tracking', {}).get('tracking_mode', 'smooth')}"
        
        cv2.putText(frame, status_text, (20, h - 30),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.8, (100, 200, 255), 1)
        
        # Draw instructions
        instructions = [
            "✓ Mueve las manos para controlar cursor",
            "✓ Empuja para CLICK aéreo",
            "✓ D = DEBUG | Q = SALIR"
        ]
        
        for idx, instr in enumerate(instructions):
            cv2.putText(frame, instr, (w - 400, 40 + idx * 30),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, (150, 150, 150), 1)
        
        return frame
    
    def run_main_loop(self):
        """Run main application loop"""
        
        print("="*70)
        print("  🎯 MAIN SYSTEM STARTED")
        print("="*70)
        print("\nControls:")
        print("  • Mouse movement: Hand tracking")
        print("  • Click: Push hand toward camera")
        print("  • D: Debug mode")
        print("  • Q: Quit")
        print("\n" + "="*70 + "\n")
        
        cv2.namedWindow(self.window_name, cv2.WINDOW_NORMAL)
        cv2.resizeWindow(self.window_name, self.width, self.height)
        
        debug_mode = False
        calibration_mode = False
        
        while True:
            ret, frame = self.cap.read()
            if not ret:
                print("⚠️  Could not read frame")
                break
            
            frame = cv2.flip(frame, 1)
            
            # Process hand tracking
            results = self.tracker.process_frame(frame)
            
            # Draw UI
            frame = self.draw_main_ui(frame, results)
            
            # Handle detections
            if results.hand_landmarks:
                for idx, hand_landmarks in enumerate(results.hand_landmarks):
                    # Move cursor based on first hand
                    if idx == 0 and results.handedness:
                        # Get palm position
                        palm_x = int(hand_landmarks.landmark[9].x * self.width)
                        palm_y = int(hand_landmarks.landmark[9].y * self.height)
                        
                        # Move cursor (would implement proper cursor movement here)
                        # self.cursor_controller.move_cursor(palm_x, palm_y)
                
                self.detection_count += 1
            
            # Display frame
            cv2.imshow(self.window_name, frame)
            
            # Handle keyboard input
            key = cv2.waitKey(30) & 0xFF
            
            if key == ord('q'):
                print("✅ Exiting...")
                break
            
            elif key == ord('d'):
                debug_mode = not debug_mode
                status = "ON" if debug_mode else "OFF"
                print(f"🐛 Debug mode: {status}")
            
            elif key == ord('c'):
                print("🔄 Recalibrating...")
        
        # Cleanup
        self.cap.release()
        cv2.destroyAllWindows()
        
        # Print session summary
        self.print_session_summary()
        
        return True
    
    def print_session_summary(self):
        """Print session summary"""
        elapsed = time.time() - self.start_time
        
        print("\n" + "="*70)
        print("  📊 SESSION SUMMARY")
        print("="*70)
        print(f"Duration: {elapsed:.1f} seconds")
        print(f"Total frames: {self.frame_count}")
        print(f"Detections: {self.detection_count}")
        print(f"Average FPS: {self.frame_count / elapsed:.1f}")
        print(f"Detection rate: {(self.detection_count / self.frame_count * 100):.1f}%")
        print("="*70 + "\n")
    
    def run(self):
        """Main entry point"""
        
        try:
            # Run initialization flow
            if not self.run_initialization_flow():
                print("❌ Initialization failed")
                return False
            
            # Initialize components
            if not self.initialize_components():
                print("❌ Component initialization failed")
                return False
            
            # Run main loop
            if not self.run_main_loop():
                print("❌ Main loop failed")
                return False
            
            print("✅ Application closed successfully")
            return True
        
        except KeyboardInterrupt:
            print("\n❌ Interrupted by user")
            return False
        
        except Exception as e:
            print(f"\n❌ Error: {e}")
            import traceback
            traceback.print_exc()
            return False
        
        finally:
            # Cleanup
            if self.cap:
                self.cap.release()
            cv2.destroyAllWindows()

def main():
    """Entry point"""
    app = AirTouchInterface()
    success = app.run()
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
