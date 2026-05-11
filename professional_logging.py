"""
Professional Logging and Diagnostic System for Air Touch Interface v3.5
Comprehensive logging, performance monitoring, and diagnostics.
"""

import logging
import os
from pathlib import Path
import json
from datetime import datetime
import traceback
import time
from collections import deque

class AirTouchLogger:
    """Professional logging system with multiple handlers."""
    
    def __init__(self, log_dir="logs", log_file="airtouch.log", level=logging.INFO):
        self.log_dir = Path(log_dir)
        self.log_dir.mkdir(exist_ok=True)
        self.log_file = self.log_dir / log_file
        
        # Crear logger
        self.logger = logging.getLogger("AirTouch")
        self.logger.setLevel(level)
        
        # Formatter profesional
        formatter = logging.Formatter(
            '%(asctime)s | %(name)s | %(levelname)-8s | %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        
        # File handler
        file_handler = logging.FileHandler(self.log_file)
        file_handler.setFormatter(formatter)
        self.logger.addHandler(file_handler)
        
        # Console handler
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        self.logger.addHandler(console_handler)
        
        self.logger.info("🚀 Air Touch Interface Logger Initialized")
    
    def get_logger(self):
        return self.logger


class PerformanceMonitor:
    """Monitorea el rendimiento de la aplicación."""
    
    def __init__(self, history_size=300):
        self.history_size = history_size
        self.fps_history = deque(maxlen=history_size)
        self.latency_history = deque(maxlen=history_size)
        self.detection_history = deque(maxlen=history_size)
        
        self.start_time = time.time()
        self.frame_count = 0
        self.detection_count = 0
        self.click_count = 0
        
        # Stats
        self.stats = {
            "total_frames": 0,
            "total_detections": 0,
            "total_clicks": 0,
            "average_fps": 0,
            "average_latency": 0,
            "detection_rate": 0
        }
    
    def record_frame(self, fps):
        """Registra FPS de un frame."""
        self.fps_history.append(fps)
        self.frame_count += 1
        self.stats["total_frames"] = self.frame_count
        if len(self.fps_history) > 0:
            self.stats["average_fps"] = sum(self.fps_history) / len(self.fps_history)
    
    def record_detection(self, latency):
        """Registra una detección."""
        self.latency_history.append(latency)
        self.detection_count += 1
        self.stats["total_detections"] = self.detection_count
        if len(self.latency_history) > 0:
            self.stats["average_latency"] = sum(self.latency_history) / len(self.latency_history)
    
    def record_click(self):
        """Registra un click."""
        self.click_count += 1
        self.stats["total_clicks"] = self.click_count
    
    def get_stats(self):
        """Obtiene estadísticas actuales."""
        if self.frame_count > 0:
            self.stats["detection_rate"] = (self.detection_count / self.frame_count) * 100
        return self.stats
    
    def get_summary(self):
        """Obtiene resumen de rendimiento."""
        elapsed = time.time() - self.start_time
        stats = self.get_stats()
        return {
            "session_duration": elapsed,
            "average_fps": round(stats["average_fps"], 2),
            "average_latency_ms": round(stats["average_latency"] * 1000, 2),
            "detection_rate": round(stats["detection_rate"], 1),
            "total_clicks": stats["total_clicks"],
            "total_frames": stats["total_frames"],
            "total_detections": stats["total_detections"]
        }


class Diagnostics:
    """Sistema de diagnóstico y validación."""
    
    def __init__(self, logger):
        self.logger = logger.get_logger()
        self.errors = []
        self.warnings = []
    
    def check_camera(self):
        """Verifica disponibilidad de cámara."""
        try:
            import cv2
            cap = cv2.VideoCapture(0)
            if cap.isOpened():
                self.logger.info("✅ Camera detected and working")
                cap.release()
                return True
            else:
                msg = "❌ Camera not found or not accessible"
                self.logger.warning(msg)
                self.warnings.append(msg)
                return False
        except Exception as e:
            msg = f"❌ Camera check failed: {str(e)}"
            self.logger.error(msg)
            self.errors.append(msg)
            return False
    
    def check_mediapipe(self):
        """Verifica MediaPipe."""
        try:
            import mediapipe as mp
            self.logger.info("✅ MediaPipe installed and working")
            return True
        except Exception as e:
            msg = f"❌ MediaPipe check failed: {str(e)}"
            self.logger.error(msg)
            self.errors.append(msg)
            return False
    
    def check_opencv(self):
        """Verifica OpenCV."""
        try:
            import cv2
            self.logger.info(f"✅ OpenCV {cv2.__version__} detected")
            return True
        except Exception as e:
            msg = f"❌ OpenCV check failed: {str(e)}"
            self.logger.error(msg)
            self.errors.append(msg)
            return False
    
    def check_pyautogui(self):
        """Verifica PyAutoGUI."""
        try:
            import pyautogui
            screen_size = pyautogui.size()
            self.logger.info(f"✅ PyAutoGUI working, screen size: {screen_size}")
            return True
        except Exception as e:
            msg = f"❌ PyAutoGUI check failed: {str(e)}"
            self.logger.error(msg)
            self.errors.append(msg)
            return False
    
    def run_full_diagnostics(self):
        """Ejecuta diagnóstico completo."""
        self.logger.info("=" * 60)
        self.logger.info("🔍 RUNNING FULL DIAGNOSTICS")
        self.logger.info("=" * 60)
        
        results = {
            "camera": self.check_camera(),
            "mediapipe": self.check_mediapipe(),
            "opencv": self.check_opencv(),
            "pyautogui": self.check_pyautogui()
        }
        
        self.logger.info("=" * 60)
        self.logger.info("📊 DIAGNOSTIC RESULTS")
        self.logger.info("=" * 60)
        for key, value in results.items():
            status = "✅" if value else "❌"
            self.logger.info(f"{status} {key.upper()}: {'OK' if value else 'FAILED'}")
        
        if self.errors:
            self.logger.warning("\n⚠️ ERRORS:")
            for error in self.errors:
                self.logger.error(f"  {error}")
        
        if self.warnings:
            self.logger.warning("\n⚠️ WARNINGS:")
            for warning in self.warnings:
                self.logger.warning(f"  {warning}")
        
        return results


class BenchmarkMode:
    """Sistema de benchmark para medir rendimiento."""
    
    def __init__(self, logger, duration_seconds=30):
        self.logger = logger.get_logger()
        self.duration = duration_seconds
        self.results = {}
    
    def run_benchmark(self, monitor):
        """Ejecuta benchmark."""
        self.logger.info("=" * 60)
        self.logger.info("⚡ STARTING BENCHMARK")
        self.logger.info(f"Duration: {self.duration} seconds")
        self.logger.info("=" * 60)
        
        # En main.py se llamará durante la sesión
        # Aquí solo preparamos el reporte
    
    def generate_report(self, monitor):
        """Genera reporte de benchmark."""
        stats = monitor.get_summary()
        
        report = f"""
{'=' * 60}
📊 BENCHMARK REPORT
{'=' * 60}

SESSION STATISTICS:
  • Duration: {stats['session_duration']:.1f} seconds
  • Average FPS: {stats['average_fps']} fps
  • Average Latency: {stats['average_latency_ms']:.2f} ms
  • Detection Rate: {stats['detection_rate']:.1f}%
  
INTERACTION STATS:
  • Total Frames: {stats['total_frames']}
  • Total Detections: {stats['total_detections']}
  • Total Clicks: {stats['total_clicks']}

PERFORMANCE RATING:
  • FPS: {'Excellent' if stats['average_fps'] >= 25 else 'Good' if stats['average_fps'] >= 20 else 'Fair'}
  • Latency: {'Excellent' if stats['average_latency_ms'] <= 50 else 'Good' if stats['average_latency_ms'] <= 100 else 'Fair'}

{'=' * 60}
"""
        self.logger.info(report)
        self.results = stats
        return report


class SessionReporter:
    """Genera reportes de sesión profesionales."""
    
    def __init__(self, logger):
        self.logger = logger.get_logger()
    
    def generate_session_report(self, monitor, performance_data=None):
        """Genera reporte final de sesión."""
        stats = monitor.get_summary()
        
        report = f"""
{'=' * 70}
{'🎯 AIR TOUCH INTERFACE - SESSION REPORT':^70}
{'=' * 70}

📅 TIMESTAMP: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

⏱️  SESSION DURATION: {stats['session_duration']:.1f} seconds

📊 PERFORMANCE METRICS:
   ├─ Average FPS: {stats['average_fps']:.1f}
   ├─ Average Latency: {stats['average_latency_ms']:.2f} ms
   ├─ Detection Rate: {stats['detection_rate']:.1f}%
   └─ Response Time: Optimal

🖱️  INTERACTION SUMMARY:
   ├─ Total Frames Processed: {stats['total_frames']}
   ├─ Total Hand Detections: {stats['total_detections']}
   ├─ Total Clicks: {stats['total_clicks']}
   └─ Clicks per Minute: {(stats['total_clicks'] / (stats['session_duration']/60) if stats['session_duration'] > 0 else 0):.1f}

✅ STATUS: Session completed successfully
🔧 NEXT: Check diagnostics if performance needs improvement

{'=' * 70}
"""
        self.logger.info(report)
        return report
    
    def save_session_log(self, log_file="logs/session_reports.json"):
        """Guarda log de sesión en JSON."""
        Path("logs").mkdir(exist_ok=True)
        
        try:
            # Intentar cargar reportes anteriores
            if os.path.exists(log_file):
                with open(log_file, 'r') as f:
                    reports = json.load(f)
            else:
                reports = []
            
            # Agregar nuevo reporte
            report = {
                "timestamp": datetime.now().isoformat(),
                "duration": time.time()
            }
            reports.append(report)
            
            # Guardar
            with open(log_file, 'w') as f:
                json.dump(reports, f, indent=2)
            
            self.logger.info(f"✅ Session log saved to {log_file}")
        except Exception as e:
            self.logger.error(f"❌ Failed to save session log: {str(e)}")


# Inicialización global
_logger = None
_monitor = None
_diagnostics = None
_reporter = None


def initialize_logging(log_level=logging.INFO):
    """Inicializa el sistema de logging global."""
    global _logger, _monitor, _diagnostics, _reporter
    
    _logger = AirTouchLogger(level=log_level)
    _monitor = PerformanceMonitor()
    _diagnostics = Diagnostics(_logger)
    _reporter = SessionReporter(_logger)
    
    return _logger, _monitor, _diagnostics, _reporter


def get_logger():
    """Obtiene el logger global."""
    global _logger
    if _logger is None:
        initialize_logging()
    return _logger


def get_monitor():
    """Obtiene el monitor de rendimiento global."""
    global _monitor
    if _monitor is None:
        initialize_logging()
    return _monitor


def get_diagnostics():
    """Obtiene el sistema de diagnósticos global."""
    global _diagnostics
    if _diagnostics is None:
        initialize_logging()
    return _diagnostics


def get_reporter():
    """Obtiene el reportero de sesión global."""
    global _reporter
    if _reporter is None:
        initialize_logging()
    return _reporter
