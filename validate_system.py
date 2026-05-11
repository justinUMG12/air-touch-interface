"""
Air Touch Interface - System Validation Script
Verify all dependencies and system configuration before running
"""

import sys
import platform
import subprocess
from pathlib import Path

class SystemValidator:
    def __init__(self):
        self.checks_passed = 0
        self.checks_failed = 0
        self.warnings = []
        self.errors = []
    
    def print_header(self):
        """Print header"""
        print("\n" + "="*70)
        print("  🔍 AIR TOUCH INTERFACE - SYSTEM VALIDATION")
        print("="*70 + "\n")
    
    def print_footer(self):
        """Print footer with summary"""
        print("\n" + "="*70)
        print(f"  ✅ PASSED: {self.checks_passed} | ❌ FAILED: {self.checks_failed}")
        print("="*70)
        
        if self.errors:
            print("\n⚠️  CRITICAL ERRORS:")
            for error in self.errors:
                print(f"  ❌ {error}")
        
        if self.warnings:
            print("\n⚠️  WARNINGS:")
            for warning in self.warnings:
                print(f"  ⚠️  {warning}")
        
        print()
    
    def check_os(self):
        """Check operating system"""
        print("1. Checking Operating System...")
        os_name = platform.system()
        
        if os_name == "Windows":
            version = platform.version()
            print(f"   ✅ Windows detected: {version}")
            self.checks_passed += 1
            return True
        else:
            error = f"Unsupported OS: {os_name} (Windows required)"
            print(f"   ❌ {error}")
            self.errors.append(error)
            self.checks_failed += 1
            return False
    
    def check_python_version(self):
        """Check Python version"""
        print("\n2. Checking Python Version...")
        version = sys.version_info
        version_str = f"{version.major}.{version.minor}.{version.micro}"
        
        if version.major == 3 and version.minor >= 8:
            print(f"   ✅ Python {version_str} (OK)")
            self.checks_passed += 1
            return True
        else:
            error = f"Python 3.8+ required, found {version_str}"
            print(f"   ❌ {error}")
            self.errors.append(error)
            self.checks_failed += 1
            return False
    
    def check_dependency(self, module_name, package_name):
        """Check if a module is installed"""
        try:
            __import__(module_name)
            print(f"   ✅ {package_name}")
            return True
        except ImportError:
            warning = f"{package_name} not installed"
            print(f"   ❌ {warning}")
            self.warnings.append(warning)
            return False
    
    def check_dependencies(self):
        """Check all required dependencies"""
        print("\n3. Checking Dependencies...")
        
        dependencies = [
            ('cv2', 'OpenCV'),
            ('mediapipe', 'MediaPipe'),
            ('pyautogui', 'PyAutoGUI'),
            ('numpy', 'NumPy'),
            ('tkinter', 'Tkinter'),
        ]
        
        all_present = True
        for module, name in dependencies:
            if not self.check_dependency(module, name):
                all_present = False
        
        if all_present:
            self.checks_passed += 1
            print("   ✅ All dependencies installed")
        else:
            self.checks_failed += 1
            print("\n   💡 Install missing dependencies:")
            print("      pip install -r requirements_v35.txt")
        
        return all_present
    
    def check_files(self):
        """Check required files"""
        print("\n4. Checking Project Files...")
        
        required_files = [
            'main_new.py',
            'splash_screen.py',
            'camera_selector.py',
            'quick_config.py',
            'hand_visualizer.py',
            'test_screen.py',
            'hand_tracker.py',
            'cursor_controller.py',
            'gesture_engine.py',
            'utils.py',
            'config_advanced.json',
            'AirTouch_v35.bat',
        ]
        
        missing = []
        for filename in required_files:
            path = Path(filename)
            if path.exists():
                print(f"   ✅ {filename}")
            else:
                print(f"   ❌ {filename} (missing)")
                missing.append(filename)
        
        if not missing:
            self.checks_passed += 1
            print("   ✅ All files present")
        else:
            self.checks_failed += 1
            error = f"Missing files: {', '.join(missing)}"
            self.errors.append(error)
        
        return len(missing) == 0
    
    def check_camera(self):
        """Check if camera is available"""
        print("\n5. Checking Camera...")
        
        try:
            import cv2
            cap = cv2.VideoCapture(0)
            if cap.isOpened():
                ret, frame = cap.read()
                cap.release()
                if ret:
                    print("   ✅ Camera detected and working")
                    self.checks_passed += 1
                    return True
                else:
                    warning = "Camera detected but cannot read frames"
                    print(f"   ⚠️  {warning}")
                    self.warnings.append(warning)
                    self.checks_failed += 1
                    return False
            else:
                warning = "No camera detected (USB camera recommended)"
                print(f"   ⚠️  {warning}")
                self.warnings.append(warning)
                self.checks_failed += 1
                return False
        except Exception as e:
            warning = f"Camera check failed: {str(e)}"
            print(f"   ⚠️  {warning}")
            self.warnings.append(warning)
            self.checks_failed += 1
            return False
    
    def check_disk_space(self):
        """Check available disk space"""
        print("\n6. Checking Disk Space...")
        
        try:
            import shutil
            total, used, free = shutil.disk_usage(".")
            free_mb = free / (1024 * 1024)
            
            if free_mb > 100:
                print(f"   ✅ {free_mb:.0f} MB available")
                self.checks_passed += 1
                return True
            else:
                warning = f"Low disk space: {free_mb:.0f} MB (500 MB recommended)"
                print(f"   ⚠️  {warning}")
                self.warnings.append(warning)
                self.checks_failed += 1
                return False
        except Exception as e:
            warning = f"Disk space check failed: {str(e)}"
            print(f"   ⚠️  {warning}")
            self.warnings.append(warning)
            return False
    
    def print_recommendations(self):
        """Print recommendations"""
        print("\n📋 RECOMMENDATIONS:\n")
        
        if self.errors:
            print("Fix critical errors before running:")
            for error in self.errors:
                print(f"  • {error}")
        
        if self.warnings:
            print("\nFor best experience, consider:")
            for warning in self.warnings:
                print(f"  • {warning}")
        
        print("\n💡 Installation help:")
        print("  1. Check README_v35_NEW.md for detailed guide")
        print("  2. Run: pip install -r requirements_v35.txt")
        print("  3. If issues persist, create issue on GitHub")
    
    def run_all_checks(self):
        """Run all system checks"""
        self.print_header()
        
        # Run checks
        self.check_os()
        self.check_python_version()
        self.check_dependencies()
        self.check_files()
        self.check_camera()
        self.check_disk_space()
        
        # Print results
        self.print_footer()
        
        # Print recommendations
        if self.errors:
            self.print_recommendations()
            return False
        else:
            print("✅ System is ready to run Air Touch Interface!\n")
            print("To start, run:")
            print("  python main_new.py")
            print("or double-click:")
            print("  AirTouch_v35.bat\n")
            return True

def main():
    """Main entry point"""
    validator = SystemValidator()
    success = validator.run_all_checks()
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
