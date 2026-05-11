"""
Hand Visualizer Module
Professional visualization of MediaPipe hand landmarks with tracking overlay
"""

import cv2
import numpy as np
import mediapipe as mp

class HandVisualizer:
    def __init__(self):
        self.mp_hands = mp.solutions.hands
        self.mp_drawing = mp.solutions.drawing_utils
        self.hands = self.mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=2,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.3
        )
        
        # Color scheme - Cyberpunk Neon
        self.colors = {
            'landmarks': (0, 255, 255),      # Cyan
            'connections': (255, 0, 255),     # Magenta
            'joints': (0, 200, 255),          # Light Cyan
            'palm': (255, 100, 0),            # Orange
            'active': (0, 255, 100),          # Green (when clicking)
            'text': (0, 255, 255),            # Cyan
            'background': (20, 20, 40)        # Dark blue
        }
    
    def draw_hand_landmarks_modern(self, frame, hand_landmarks, handedness, hand_index=0):
        """Draw hand landmarks with modern futuristic style"""
        
        h, w, c = frame.shape
        
        # Convert landmarks to pixel coordinates
        landmarks_xy = []
        for landmark in hand_landmarks.landmark:
            x = int(landmark.x * w)
            y = int(landmark.y * h)
            z = landmark.z
            confidence = landmark.z
            landmarks_xy.append((x, y, z, confidence))
        
        # Draw palm base circle
        if len(landmarks_xy) >= 1:
            palm_x, palm_y = landmarks_xy[0][:2]
            cv2.circle(frame, (palm_x, palm_y), 15, self.colors['palm'], -1)
            cv2.circle(frame, (palm_x, palm_y), 15, self.colors['landmarks'], 2)
        
        # Draw connections between joints (bones)
        connections = [
            (0, 1), (1, 2), (2, 3), (3, 4),      # Thumb
            (0, 5), (5, 6), (6, 7), (7, 8),      # Index
            (0, 9), (9, 10), (10, 11), (11, 12), # Middle
            (0, 13), (13, 14), (14, 15), (15, 16), # Ring
            (0, 17), (17, 18), (18, 19), (19, 20)  # Pinky
        ]
        
        for connection in connections:
            start_idx, end_idx = connection
            if start_idx < len(landmarks_xy) and end_idx < len(landmarks_xy):
                x1, y1, z1, _ = landmarks_xy[start_idx]
                x2, y2, z2, _ = landmarks_xy[end_idx]
                
                # Depth-based color variation
                depth_color = self.interpolate_color_by_depth(z1, z2)
                
                # Draw line
                cv2.line(frame, (x1, y1), (x2, y2), self.colors['connections'], 2)
                # Draw glow effect
                cv2.line(frame, (x1, y1), (x2, y2), (100, 150, 200), 1)
        
        # Draw landmarks (joints) as circles
        for idx, (x, y, z, conf) in enumerate(landmarks_xy):
            # Size varies by confidence
            radius = 5 + int(3 * conf) if conf > 0 else 5
            
            # Joint colors
            if idx == 0:  # Wrist
                color = self.colors['palm']
                cv2.circle(frame, (x, y), radius + 2, color, -1)
            elif idx % 4 == 0:  # Finger tips (4, 8, 12, 16, 20)
                color = self.colors['active']
                cv2.circle(frame, (x, y), radius + 1, color, -1)
            else:  # Middle joints
                color = self.colors['joints']
                cv2.circle(frame, (x, y), radius, color, -1)
            
            # Outline
            cv2.circle(frame, (x, y), radius + 1, self.colors['landmarks'], 1)
            
            # Confidence indicator for finger tips
            if idx in [4, 8, 12, 16, 20]:  # Finger tips
                # Draw small bar showing confidence
                bar_width = int(10 * conf)
                cv2.rectangle(frame, (x - 5, y - 20), (x - 5 + bar_width, y - 15), 
                            self.colors['active'], -1)
        
        # Draw hand label
        if handedness:
            label = f"✋ {handedness.classification[0].label} ({hand_index+1})"
            cv2.putText(frame, label, (landmarks_xy[0][0] - 40, landmarks_xy[0][1] - 30),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, self.colors['text'], 2)
        
        return landmarks_xy
    
    def interpolate_color_by_depth(self, z1, z2):
        """Get color based on depth (z coordinate)"""
        avg_z = (z1 + z2) / 2
        
        if avg_z < 0:  # Closer to camera
            return (0, 255, 255)  # Cyan
        elif avg_z < 0.2:
            return (0, 200, 255)  # Light cyan
        else:
            return (100, 100, 255)  # Purple
    
    def draw_hand_info_panel(self, frame, hand_landmarks, handedness, hand_index=0):
        """Draw information panel for hand"""
        
        h, w, c = frame.shape
        panel_x = 20 + (hand_index * 450)
        panel_y = 20
        panel_w = 420
        panel_h = 180
        
        # Semi-transparent background
        overlay = frame.copy()
        cv2.rectangle(overlay, (panel_x, panel_y), (panel_x + panel_w, panel_y + panel_h), 
                     (10, 10, 30), -1)
        cv2.addWeighted(overlay, 0.7, frame, 0.3, 0, frame)
        
        # Border
        cv2.rectangle(frame, (panel_x, panel_y), (panel_x + panel_w, panel_y + panel_h), 
                     (0, 255, 255), 2)
        
        # Title
        title = f"✋ MANO {hand_index + 1}: {handedness.classification[0].label.upper()}"
        cv2.putText(frame, title, (panel_x + 15, panel_y + 35),
                   cv2.FONT_HERSHEY_DUPLEX, 1.0, (0, 255, 255), 1)
        
        # Calculate hand metrics
        landmarks_xy = [(int(l.x * w), int(l.y * h)) for l in hand_landmarks.landmark]
        
        # Hand center
        hand_center_x = int(np.mean([l[0] for l in landmarks_xy]))
        hand_center_y = int(np.mean([l[1] for l in landmarks_xy]))
        
        # Hand size (distance from wrist to middle finger tip)
        wrist = landmarks_xy[0]
        middle_tip = landmarks_xy[12]
        hand_size = np.sqrt((middle_tip[0]-wrist[0])**2 + (middle_tip[1]-wrist[1])**2)
        
        # Confidence
        conf = handedness.classification[0].score
        
        # Draw metrics
        y_offset = 70
        cv2.putText(frame, f"Posición: ({hand_center_x}, {hand_center_y})", 
                   (panel_x + 15, panel_y + y_offset),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, (100, 200, 255), 1)
        
        cv2.putText(frame, f"Tamaño: {int(hand_size)} px", 
                   (panel_x + 15, panel_y + y_offset + 30),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, (100, 200, 255), 1)
        
        cv2.putText(frame, f"Confianza: {conf:.1%}", 
                   (panel_x + 15, panel_y + y_offset + 60),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, (100, 200, 255), 1)
        
        cv2.putText(frame, f"Landmarks: {len(hand_landmarks.landmark)}", 
                   (panel_x + 15, panel_y + y_offset + 90),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, (100, 200, 255), 1)
        
        # Show finger states
        finger_names = ['Pulgar', 'Índice', 'Medio', 'Anular', 'Meñique']
        finger_tips = [4, 8, 12, 16, 20]
        finger_pips = [3, 7, 11, 15, 19]
        
        fingers_extended = 0
        for i, (tip_idx, pip_idx) in enumerate(zip(finger_tips, finger_pips)):
            if landmarks_xy[tip_idx][1] < landmarks_xy[pip_idx][1]:
                fingers_extended += 1
        
        if hand_index == 0:
            cv2.putText(frame, f"Dedos extendidos: {fingers_extended}/5", 
                       (panel_x + 15, panel_y + y_offset + 120),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 100), 1)
    
    def process_frame(self, frame):
        """Process frame and return hand info"""
        
        # Convert to RGB for MediaPipe
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        # Process
        results = self.hands.process(frame_rgb)
        
        return results
    
    def draw_full_visualization(self, frame, results):
        """Draw complete hand visualization"""
        
        if results.hand_landmarks and results.handedness:
            for idx, (hand_landmarks, handedness) in enumerate(
                zip(results.hand_landmarks, results.handedness)):
                # Draw landmarks
                self.draw_hand_landmarks_modern(frame, hand_landmarks, handedness, idx)
                # Draw info panel
                self.draw_hand_info_panel(frame, hand_landmarks, handedness, idx)
        else:
            # No hands detected - draw message
            cv2.putText(frame, "No se detectaron manos", 
                       (50, 100),
                       cv2.FONT_HERSHEY_DUPLEX, 1.5, (100, 100, 100), 2)
        
        return frame

def test_visualizer(camera_id=0):
    """Test the hand visualizer"""
    
    visualizer = HandVisualizer()
    cap = cv2.VideoCapture(camera_id)
    
    if not cap.isOpened():
        print("Could not open camera")
        return
    
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
    
    print("Press 'q' to quit")
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        
        frame = cv2.flip(frame, 1)
        
        # Process and visualize
        results = visualizer.process_frame(frame)
        frame = visualizer.draw_full_visualization(frame, results)
        
        cv2.imshow("Hand Visualizer Test", frame)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    test_visualizer()
