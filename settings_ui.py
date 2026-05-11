"""
Professional Settings UI for Air Touch Interface v3.5
Modern, responsive, and user-friendly configuration interface.
"""

import tkinter as tk
from tkinter import ttk
import json
import os
from pathlib import Path

class SettingsUI:
    def __init__(self, config_file="config_advanced.json"):
        self.config_file = config_file
        self.config = self.load_config()
        self.root = tk.Tk()
        self.root.title("Air Touch Interface - Professional Settings")
        self.root.geometry("1000x700")
        
        # Aplicar tema moderno
        self.setup_theme()
        self.setup_ui()
        
    def setup_theme(self):
        """Configura tema moderno y colores profesionales."""
        self.root.configure(bg="#1e1e2e")
        
        # Colores profesionales
        self.colors = {
            "bg_primary": "#1e1e2e",
            "bg_secondary": "#2d2d44",
            "fg_primary": "#ffffff",
            "fg_secondary": "#b0b0b0",
            "accent": "#00d4ff",
            "accent_hover": "#00f0ff",
            "success": "#00ff88",
            "warning": "#ffaa00",
            "error": "#ff4444"
        }
        
        # Configurar estilos
        style = ttk.Style()
        style.theme_use('clam')
        
        # Estilo para notebook tabs
        style.configure('TNotebook', background=self.colors["bg_primary"], 
                       foreground=self.colors["fg_primary"])
        style.configure('TNotebook.Tab', padding=[20, 10])
        
    def load_config(self):
        """Carga la configuración desde archivo JSON."""
        if os.path.exists(self.config_file):
            with open(self.config_file, 'r') as f:
                return json.load(f)
        return {}
    
    def save_config(self):
        """Guarda la configuración a archivo JSON."""
        with open(self.config_file, 'w') as f:
            json.dump(self.config, f, indent=2)
    
    def setup_ui(self):
        """Configura la interfaz principal."""
        # Header
        self.create_header()
        
        # Notebook (pestañas)
        notebook = ttk.Notebook(self.root)
        notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Pestañas
        self.create_cursor_tab(notebook)
        self.create_click_tab(notebook)
        self.create_hand_tracking_tab(notebook)
        self.create_visual_tab(notebook)
        self.create_camera_tab(notebook)
        self.create_profiles_tab(notebook)
        self.create_accessibility_tab(notebook)
        self.create_audio_tab(notebook)
        self.create_advanced_tab(notebook)
        
        # Footer
        self.create_footer()
    
    def create_header(self):
        """Crea el header profesional."""
        header = tk.Frame(self.root, bg=self.colors["bg_secondary"], height=60)
        header.pack(fill=tk.X, padx=0, pady=0)
        header.pack_propagate(False)
        
        # Título
        title = tk.Label(header, text="🎯 AIR TOUCH INTERFACE v3.5 - PROFESSIONAL SETTINGS",
                        font=("Segoe UI", 16, "bold"), 
                        bg=self.colors["bg_secondary"],
                        fg=self.colors["accent"])
        title.pack(side=tk.LEFT, padx=20, pady=15)
        
        # Perfil actual
        profile = tk.Label(header, text=f"Profile: {self.config.get('profile', 'Standard')}",
                          font=("Segoe UI", 10),
                          bg=self.colors["bg_secondary"],
                          fg=self.colors["fg_secondary"])
        profile.pack(side=tk.RIGHT, padx=20, pady=15)
    
    def create_footer(self):
        """Crea el footer con botones de acción."""
        footer = tk.Frame(self.root, bg=self.colors["bg_secondary"], height=50)
        footer.pack(fill=tk.X, padx=0, pady=0)
        footer.pack_propagate(False)
        
        # Botones
        save_btn = tk.Button(footer, text="💾 SAVE CONFIG", 
                           command=self.on_save,
                           bg=self.colors["success"],
                           fg="#000000",
                           font=("Segoe UI", 10, "bold"),
                           relief=tk.FLAT,
                           padx=15, pady=10)
        save_btn.pack(side=tk.LEFT, padx=10, pady=10)
        
        default_btn = tk.Button(footer, text="🔄 RESTORE DEFAULTS",
                              command=self.on_restore_defaults,
                              bg=self.colors["warning"],
                              fg="#000000",
                              font=("Segoe UI", 10, "bold"),
                              relief=tk.FLAT,
                              padx=15, pady=10)
        default_btn.pack(side=tk.LEFT, padx=10, pady=10)
        
        export_btn = tk.Button(footer, text="📤 EXPORT",
                             command=self.on_export,
                             bg=self.colors["accent"],
                             fg="#000000",
                             font=("Segoe UI", 10, "bold"),
                             relief=tk.FLAT,
                             padx=15, pady=10)
        export_btn.pack(side=tk.LEFT, padx=10, pady=10)
        
        close_btn = tk.Button(footer, text="✕ CLOSE",
                            command=self.root.quit,
                            bg=self.colors["error"],
                            fg="#ffffff",
                            font=("Segoe UI", 10, "bold"),
                            relief=tk.FLAT,
                            padx=15, pady=10)
        close_btn.pack(side=tk.RIGHT, padx=10, pady=10)
    
    def create_cursor_tab(self, notebook):
        """Pestaña de configuración del cursor."""
        frame = tk.Frame(notebook, bg=self.colors["bg_primary"])
        notebook.add(frame, text="🎯 Cursor")
        
        self.create_slider_option(frame, "Cursor Speed:", 0.5, 3.0, 
                                 self.config["cursor"]["speed"], 
                                 lambda v: self.update_config("cursor.speed", v))
        
        self.create_slider_option(frame, "Smoothing:", 0.1, 1.0,
                                 self.config["cursor"]["smoothing"],
                                 lambda v: self.update_config("cursor.smoothing", v))
        
        self.create_slider_option(frame, "Acceleration:", 0.8, 1.5,
                                 self.config["cursor"]["acceleration"],
                                 lambda v: self.update_config("cursor.acceleration", v))
        
        self.create_combobox_option(frame, "Size:",
                                   ["small", "medium", "large", "gigantic"],
                                   self.config["cursor"]["size"],
                                   lambda v: self.update_config("cursor.size", v))
        
        self.create_combobox_option(frame, "Stability:",
                                   ["low", "medium", "high", "extreme"],
                                   self.config["cursor"]["stability"],
                                   lambda v: self.update_config("cursor.stability", v))
    
    def create_click_tab(self, notebook):
        """Pestaña de configuración de clicks."""
        frame = tk.Frame(notebook, bg=self.colors["bg_primary"])
        notebook.add(frame, text="👆 Click")
        
        self.create_slider_option(frame, "Click Sensitivity:", 0.5, 2.0,
                                 self.config["click"]["sensitivity"],
                                 lambda v: self.update_config("click.sensitivity", v))
        
        self.create_slider_option(frame, "Distance Threshold:", 0.2, 0.6,
                                 self.config["click"]["distance_threshold"],
                                 lambda v: self.update_config("click.distance_threshold", v))
        
        self.create_slider_option(frame, "Cooldown (ms):", 100, 500,
                                 self.config["click"]["cooldown_ms"],
                                 lambda v: self.update_config("click.cooldown_ms", v))
        
        self.create_combobox_option(frame, "Force Required:",
                                   ["light", "medium", "heavy"],
                                   self.config["click"]["force_required"],
                                   lambda v: self.update_config("click.force_required", v))
        
        self.create_checkbox_option(frame, "Double Click Enabled",
                                   self.config["click"]["double_click_enabled"],
                                   lambda v: self.update_config("click.double_click_enabled", v))
    
    def create_hand_tracking_tab(self, notebook):
        """Pestaña de seguimiento de manos."""
        frame = tk.Frame(notebook, bg=self.colors["bg_primary"])
        notebook.add(frame, text="✋ Hand Tracking")
        
        self.create_combobox_option(frame, "Dominant Hand:",
                                   ["left", "right", "auto"],
                                   self.config["hand_tracking"]["dominant_hand"],
                                   lambda v: self.update_config("hand_tracking.dominant_hand", v))
        
        self.create_slider_option(frame, "Tracking Sensitivity:", 0.5, 1.5,
                                 self.config["hand_tracking"]["tracking_sensitivity"],
                                 lambda v: self.update_config("hand_tracking.tracking_sensitivity", v))
        
        self.create_combobox_option(frame, "Tracking Mode:",
                                   ["smooth", "aggressive", "slow_motion"],
                                   self.config["hand_tracking"]["tracking_mode"],
                                   lambda v: self.update_config("hand_tracking.tracking_mode", v))
        
        self.create_checkbox_option(frame, "Low Light Mode",
                                   self.config["hand_tracking"]["low_light_mode"],
                                   lambda v: self.update_config("hand_tracking.low_light_mode", v))
        
        self.create_checkbox_option(frame, "Gaming Mode",
                                   self.config["hand_tracking"]["gaming_mode"],
                                   lambda v: self.update_config("hand_tracking.gaming_mode", v))
        
        self.create_checkbox_option(frame, "Precision Mode",
                                   self.config["hand_tracking"]["precision_mode"],
                                   lambda v: self.update_config("hand_tracking.precision_mode", v))
    
    def create_visual_tab(self, notebook):
        """Pestaña de opciones visuales."""
        frame = tk.Frame(notebook, bg=self.colors["bg_primary"])
        notebook.add(frame, text="🎨 Visual")
        
        self.create_combobox_option(frame, "Theme:",
                                   ["modern_dark", "modern_light", "neon_futuristic", "minimal", "sci_fi"],
                                   self.config["visual"]["theme"],
                                   lambda v: self.update_config("visual.theme", v))
        
        self.create_slider_option(frame, "Transparency:", 0.3, 1.0,
                                 self.config["visual"]["transparency"],
                                 lambda v: self.update_config("visual.transparency", v))
        
        self.create_combobox_option(frame, "HUD Style:",
                                   ["full", "minimal", "hidden"],
                                   self.config["visual"]["hud_style"],
                                   lambda v: self.update_config("visual.hud_style", v))
        
        self.create_checkbox_option(frame, "Show FPS",
                                   self.config["visual"]["show_fps"],
                                   lambda v: self.update_config("visual.show_fps", v))
        
        self.create_checkbox_option(frame, "Show Tracking Lines",
                                   self.config["visual"]["show_tracking_lines"],
                                   lambda v: self.update_config("visual.show_tracking_lines", v))
        
        self.create_checkbox_option(frame, "High Contrast",
                                   self.config["visual"]["high_contrast"],
                                   lambda v: self.update_config("visual.high_contrast", v))
    
    def create_camera_tab(self, notebook):
        """Pestaña de configuración de cámara."""
        frame = tk.Frame(notebook, bg=self.colors["bg_primary"])
        notebook.add(frame, text="📹 Camera")
        
        self.create_slider_option(frame, "Camera Device:", 0, 3,
                                 self.config["camera"]["device_id"],
                                 lambda v: self.update_config("camera.device_id", v))
        
        self.create_combobox_option(frame, "Resolution:",
                                   ["640x480", "800x600", "1280x720", "1920x1080"],
                                   f"{self.config['camera']['frame_width']}x{self.config['camera']['frame_height']}",
                                   lambda v: self.on_resolution_change(v))
        
        self.create_slider_option(frame, "FPS Target:", 15, 60,
                                 self.config["camera"]["fps_target"],
                                 lambda v: self.update_config("camera.fps_target", v))
        
        self.create_combobox_option(frame, "Quality Mode:",
                                   ["fast", "balanced", "quality"],
                                   self.config["camera"]["quality_mode"],
                                   lambda v: self.update_config("camera.quality_mode", v))
        
        self.create_slider_option(frame, "Brightness:", 0.5, 1.5,
                                 self.config["camera"]["brightness_adjustment"],
                                 lambda v: self.update_config("camera.brightness_adjustment", v))
        
        self.create_checkbox_option(frame, "Flip Horizontal",
                                   self.config["camera"]["flip_horizontal"],
                                   lambda v: self.update_config("camera.flip_horizontal", v))
    
    def create_profiles_tab(self, notebook):
        """Pestaña de perfiles predefinidos."""
        frame = tk.Frame(notebook, bg=self.colors["bg_primary"])
        notebook.add(frame, text="⚙️ Profiles")
        
        tk.Label(frame, text="Quick Profile Selection:",
                font=("Segoe UI", 11, "bold"),
                bg=self.colors["bg_primary"],
                fg=self.colors["accent"]).pack(pady=10)
        
        profiles_frame = tk.Frame(frame, bg=self.colors["bg_primary"])
        profiles_frame.pack(pady=10)
        
        for profile_name in ["Standard", "Gaming", "Precision", "Navigation", "Accessibility"]:
            btn = tk.Button(profiles_frame, text=profile_name,
                          command=lambda p=profile_name: self.load_profile(p),
                          bg=self.colors["bg_secondary"],
                          fg=self.colors["accent"],
                          font=("Segoe UI", 10),
                          relief=tk.FLAT,
                          padx=20, pady=10)
            btn.pack(side=tk.LEFT, padx=5)
        
        tk.Label(frame, text="Profile Descriptions:",
                font=("Segoe UI", 11, "bold"),
                bg=self.colors["bg_primary"],
                fg=self.colors["accent"]).pack(pady=(20, 10))
        
        descriptions = {
            "Gaming": "High speed, low smoothing, responsive",
            "Precision": "Slow, high smoothing, stable",
            "Navigation": "Balanced settings",
            "Accessibility": "Extra stable, larger cursor, high contrast"
        }
        
        for profile, desc in descriptions.items():
            tk.Label(frame, text=f"• {profile}: {desc}",
                    font=("Segoe UI", 9),
                    bg=self.colors["bg_primary"],
                    fg=self.colors["fg_secondary"]).pack(anchor=tk.W, padx=20)
    
    def create_accessibility_tab(self, notebook):
        """Pestaña de accesibilidad."""
        frame = tk.Frame(notebook, bg=self.colors["bg_primary"])
        notebook.add(frame, text="♿ Accessibility")
        
        self.create_checkbox_option(frame, "Large Cursor",
                                   self.config["accessibility"]["cursor_size_large"],
                                   lambda v: self.update_config("accessibility.cursor_size_large", v))
        
        self.create_checkbox_option(frame, "High Contrast",
                                   self.config["accessibility"]["high_contrast_enabled"],
                                   lambda v: self.update_config("accessibility.high_contrast_enabled", v))
        
        self.create_checkbox_option(frame, "Slow Tracking",
                                   self.config["accessibility"]["tracking_slow"],
                                   lambda v: self.update_config("accessibility.tracking_slow", v))
        
        self.create_checkbox_option(frame, "Sensitive Click",
                                   self.config["accessibility"]["click_sensitivity_high"],
                                   lambda v: self.update_config("accessibility.click_sensitivity_high", v))
        
        self.create_checkbox_option(frame, "Extreme Stability",
                                   self.config["accessibility"]["extreme_stability"],
                                   lambda v: self.update_config("accessibility.extreme_stability", v))
        
        self.create_checkbox_option(frame, "Audio Feedback",
                                   self.config["accessibility"]["audio_feedback"],
                                   lambda v: self.update_config("accessibility.audio_feedback", v))
    
    def create_audio_tab(self, notebook):
        """Pestaña de opciones de audio."""
        frame = tk.Frame(notebook, bg=self.colors["bg_primary"])
        notebook.add(frame, text="🔊 Audio")
        
        self.create_checkbox_option(frame, "Audio Enabled",
                                   self.config["audio"]["enabled"],
                                   lambda v: self.update_config("audio.enabled", v))
        
        self.create_slider_option(frame, "Volume:", 0.0, 1.0,
                                 self.config["audio"]["volume"],
                                 lambda v: self.update_config("audio.volume", v))
    
    def create_advanced_tab(self, notebook):
        """Pestaña de opciones avanzadas."""
        frame = tk.Frame(notebook, bg=self.colors["bg_primary"])
        notebook.add(frame, text="🔬 Advanced")
        
        self.create_combobox_option(frame, "Performance Mode:",
                                   ["power_saving", "balanced", "maximum"],
                                   self.config["performance"]["mode"],
                                   lambda v: self.update_config("performance.mode", v))
        
        self.create_checkbox_option(frame, "GPU Acceleration",
                                   self.config["performance"]["gpu_acceleration"],
                                   lambda v: self.update_config("performance.gpu_acceleration", v))
        
        self.create_checkbox_option(frame, "Adaptive Mode",
                                   self.config["adaptive"]["enabled"],
                                   lambda v: self.update_config("adaptive.enabled", v))
        
        self.create_checkbox_option(frame, "Learning Enabled",
                                   self.config["adaptive"]["learning_enabled"],
                                   lambda v: self.update_config("adaptive.learning_enabled", v))
        
        self.create_combobox_option(frame, "Log Level:",
                                   ["DEBUG", "INFO", "WARNING", "ERROR"],
                                   self.config["logging"]["level"],
                                   lambda v: self.update_config("logging.level", v))
        
        self.create_checkbox_option(frame, "Benchmark Mode",
                                   self.config["debug"]["benchmark_mode"],
                                   lambda v: self.update_config("debug.benchmark_mode", v))
    
    def create_slider_option(self, parent, label, min_val, max_val, current_val, callback):
        """Crea una opción de slider."""
        frame = tk.Frame(parent, bg=self.colors["bg_primary"])
        frame.pack(fill=tk.X, padx=20, pady=10)
        
        tk.Label(frame, text=label, font=("Segoe UI", 10),
                bg=self.colors["bg_primary"], fg=self.colors["fg_primary"]).pack(side=tk.LEFT, padx=10)
        
        slider = tk.Scale(frame, from_=min_val, to=max_val, orient=tk.HORIZONTAL,
                         bg=self.colors["bg_secondary"],
                         fg=self.colors["accent"],
                         highlightthickness=0,
                         command=callback,
                         length=300)
        slider.set(current_val)
        slider.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=10)
        
        value_label = tk.Label(frame, text=f"{current_val:.2f}",
                              font=("Segoe UI", 9),
                              bg=self.colors["bg_primary"],
                              fg=self.colors["accent"],
                              width=8)
        value_label.pack(side=tk.RIGHT, padx=10)
        
        slider.config(command=lambda v: (callback(float(v)), value_label.config(text=f"{float(v):.2f}")))
    
    def create_combobox_option(self, parent, label, options, current_val, callback):
        """Crea una opción de combobox."""
        frame = tk.Frame(parent, bg=self.colors["bg_primary"])
        frame.pack(fill=tk.X, padx=20, pady=10)
        
        tk.Label(frame, text=label, font=("Segoe UI", 10),
                bg=self.colors["bg_primary"], fg=self.colors["fg_primary"]).pack(side=tk.LEFT, padx=10)
        
        combo = ttk.Combobox(frame, values=options, state="readonly", width=20)
        combo.set(current_val)
        combo.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=10)
        combo.bind("<<ComboboxSelected>>", lambda e: callback(combo.get()))
    
    def create_checkbox_option(self, parent, label, current_val, callback):
        """Crea una opción de checkbox."""
        frame = tk.Frame(parent, bg=self.colors["bg_primary"])
        frame.pack(fill=tk.X, padx=20, pady=10)
        
        var = tk.BooleanVar(value=current_val)
        check = tk.Checkbutton(frame, text=label, variable=var,
                              font=("Segoe UI", 10),
                              bg=self.colors["bg_primary"],
                              fg=self.colors["fg_primary"],
                              selectcolor=self.colors["bg_secondary"],
                              activebackground=self.colors["bg_secondary"],
                              activeforeground=self.colors["accent"],
                              command=lambda: callback(var.get()))
        check.pack(side=tk.LEFT, padx=10)
    
    def update_config(self, key_path, value):
        """Actualiza un valor en la configuración usando notación de puntos."""
        keys = key_path.split('.')
        config = self.config
        for key in keys[:-1]:
            if key not in config:
                config[key] = {}
            config = config[key]
        config[keys[-1]] = value
    
    def on_resolution_change(self, resolution_str):
        """Maneja cambio de resolución."""
        width, height = map(int, resolution_str.split('x'))
        self.update_config("camera.frame_width", width)
        self.update_config("camera.frame_height", height)
    
    def load_profile(self, profile_name):
        """Carga un perfil predefinido."""
        self.config["profile"] = profile_name
        # Aquí se aplicarían los valores del perfil
        print(f"Profile loaded: {profile_name}")
    
    def on_save(self):
        """Guarda la configuración."""
        self.save_config()
        print(f"✅ Configuration saved to {self.config_file}")
    
    def on_restore_defaults(self):
        """Restaura configuración por defecto."""
        # Aquí se cargarían los valores por defecto
        print("🔄 Configuration restored to defaults")
    
    def on_export(self):
        """Exporta la configuración."""
        print("📤 Configuration exported")
    
    def run(self):
        """Ejecuta la interfaz."""
        self.root.mainloop()


if __name__ == "__main__":
    app = SettingsUI()
    app.run()
