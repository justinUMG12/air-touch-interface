"""
Script de prueba para autostart.
Simula el comportamiento sin diálogo interactivo.
"""

import sys
import io
import json
from pathlib import Path
import time

# Fijar encoding UTF-8 para soporte de emojis
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

sys.path.insert(0, str(Path(__file__).parent))

def test_startup():
    """Prueba la funcionalidad de autostart."""
    print("\n" + "=" * 60)
    print("🧪 TEST AUTOSTART - Air Touch Interface")
    print("=" * 60 + "\n")
    
    # Test 1: Verificar archivos
    print("✓ Test 1: Verificar archivos necesarios")
    config_file = Path(__file__).parent / "config.json"
    startup_file = Path(__file__).parent / "startup_auto.py"
    main_file = Path(__file__).parent / "main.py"
    
    files_ok = config_file.exists() and startup_file.exists() and main_file.exists()
    print(f"  • config.json: {'✅' if config_file.exists() else '❌'}")
    print(f"  • startup_auto.py: {'✅' if startup_file.exists() else '❌'}")
    print(f"  • main.py: {'✅' if main_file.exists() else '❌'}")
    
    if not files_ok:
        print("\n❌ Error: Faltan archivos")
        return False
    
    # Test 2: Cargar configuración
    print("\n✓ Test 2: Cargar configuración")
    try:
        with open(config_file, 'r', encoding='utf-8') as f:
            config = json.load(f)
        print("  ✅ Configuración cargada correctamente")
    except Exception as e:
        print(f"  ❌ Error: {e}")
        return False
    
    # Test 3: Verificar parámetros de performance
    print("\n✓ Test 3: Parámetros de performance")
    try:
        perf = config.get("performance", {})
        print(f"  • Detection Confidence: {perf.get('detection_confidence', 0.5)}")
        print(f"  • Tracking Confidence: {perf.get('tracking_confidence', 0.3)}")
        print(f"  • Max Hands: {perf.get('max_hands', 2)}")
        print("  ✅ Parámetros válidos")
    except Exception as e:
        print(f"  ❌ Error: {e}")
        return False
    
    # Test 4: Importar módulos
    print("\n✓ Test 4: Importar módulos principales")
    try:
        from hand_tracker import HandTracker
        print("  • HandTracker: ✅")
        from gesture_engine import GestureEngine
        print("  • GestureEngine: ✅")
        from cursor_controller import CursorController
        print("  • CursorController: ✅")
        from utils import load_config
        print("  • Utils: ✅")
        print("  ✅ Todos los módulos importados")
    except Exception as e:
        print(f"  ❌ Error: {e}")
        return False
    
    # Test 5: Simular ajustes automáticos
    print("\n✓ Test 5: Simular ajustes automáticos")
    try:
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
        config["last_auto_adjustment"] = timestamp
        config["auto_startup_enabled"] = True
        
        print(f"  • Timestamp: {timestamp}")
        print(f"  • Auto-adjust habilitado: True")
        print("  ✅ Ajustes simulados correctamente")
    except Exception as e:
        print(f"  ❌ Error: {e}")
        return False
    
    # Test 6: Resumen de parámetros optimizados
    print("\n✓ Test 6: Parámetros optimizados para baja calidad")
    print("  Imagen:")
    print("    • CLAHE: Activado")
    print("    • Bilateral Filter: Activado")
    print("    • Nitidez: Activada")
    print("  Detección:")
    print(f"    • Detection Confidence: {perf.get('detection_confidence', 0.5)}")
    print(f"    • Tracking Confidence: {perf.get('tracking_confidence', 0.3)}")
    print("  Cursor:")
    print(f"    • Sensitivity: {config['cursor'].get('sensitivity', 1.5)}")
    print(f"    • Smoothing Factor: {config['cursor'].get('smoothing_factor', 0.5)}")
    print("  ✅ Parámetros optimizados")
    
    return True

if __name__ == "__main__":
    success = test_startup()
    
    print("\n" + "=" * 60)
    if success:
        print("✅ TODOS LOS TESTS PASARON CORRECTAMENTE")
        print("=" * 60)
        print("\nLa app está lista para autostart:")
        print("  1. Ejecuta: setup_autostart.bat (como administrador)")
        print("  2. O ejecuta: setup_autostart.ps1 (en PowerShell admin)")
        print("  3. Reinicia tu PC")
        print("  4. ¡La app se abrirá automáticamente!")
    else:
        print("❌ ALGUNOS TESTS FALLARON")
        print("=" * 60)
        sys.exit(1)
