"""
Air Touch Interface - EXE Generator and Shortcut Creator
Creates standalone EXE and Windows shortcuts for easy distribution.
"""

import os
import sys
from pathlib import Path
import json
import subprocess
import shutil
import time


class ExeGenerator:
    """Genera un ejecutable standalone usando PyInstaller."""
    
    def __init__(self, app_dir=None):
        self.app_dir = Path(app_dir) if app_dir else Path.cwd()
        self.dist_dir = self.app_dir / "dist"
        self.build_dir = self.app_dir / "build"
        
    def check_pyinstaller(self):
        """Verifica si PyInstaller está instalado."""
        try:
            import PyInstaller
            return True
        except ImportError:
            print("❌ PyInstaller not found")
            print("Installing PyInstaller...")
            os.system(f"{sys.executable} -m pip install pyinstaller")
            return True
    
    def generate_spec_file(self):
        """Genera archivo spec para PyInstaller."""
        spec_content = """# -*- mode: python ; coding: utf-8 -*-
import sys
from pathlib import Path

a = Analysis(
    ['launcher.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('config_advanced.json', '.'),
        ('assets', 'assets'),
        ('themes', 'themes'),
        ('profiles', 'profiles'),
    ],
    hiddenimports=['mediapipe', 'cv2', 'pyautogui', 'numpy'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludedimports=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=None)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='AirTouch',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='assets/icon.ico' if Path('assets/icon.ico').exists() else None,
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='AirTouch'
)
"""
        spec_file = self.app_dir / "AirTouch.spec"
        with open(spec_file, 'w') as f:
            f.write(spec_content)
        return spec_file
    
    def generate_exe(self):
        """Genera el ejecutable."""
        print("\n" + "="*60)
        print("📦 GENERATING EXECUTABLE")
        print("="*60 + "\n")
        
        if not self.check_pyinstaller():
            return False
        
        print("📝 Generating spec file...")
        spec_file = self.generate_spec_file()
        
        print("⏳ Building executable...")
        print("   This may take a few minutes...\n")
        
        os.chdir(self.app_dir)
        result = os.system(f"pyinstaller {spec_file}")
        
        if result == 0:
            print("\n✅ Executable generated successfully!")
            exe_path = self.dist_dir / "AirTouch" / "AirTouch.exe"
            print(f"📍 Location: {exe_path}")
            return True
        else:
            print("\n❌ Executable generation failed")
            return False
    
    def cleanup(self):
        """Limpia archivos temporales."""
        print("\n🧹 Cleaning up temporary files...")
        if self.build_dir.exists():
            shutil.rmtree(self.build_dir)
        
        spec_file = self.app_dir / "AirTouch.spec"
        if spec_file.exists():
            spec_file.unlink()
        
        print("✅ Cleanup complete")


class ShortcutCreator:
    """Crea accesos directos de Windows."""
    
    @staticmethod
    def create_shortcut(target_path, shortcut_path, description="", icon_path=None):
        """Crea un acceso directo de Windows."""
        try:
            import win32com.client
            shell = win32com.client.Dispatch("WScript.Shell")
            
            shortcut = shell.CreateShortCut(str(shortcut_path))
            shortcut.TargetPath = str(target_path)
            shortcut.WorkingDirectory = str(Path(target_path).parent)
            shortcut.Description = description
            
            if icon_path and Path(icon_path).exists():
                shortcut.IconLocation = str(icon_path)
            
            shortcut.save()
            return True
        except Exception as e:
            print(f"❌ Failed to create shortcut: {str(e)}")
            return False
    
    @staticmethod
    def create_powershell_shortcut(target_path, shortcut_path, description=""):
        """Crea acceso directo usando PowerShell como fallback."""
        try:
            ps_script = f"""
            $shell = New-Object -ComObject WScript.Shell
            $shortcut = $shell.CreateShortCut('{shortcut_path}')
            $shortcut.TargetPath = '{target_path}'
            $shortcut.Description = '{description}'
            $shortcut.Save()
            """
            
            ps_file = Path(shortcut_path).parent / "create_shortcut.ps1"
            with open(ps_file, 'w') as f:
                f.write(ps_script)
            
            os.system(f"powershell -ExecutionPolicy Bypass -File {ps_file}")
            ps_file.unlink()
            return True
        except Exception as e:
            print(f"❌ Failed to create shortcut: {str(e)}")
            return False


class SetupBuilder:
    """Construye el paquete de distribución."""
    
    def __init__(self, app_dir=None):
        self.app_dir = Path(app_dir) if app_dir else Path.cwd()
        self.dist_path = self.app_dir / "dist"
    
    def create_directories(self):
        """Crea estructura de directorios."""
        print("\n📁 Creating directory structure...")
        
        dirs = [
            "assets/sounds",
            "assets/icons",
            "themes",
            "profiles",
            "logs",
        ]
        
        for dir_path in dirs:
            (self.app_dir / dir_path).mkdir(parents=True, exist_ok=True)
        
        print("✅ Directories created")
    
    def create_desktop_shortcut(self):
        """Crea acceso directo en el escritorio."""
        print("\n🔗 Creating desktop shortcut...")
        
        desktop_path = Path.home() / "Desktop"
        shortcut_path = desktop_path / "Air Touch Interface.lnk"
        
        # Intentar con pywin32
        creator = ShortcutCreator()
        
        # Determinar path del ejecutable
        if (self.app_dir / "dist" / "AirTouch" / "AirTouch.exe").exists():
            target = self.app_dir / "dist" / "AirTouch" / "AirTouch.exe"
        else:
            target = self.app_dir / "AirTouch.bat"
        
        success = creator.create_shortcut(
            target,
            shortcut_path,
            "Air Touch Interface - Control Windows with Gestures",
            self.app_dir / "assets" / "icons" / "airtouch.ico" if (self.app_dir / "assets" / "icons" / "airtouch.ico").exists() else None
        )
        
        if not success:
            # Fallback to PowerShell
            success = creator.create_powershell_shortcut(
                str(target),
                str(shortcut_path),
                "Air Touch Interface"
            )
        
        if success:
            print(f"✅ Desktop shortcut created: {shortcut_path}")
        else:
            print("⚠️  Could not create desktop shortcut automatically")
        
        return success


def main():
    """Programa principal."""
    print("\n" + "="*60)
    print("  AIR TOUCH INTERFACE - BUILD & DISTRIBUTION TOOL")
    print("="*60)
    print("\nOptions:")
    print("  1. Generate EXE")
    print("  2. Create Desktop Shortcut")
    print("  3. Setup Complete Distribution")
    print("  4. Clean Build Files")
    print("  5. Exit")
    
    choice = input("\nSelect option (1-5): ").strip()
    
    if choice == "1":
        generator = ExeGenerator()
        if generator.generate_exe():
            generator.cleanup()
        else:
            print("❌ Build failed")
    
    elif choice == "2":
        setup = SetupBuilder()
        setup.create_desktop_shortcut()
    
    elif choice == "3":
        setup = SetupBuilder()
        setup.create_directories()
        
        generator = ExeGenerator()
        if generator.generate_exe():
            generator.cleanup()
            setup.create_desktop_shortcut()
        else:
            print("❌ Build failed")
    
    elif choice == "4":
        generator = ExeGenerator()
        if generator.build_dir.exists():
            shutil.rmtree(generator.build_dir)
        if generator.dist_dir.exists():
            shutil.rmtree(generator.dist_dir)
        print("✅ Build files cleaned")
    
    elif choice == "5":
        print("👋 Goodbye!")
        return
    
    else:
        print("❌ Invalid option")
    
    print("\n✅ Done!")


if __name__ == "__main__":
    main()
