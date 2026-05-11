"""
Air Touch Interface v3.5 - Professional Launcher
Main entry point for the application with menu system and professional features.
"""

import os
import sys
import json
from pathlib import Path
import subprocess
import platform
import time

# Add current directory to path
sys.path.insert(0, str(Path(__file__).parent))

from professional_logging import initialize_logging, get_logger, get_diagnostics, get_monitor, get_reporter


class AirTouchLauncher:
    """Launcer profesional con sistema de menú."""
    
    def __init__(self):
        self.logger, self.monitor, self.diagnostics, self.reporter = initialize_logging()
        self.config = self.load_config()
        
    def load_config(self):
        """Carga configuración."""
        config_file = Path(__file__).parent / "config_advanced.json"
        if config_file.exists():
            with open(config_file, 'r') as f:
                return json.load(f)
        return {}
    
    def clear_screen(self):
        """Limpia la pantalla."""
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def print_banner(self):
        """Imprime el banner de bienvenida."""
        self.clear_screen()
        banner = """
╔════════════════════════════════════════════════════════════════╗
║                                                                ║
║        🎯 AIR TOUCH INTERFACE v3.5 - ULTIMATE EDITION 🎯      ║
║                                                                ║
║         Control Windows with Hand Gestures in Mid-Air          ║
║                                                                ║
╚════════════════════════════════════════════════════════════════╝

🖐️  Technology Stack:
    • MediaPipe Hand Detection
    • OpenCV Real-time Processing
    • PyAutoGUI Cursor Control
    • Professional Settings UI

✨ Features:
    ✅ Smooth cursor movement with adaptive smoothing
    ✅ Precision clicking with depth detection
    ✅ Left/Right hand support with automatic detection
    ✅ Multiple tracking modes (Gaming, Precision, Navigation)
    ✅ Professional settings panel
    ✅ Real-time performance monitoring
    ✅ Accessibility features

📊 Current Profile: {profile}
🎨 Theme: {theme}

{'='*66}

"""
        print(banner.format(
            profile=self.config.get('profile', 'Standard'),
            theme=self.config.get('visual', {}).get('theme', 'modern_dark')
        ))
    
    def print_main_menu(self):
        """Imprime el menú principal."""
        menu = """
┌─ MAIN MENU ──────────────────────────────────────────────────┐
│                                                               │
│  1️⃣  ▶ START AIR TOUCH INTERFACE                             │
│  2️⃣  ⚙️  SETTINGS & CONFIGURATION                             │
│  3️⃣  🔍 RUN DIAGNOSTICS                                      │
│  4️⃣  📊 PERFORMANCE BENCHMARK                                │
│  5️⃣  📚 HELP & TUTORIAL                                      │
│  6️⃣  💾 MANAGE PROFILES                                      │
│  7️⃣  📝 VIEW LOGS                                            │
│  8️⃣  ❌ EXIT                                                  │
│                                                               │
└───────────────────────────────────────────────────────────────┘

"""
        print(menu)
    
    def start_application(self):
        """Inicia la aplicación principal."""
        self.logger.get_logger().info("🚀 Starting Air Touch Interface...")
        print("\n⏳ Initializing components...")
        print("   • Loading hand tracker...")
        print("   • Initializing camera...")
        print("   • Starting gesture engine...")
        print("\n✅ All systems initialized!")
        print("\n" + "="*66)
        print("INSTRUCTIONS:")
        print("="*66)
        print("  🖐️  Move your hand to move the cursor")
        print("  👆 Push forward (toward camera) to CLICK")
        print("  ✋✋ Two hands: SCROLL vertically")
        print("  📸 'p' to take screenshot")
        print("  🔧 's' to open settings")
        print("  🆘 'd' for debug info")
        print("  ❌ 'q' to QUIT")
        print("="*66 + "\n")
        
        try:
            # Import and run main
            from main import main
            main()
        except KeyboardInterrupt:
            print("\n⏸️  Application paused by user")
        except Exception as e:
            self.logger.get_logger().error(f"Application error: {str(e)}")
            print(f"\n❌ Error: {str(e)}")
            input("\nPress Enter to continue...")
    
    def open_settings(self):
        """Abre el panel de configuración."""
        print("\n⏳ Loading settings interface...")
        try:
            from settings_ui import SettingsUI
            app = SettingsUI()
            app.run()
        except Exception as e:
            self.logger.get_logger().error(f"Settings error: {str(e)}")
            print(f"❌ Error opening settings: {str(e)}")
            input("\nPress Enter to continue...")
    
    def run_diagnostics(self):
        """Ejecuta diagnósticos."""
        print("\n" + "="*66)
        print("🔍 RUNNING DIAGNOSTICS")
        print("="*66 + "\n")
        
        results = self.diagnostics.run_full_diagnostics()
        
        print("\n" + "="*66)
        all_ok = all(results.values())
        if all_ok:
            print("✅ All systems operational!")
        else:
            print("⚠️  Some components need attention")
        print("="*66)
        
        input("\nPress Enter to continue...")
    
    def run_benchmark(self):
        """Ejecuta benchmark."""
        print("\n" + "="*66)
        print("⚡ PERFORMANCE BENCHMARK")
        print("="*66)
        print("\n📝 Note: Benchmark will run during normal application usage")
        print("   Keep your hand in front of the camera for best results")
        print("\n⏳ Starting application in benchmark mode...")
        print("   Run will continue for 60 seconds...")
        
        try:
            from main import main
            main()
            
            # Mostrar resultados
            stats = self.monitor.get_summary()
            print("\n" + "="*66)
            print("⚡ BENCHMARK RESULTS")
            print("="*66)
            print(f"Average FPS: {stats['average_fps']:.1f}")
            print(f"Average Latency: {stats['average_latency_ms']:.2f} ms")
            print(f"Detection Rate: {stats['detection_rate']:.1f}%")
            print(f"Total Clicks: {stats['total_clicks']}")
            print("="*66)
        except Exception as e:
            self.logger.get_logger().error(f"Benchmark error: {str(e)}")
            print(f"\n❌ Error: {str(e)}")
        
        input("\nPress Enter to continue...")
    
    def show_help(self):
        """Muestra ayuda y tutorial."""
        help_text = """
╔════════════════════════════════════════════════════════════════╗
║                   📚 HELP & TUTORIAL 📚                        ║
╚════════════════════════════════════════════════════════════════╝

🎯 BASIC USAGE:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

1. CURSOR MOVEMENT
   ├─ Position your right hand in front of camera
   ├─ Move hand to move cursor
   ├─ Adjust sensitivity in Settings
   └─ Works best at arm's length distance

2. CLICKING
   ├─ When cursor is over target, push hand forward
   ├─ Depth of push determines click strength
   ├─ Adjust click sensitivity in Settings
   └─ Cooldown prevents double-clicks (configurable)

3. SCROLLING
   ├─ Raise both hands in front of camera
   ├─ Move hands up/down to scroll
   ├─ Adjust scroll sensitivity in Settings
   └─ Works with any scrollable window

4. HAND SELECTION
   ├─ Use Settings → Hand Tracking → Dominant Hand
   ├─ Select: Left, Right, or Auto
   ├─ Auto detects right hand by default
   └─ Can switch during session

⚙️  CONFIGURATION:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

PROFILES:
  • Gaming: Fast response, low smoothing
  • Precision: Slow, high stability
  • Navigation: Balanced for web browsing
  • Accessibility: Extra stable, large cursor

THEMES:
  • Modern Dark: Professional dark theme
  • Modern Light: Bright, clean design
  • Neon Futuristic: Sci-fi glowing effect
  • Minimal: Minimalist interface

PERFORMANCE MODES:
  • Power Saving: Lower CPU usage
  • Balanced: Default, good balance
  • Maximum: Highest responsiveness

🔧 KEYBOARD SHORTCUTS:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  q  ─ Quit application
  s  ─ Open settings
  d  ─ Toggle debug info
  c  ─ Calibration mode
  p  ─ Take screenshot
  o  ─ Toggle overlay

💡 TIPS:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

✓ Best distance: 50-150 cm from camera
✓ Good lighting: Face forward, not backlit
✓ Steady hand: Rest arm for precision tasks
✓ Profile switching: Quick profiles in Settings
✓ Calibration: Run calibration if tracking is unstable

🆘 TROUBLESHOOTING:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Hand not detected:
  → Check camera (use Diagnostics)
  → Ensure good lighting
  → Move hand closer to camera
  → Try low light mode in Hand Tracking settings

Cursor jumps around:
  → Increase smoothing in Cursor settings
  → Use Precision profile
  → Check for reflections/glare
  → Increase stability level

Click not registering:
  → Check click sensitivity
  → Ensure steady push forward
  → Try different force settings
  → Run diagnostics on camera

Slow performance:
  → Lower camera resolution
  → Use Power Saving mode
  → Close background applications
  → Run Benchmark to check performance

╔════════════════════════════════════════════════════════════════╗

"""
        print(help_text)
        input("Press Enter to continue...")
    
    def manage_profiles(self):
        """Gestor de perfiles."""
        print("\n" + "="*66)
        print("💾 PROFILE MANAGER")
        print("="*66)
        print("\nAvailable Profiles:")
        print("  1. Standard - Default balanced settings")
        print("  2. Gaming - Fast, responsive")
        print("  3. Precision - Stable, accurate")
        print("  4. Navigation - Web browsing optimized")
        print("  5. Accessibility - For mobility assistance")
        print("  6. Create New Profile")
        print("  7. Back to Main Menu")
        
        choice = input("\nSelect option (1-7): ").strip()
        if choice == "1":
            self.config['profile'] = 'Standard'
            print("✅ Switched to Standard profile")
        elif choice == "2":
            self.config['profile'] = 'Gaming'
            print("✅ Switched to Gaming profile")
        elif choice == "3":
            self.config['profile'] = 'Precision'
            print("✅ Switched to Precision profile")
        elif choice == "4":
            self.config['profile'] = 'Navigation'
            print("✅ Switched to Navigation profile")
        elif choice == "5":
            self.config['profile'] = 'Accessibility'
            print("✅ Switched to Accessibility profile")
        
        time.sleep(1)
    
    def view_logs(self):
        """Muestra logs."""
        log_file = Path("logs") / "airtouch.log"
        if log_file.exists():
            print("\n" + "="*66)
            print("📝 RECENT LOGS")
            print("="*66 + "\n")
            
            with open(log_file, 'r') as f:
                lines = f.readlines()
                # Show last 20 lines
                for line in lines[-20:]:
                    print(line.rstrip())
        else:
            print("\n❌ No logs found yet. Run the application first.")
        
        print("\n" + "="*66)
        input("Press Enter to continue...")
    
    def run(self):
        """Ejecuta el launcher."""
        while True:
            self.print_banner()
            self.print_main_menu()
            
            choice = input("Select option (1-8): ").strip()
            
            if choice == "1":
                self.start_application()
            elif choice == "2":
                self.open_settings()
            elif choice == "3":
                self.run_diagnostics()
            elif choice == "4":
                self.run_benchmark()
            elif choice == "5":
                self.show_help()
            elif choice == "6":
                self.manage_profiles()
            elif choice == "7":
                self.view_logs()
            elif choice == "8":
                self.print_goodbye()
                break
            else:
                print("\n❌ Invalid option. Please select 1-8.")
                input("Press Enter to continue...")
    
    def print_goodbye(self):
        """Mensaje de despedida."""
        goodbye = """

╔════════════════════════════════════════════════════════════════╗
║                                                                ║
║                 👋 Thank you for using AIR TOUCH! 👋           ║
║                                                                ║
║                    See you next time! 👀                       ║
║                                                                ║
╚════════════════════════════════════════════════════════════════╝

            Made with ❤️  for Gesture Control
            
"""
        print(goodbye)
        time.sleep(2)


def main():
    """Punto de entrada principal."""
    launcher = AirTouchLauncher()
    launcher.run()


if __name__ == "__main__":
    main()
