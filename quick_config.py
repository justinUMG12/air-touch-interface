"""
Quick Config Module
Modern GUI for rapid configuration before starting the application
"""

import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
from pathlib import Path

class QuickConfigUI:
    def __init__(self, config_file="config_advanced.json"):
        self.config_file = config_file
        self.config = self.load_config()
        
        self.root = tk.Tk()
        self.root.title("⚙️  Air Touch Interface - Configuración Rápida")
        self.root.geometry("1000x700")
        
        # Style
        self.setup_style()
        
        # Result
        self.result = None
    
    def setup_style(self):
        """Setup modern theme"""
        style = ttk.Style()
        
        # Dark theme
        self.bg_color = "#1a1a2e"
        self.fg_color = "#00ffff"
        self.root.configure(bg=self.bg_color)
        
        style.theme_use('clam')
        style.configure('TFrame', background=self.bg_color)
        style.configure('TLabel', background=self.bg_color, foreground=self.fg_color)
        style.configure('TScale', background=self.bg_color)
        style.configure('Title.TLabel', font=('Arial', 20, 'bold'), 
                       foreground='#00ffff', background=self.bg_color)
        style.configure('Section.TLabel', font=('Arial', 14, 'bold'), 
                       foreground='#ff00ff', background=self.bg_color)
        style.configure('Normal.TLabel', font=('Arial', 10), 
                       foreground='#aaaaaa', background=self.bg_color)
    
    def load_config(self):
        """Load configuration from JSON"""
        if os.path.exists(self.config_file):
            with open(self.config_file, 'r') as f:
                return json.load(f)
        return {
            'cursor': {},
            'click': {},
            'hand_tracking': {},
            'visual': {}
        }
    
    def save_config(self):
        """Save configuration to JSON"""
        with open(self.config_file, 'w') as f:
            json.dump(self.config, f, indent=2)
        return True
    
    def create_ui(self):
        """Create the configuration UI"""
        
        # Main container
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Title
        title_label = ttk.Label(main_frame, text="CONFIGURACIÓN RÁPIDA", 
                               style='Title.TLabel')
        title_label.pack(pady=10)
        
        # Create notebook (tabs)
        notebook = ttk.Notebook(main_frame)
        notebook.pack(fill=tk.BOTH, expand=True)
        
        # Tab 1: Cursor
        self.create_cursor_tab(notebook)
        
        # Tab 2: Click
        self.create_click_tab(notebook)
        
        # Tab 3: Hand Tracking
        self.create_tracking_tab(notebook)
        
        # Tab 4: Visual
        self.create_visual_tab(notebook)
        
        # Button frame
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=20)
        
        # Buttons
        save_btn = tk.Button(button_frame, text="✅ GUARDAR Y CONTINUAR", 
                            command=self.save_and_continue,
                            bg='#00aa00', fg='white', font=('Arial', 12, 'bold'),
                            padx=20, pady=10)
        save_btn.pack(side=tk.LEFT, padx=10)
        
        cancel_btn = tk.Button(button_frame, text="❌ CANCELAR", 
                              command=self.cancel,
                              bg='#aa0000', fg='white', font=('Arial', 12, 'bold'),
                              padx=20, pady=10)
        cancel_btn.pack(side=tk.LEFT, padx=10)
        
        reset_btn = tk.Button(button_frame, text="🔄 RESETEAR VALORES", 
                             command=self.reset_to_defaults,
                             bg='#444444', fg='white', font=('Arial', 10),
                             padx=15, pady=8)
        reset_btn.pack(side=tk.RIGHT, padx=10)
    
    def create_cursor_tab(self, notebook):
        """Create cursor settings tab"""
        frame = ttk.Frame(notebook)
        notebook.add(frame, text="🖱️  CURSOR")
        
        # Padding
        inner_frame = ttk.Frame(frame)
        inner_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)
        
        # Velocidad
        ttk.Label(inner_frame, text="VELOCIDAD DEL CURSOR", 
                 style='Section.TLabel').pack(anchor='w')
        
        speed_frame = ttk.Frame(inner_frame)
        speed_frame.pack(fill=tk.X, pady=10)
        
        self.speed_var = tk.DoubleVar(value=self.config.get('cursor', {}).get('speed', 1.8))
        speed_scale = ttk.Scale(speed_frame, from_=0.5, to=3.0, 
                               orient=tk.HORIZONTAL, variable=self.speed_var)
        speed_scale.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        self.speed_label = ttk.Label(speed_frame, text="1.8")
        self.speed_label.pack(side=tk.LEFT, padx=10)
        self.speed_var.trace('w', lambda *args: self.update_label(self.speed_var, self.speed_label))
        
        # Sensibilidad
        ttk.Label(inner_frame, text="SENSIBILIDAD", 
                 style='Section.TLabel').pack(anchor='w', pady=(20, 0))
        
        sens_frame = ttk.Frame(inner_frame)
        sens_frame.pack(fill=tk.X, pady=10)
        
        self.sens_var = tk.DoubleVar(value=self.config.get('cursor', {}).get('sensitivity', 1.8))
        sens_scale = ttk.Scale(sens_frame, from_=0.5, to=3.0, 
                              orient=tk.HORIZONTAL, variable=self.sens_var)
        sens_scale.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        self.sens_label = ttk.Label(sens_frame, text="1.8")
        self.sens_label.pack(side=tk.LEFT, padx=10)
        self.sens_var.trace('w', lambda *args: self.update_label(self.sens_var, self.sens_label))
        
        # Suavizado
        ttk.Label(inner_frame, text="SUAVIZADO", 
                 style='Section.TLabel').pack(anchor='w', pady=(20, 0))
        
        smooth_frame = ttk.Frame(inner_frame)
        smooth_frame.pack(fill=tk.X, pady=10)
        
        self.smooth_var = tk.DoubleVar(value=self.config.get('cursor', {}).get('smoothing', 0.5))
        smooth_scale = ttk.Scale(smooth_frame, from_=0.0, to=1.0, 
                                orient=tk.HORIZONTAL, variable=self.smooth_var)
        smooth_scale.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        self.smooth_label = ttk.Label(smooth_frame, text="0.5")
        self.smooth_label.pack(side=tk.LEFT, padx=10)
        self.smooth_var.trace('w', lambda *args: self.update_label(self.smooth_var, self.smooth_label))
        
        # Tamaño del cursor
        ttk.Label(inner_frame, text="TAMAÑO DEL CURSOR", 
                 style='Section.TLabel').pack(anchor='w', pady=(20, 0))
        
        self.size_var = tk.StringVar(value=self.config.get('cursor', {}).get('size', 'medium'))
        size_frame = ttk.Frame(inner_frame)
        size_frame.pack(fill=tk.X, pady=10)
        
        for size in ['small', 'medium', 'large', 'gigantic']:
            rb = ttk.Radiobutton(size_frame, text=size.upper(), variable=self.size_var, 
                                value=size)
            rb.pack(side=tk.LEFT, padx=10)
    
    def create_click_tab(self, notebook):
        """Create click settings tab"""
        frame = ttk.Frame(notebook)
        notebook.add(frame, text="👆 CLICK")
        
        inner_frame = ttk.Frame(frame)
        inner_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)
        
        # Sensibilidad de pulsación
        ttk.Label(inner_frame, text="SENSIBILIDAD DE PULSACIÓN", 
                 style='Section.TLabel').pack(anchor='w')
        
        click_sens_frame = ttk.Frame(inner_frame)
        click_sens_frame.pack(fill=tk.X, pady=10)
        
        self.click_sens_var = tk.DoubleVar(value=self.config.get('click', {}).get('sensitivity', 1.0))
        click_sens_scale = ttk.Scale(click_sens_frame, from_=0.5, to=2.0, 
                                     orient=tk.HORIZONTAL, variable=self.click_sens_var)
        click_sens_scale.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        self.click_sens_label = ttk.Label(click_sens_frame, text="1.0")
        self.click_sens_label.pack(side=tk.LEFT, padx=10)
        self.click_sens_var.trace('w', lambda *args: self.update_label(self.click_sens_var, self.click_sens_label))
        
        # Distancia de activación
        ttk.Label(inner_frame, text="DISTANCIA DE ACTIVACIÓN", 
                 style='Section.TLabel').pack(anchor='w', pady=(20, 0))
        
        dist_frame = ttk.Frame(inner_frame)
        dist_frame.pack(fill=tk.X, pady=10)
        
        self.dist_var = tk.DoubleVar(value=self.config.get('click', {}).get('distance_threshold', 0.35))
        dist_scale = ttk.Scale(dist_frame, from_=0.1, to=0.8, 
                              orient=tk.HORIZONTAL, variable=self.dist_var)
        dist_scale.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        self.dist_label = ttk.Label(dist_frame, text="0.35")
        self.dist_label.pack(side=tk.LEFT, padx=10)
        self.dist_var.trace('w', lambda *args: self.update_label(self.dist_var, self.dist_label, format_str="{:.2f}"))
        
        # Cooldown
        ttk.Label(inner_frame, text="COOLDOWN (ms)", 
                 style='Section.TLabel').pack(anchor='w', pady=(20, 0))
        
        cooldown_frame = ttk.Frame(inner_frame)
        cooldown_frame.pack(fill=tk.X, pady=10)
        
        self.cooldown_var = tk.IntVar(value=self.config.get('click', {}).get('cooldown_ms', 250))
        cooldown_scale = ttk.Scale(cooldown_frame, from_=100, to=500, 
                                   orient=tk.HORIZONTAL, variable=self.cooldown_var)
        cooldown_scale.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        self.cooldown_label = ttk.Label(cooldown_frame, text="250")
        self.cooldown_label.pack(side=tk.LEFT, padx=10)
        self.cooldown_var.trace('w', lambda *args: self.update_label(self.cooldown_var, self.cooldown_label))
        
        # Double click
        self.double_click_var = tk.BooleanVar(
            value=self.config.get('click', {}).get('double_click_enabled', True))
        double_click_check = ttk.Checkbutton(inner_frame, text="Habilitar Double-Click", 
                                            variable=self.double_click_var)
        double_click_check.pack(anchor='w', pady=(20, 0))
    
    def create_tracking_tab(self, notebook):
        """Create hand tracking settings tab"""
        frame = ttk.Frame(notebook)
        notebook.add(frame, text="✋ TRACKING")
        
        inner_frame = ttk.Frame(frame)
        inner_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)
        
        # Mano dominante
        ttk.Label(inner_frame, text="MANO DOMINANTE", 
                 style='Section.TLabel').pack(anchor='w')
        
        self.hand_var = tk.StringVar(value=self.config.get('hand_tracking', {}).get('dominant_hand', 'auto'))
        hand_frame = ttk.Frame(inner_frame)
        hand_frame.pack(fill=tk.X, pady=10)
        
        for hand in ['auto', 'derecha', 'izquierda']:
            rb = ttk.Radiobutton(hand_frame, text=hand.upper(), variable=self.hand_var, 
                                value=hand)
            rb.pack(side=tk.LEFT, padx=10)
        
        # Modo de tracking
        ttk.Label(inner_frame, text="MODO DE TRACKING", 
                 style='Section.TLabel').pack(anchor='w', pady=(20, 0))
        
        self.track_mode_var = tk.StringVar(value=self.config.get('hand_tracking', {}).get('tracking_mode', 'smooth'))
        mode_frame = ttk.Frame(inner_frame)
        mode_frame.pack(fill=tk.X, pady=10)
        
        for mode in ['smooth', 'aggressive', 'slow_motion']:
            rb = ttk.Radiobutton(mode_frame, text=mode.upper(), variable=self.track_mode_var, 
                                value=mode)
            rb.pack(side=tk.LEFT, padx=10)
        
        # Show landmarks
        self.show_landmarks_var = tk.BooleanVar(value=True)
        landmarks_check = ttk.Checkbutton(inner_frame, text="✅ Mostrar puntos de mano", 
                                         variable=self.show_landmarks_var)
        landmarks_check.pack(anchor='w', pady=(20, 0))
        
        # Show lines
        self.show_lines_var = tk.BooleanVar(value=True)
        lines_check = ttk.Checkbutton(inner_frame, text="✅ Mostrar líneas de tracking", 
                                     variable=self.show_lines_var)
        lines_check.pack(anchor='w', pady=5)
        
        # Show FPS
        self.show_fps_var = tk.BooleanVar(value=True)
        fps_check = ttk.Checkbutton(inner_frame, text="✅ Mostrar FPS", 
                                   variable=self.show_fps_var)
        fps_check.pack(anchor='w', pady=5)
        
        # Show overlay
        self.show_overlay_var = tk.BooleanVar(value=True)
        overlay_check = ttk.Checkbutton(inner_frame, text="✅ Mostrar overlay visual", 
                                       variable=self.show_overlay_var)
        overlay_check.pack(anchor='w', pady=5)
    
    def create_visual_tab(self, notebook):
        """Create visual settings tab"""
        frame = ttk.Frame(notebook)
        notebook.add(frame, text="🎨 VISUAL")
        
        inner_frame = ttk.Frame(frame)
        inner_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)
        
        # Tema
        ttk.Label(inner_frame, text="TEMA", 
                 style='Section.TLabel').pack(anchor='w')
        
        self.theme_var = tk.StringVar(value=self.config.get('visual', {}).get('theme', 'modern_dark'))
        theme_frame = ttk.Frame(inner_frame)
        theme_frame.pack(fill=tk.X, pady=10)
        
        for theme in ['modern_dark', 'modern_light', 'neon', 'minimal']:
            rb = ttk.Radiobutton(theme_frame, text=theme.replace('_', ' ').upper(), 
                                variable=self.theme_var, value=theme)
            rb.pack(side=tk.LEFT, padx=10)
        
        # Info text
        info_frame = ttk.Frame(inner_frame)
        info_frame.pack(fill=tk.BOTH, expand=True, pady=(30, 0))
        
        info_text = """
🎯 TIPS DE CONFIGURACIÓN:

👤 PRINCIPIANTE:
   • Velocidad: 1.5 - 2.0
   • Sensibilidad: 1.5 - 2.0
   • Suavizado: 0.6 - 0.8

🎮 JUGADOR:
   • Velocidad: 2.5 - 3.0
   • Sensibilidad: 2.0 - 2.5
   • Suavizado: 0.2 - 0.4

🎯 PRECISIÓN:
   • Velocidad: 1.0 - 1.5
   • Sensibilidad: 1.0 - 1.5
   • Suavizado: 0.8 - 1.0
        """
        
        info_label = ttk.Label(inner_frame, text=info_text, justify=tk.LEFT, 
                              style='Normal.TLabel')
        info_label.pack(anchor='w')
    
    def update_label(self, var, label, format_str="{:.1f}"):
        """Update label with variable value"""
        try:
            value = var.get()
            if isinstance(value, int):
                label.config(text=str(value))
            else:
                label.config(text=format_str.format(value))
        except:
            pass
    
    def reset_to_defaults(self):
        """Reset to default values"""
        if messagebox.askyesno("Confirmar", "¿Resetear todos los valores por defecto?"):
            self.speed_var.set(1.8)
            self.sens_var.set(1.8)
            self.smooth_var.set(0.5)
            self.size_var.set('medium')
            self.click_sens_var.set(1.0)
            self.dist_var.set(0.35)
            self.cooldown_var.set(250)
            self.double_click_var.set(True)
            self.hand_var.set('auto')
            self.track_mode_var.set('smooth')
            self.show_landmarks_var.set(True)
            self.show_lines_var.set(True)
            self.show_fps_var.set(True)
            self.show_overlay_var.set(True)
            self.theme_var.set('modern_dark')
    
    def save_and_continue(self):
        """Save configuration and close"""
        self.config['cursor']['speed'] = self.speed_var.get()
        self.config['cursor']['sensitivity'] = self.sens_var.get()
        self.config['cursor']['smoothing'] = self.smooth_var.get()
        self.config['cursor']['size'] = self.size_var.get()
        
        self.config['click']['sensitivity'] = self.click_sens_var.get()
        self.config['click']['distance_threshold'] = self.dist_var.get()
        self.config['click']['cooldown_ms'] = self.cooldown_var.get()
        self.config['click']['double_click_enabled'] = self.double_click_var.get()
        
        self.config['hand_tracking']['dominant_hand'] = self.hand_var.get()
        self.config['hand_tracking']['tracking_mode'] = self.track_mode_var.get()
        
        self.config['visual']['theme'] = self.theme_var.get()
        
        self.config['visual']['show_landmarks'] = self.show_landmarks_var.get()
        self.config['visual']['show_lines'] = self.show_lines_var.get()
        self.config['visual']['show_fps'] = self.show_fps_var.get()
        self.config['visual']['show_overlay'] = self.show_overlay_var.get()
        
        self.save_config()
        self.result = self.config
        self.root.quit()
    
    def cancel(self):
        """Cancel and close"""
        self.result = None
        self.root.quit()
    
    def run(self):
        """Run the configuration UI"""
        self.create_ui()
        self.root.mainloop()
        return self.result

def show_quick_config():
    """Show quick configuration UI"""
    ui = QuickConfigUI()
    return ui.run()

if __name__ == "__main__":
    config = show_quick_config()
    if config:
        print("✅ Configuración guardada")
    else:
        print("❌ Configuración cancelada")
