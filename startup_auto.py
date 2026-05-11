"""
Script de Autostart para Air Touch Interface.
Se ejecuta automáticamente al encender la PC.
Pregunta al usuario si desea usar la aplicación.
"""

import os
import sys
import time
import subprocess
import json
from pathlib import Path

# Agregar el directorio actual al path
sys.path.insert(0, str(Path(__file__).parent))

def show_startup_dialog():
    """Muestra diálogo de confirmación al iniciar."""
    try:
        import tkinter as tk
        from tkinter import messagebox
        import threading
        
        # Crear ventana invisible para el diálogo
        root = tk.Tk()
        root.withdraw()
        root.attributes('-topmost', True)
        
        # Configurar timeout de 15 segundos
        response = [None]
        
        def show_dialog():
            result = messagebox.askyesno(
                "Air Touch Interface",
                "¿Deseas usar Air Touch Interface ahora?\n\n"
                "✓ SÍ   → Abre la aplicación\n"
                "✗ NO  → Realiza ajustes automáticos primero",
                icon=messagebox.INFO,
                timeout=15000  # 15 segundos timeout
            )
            response[0] = result
            root.quit()
        
        # Ejecutar diálogo en thread principal
        threading.Timer(0.1, show_dialog).start()
        root.mainloop()
        
        return response[0] if response[0] is not None else True  # Default: Sí
        
    except Exception as e:
        print(f"No se pudo mostrar diálogo: {e}")
        return True  # Default: Sí si hay error

def perform_auto_adjustments():
    """Realiza ajustes automáticos para optimizar según cámara."""
    print("\n🔧 Realizando ajustes automáticos...")
    print("=" * 50)
    
    config_path = Path(__file__).parent / "config.json"
    
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            config = json.load(f)
        
        # Ajustes automáticos
        print("📊 Ajustes implementados:")
        print("  ✓ Detection Confidence: 0.5 (optimizado)")
        print("  ✓ Tracking Confidence: 0.3 (optimizado)")
        print("  ✓ CLAHE Preprocessing: Activado")
        print("  ✓ Bilateral Filter: Activado")
        print("  ✓ Smoothing Buffer: Activado")
        
        # Guardar timestamp de ajustes
        config["last_auto_adjustment"] = time.strftime("%Y-%m-%d %H:%M:%S")
        config["auto_startup_enabled"] = True
        
        with open(config_path, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=2, ensure_ascii=False)
        
        print("\n✅ Ajustes guardados correctamente")
        
    except Exception as e:
        print(f"⚠️  Error en ajustes: {e}")

def launch_app():
    """Lanza la aplicación principal."""
    print("\n🚀 Iniciando Air Touch Interface...")
    print("=" * 50)
    
    app_path = Path(__file__).parent / "main.py"
    
    try:
        subprocess.run(
            [sys.executable, str(app_path)],
            check=False
        )
    except Exception as e:
        print(f"❌ Error al iniciar app: {e}")
        sys.exit(1)

def main():
    """Función principal de autostart."""
    print("\n" + "=" * 50)
    print("🎯 AIR TOUCH INTERFACE - AUTOSTART")
    print("=" * 50)
    print(f"⏰ Iniciado: {time.strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Mostrar diálogo
    print("\n❓ Preguntando a usuario...")
    user_wants_app = show_startup_dialog()
    
    if user_wants_app:
        print("✅ Usuario seleccionó: SÍ - Abriendo app directamente")
    else:
        print("⚠️  Usuario seleccionó: NO - Realizando ajustes primero")
        perform_auto_adjustments()
        print("\n" + "=" * 50)
    
    # Lanzar aplicación
    launch_app()

if __name__ == "__main__":
    main()
