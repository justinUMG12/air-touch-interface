# Air Touch Interface v3.5 - PROFESSIONAL INSTALLATION GUIDE

## 📦 SYSTEM REQUIREMENTS

### Minimum Requirements
- **OS**: Windows 10 or Windows 11
- **Python**: 3.8, 3.9, 3.10, or 3.11
- **RAM**: 4 GB
- **Disk Space**: 500 MB
- **Camera**: Any USB camera or integrated webcam
- **Lighting**: Decent ambient lighting (300+ lux recommended)

### Recommended Requirements
- **OS**: Windows 11
- **Python**: 3.10 or 3.11
- **RAM**: 8 GB+
- **GPU**: NVIDIA CUDA-capable (optional, for acceleration)
- **Camera**: HD/Full HD USB camera
- **Lighting**: Good lighting (500-1000 lux)
- **Storage**: SSD for faster startup

---

## 🔧 INSTALLATION METHODS

### METHOD 1: QUICK START (RECOMMENDED)

**For users who just want to use it:**

1. Download the project folder
2. Double-click **`AirTouch.bat`**
3. Wait for initialization
4. Menu appears automatically
5. Select option **1** to start

**That's it! No technical setup needed.**

---

### METHOD 2: PYTHON + VIRTUAL ENVIRONMENT

**For Python developers:**

#### Step 1: Install Python
- Download Python 3.10+ from python.org
- **IMPORTANT**: Check "Add Python to PATH" during installation
- Verify: Open cmd and type `python --version`

#### Step 2: Create Virtual Environment
```bash
cd air_touch_interface
python -m venv airtouch_env
airtouch_env\Scripts\activate
```

#### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

This installs:
- opencv-python (4.9+)
- mediapipe (0.10+)
- pyautogui (0.9+)
- numpy (1.26+)

#### Step 4: Run Application
```bash
python launcher.py
```

---

### METHOD 3: STANDALONE EXE

**For distribution or no Python:**

#### Generate Executable
```bash
python build_exe.py
```

Then select option **1** to generate EXE.

**Requirements for EXE generation:**
```bash
pip install pyinstaller
```

The .exe will be created in `dist/AirTouch/` folder.

---

## 📋 REQUIREMENTS.TXT

Current requirements (automatically installed):

```
opencv-python==4.9.0.80
mediapipe==0.10.14
pyautogui==0.9.54
numpy==1.26.4
```

**Optional dependencies:**
```
PyInstaller==6.0  # For EXE generation
pywin32==306      # For Windows shortcuts
```

---

## 🚀 FIRST RUN CHECKLIST

- [ ] Python installed (3.8+)
- [ ] Python in PATH (`python --version` works)
- [ ] Camera connected and working
- [ ] Good lighting in room
- [ ] Sufficient disk space (500MB+)
- [ ] Virtual environment activated (if using venv)
- [ ] Dependencies installed (`pip show mediapipe` confirms)

---

## ✅ VERIFICATION STEPS

### Test 1: Python Installation
```bash
python --version
```
Should show: Python 3.8+ installed

### Test 2: Dependencies Check
```bash
python -c "import cv2, mediapipe, pyautogui, numpy; print('✅ All dependencies installed')"
```

### Test 3: Camera Detection
Run launcher → Menu option 3 (Diagnostics)

Checks:
- Camera detected
- MediaPipe working
- OpenCV installed
- PyAutoGUI responsive

### Test 4: Quick Test Run
```bash
python launcher.py
```

Select option 5 (Help) then return

---

## 🎯 STARTUP OPTIONS

### Option A: Double-Click Launcher
**File**: `AirTouch.bat`
- Opens professional menu
- All options available
- Recommended for users

### Option B: Direct Application
**File**: `start_airtouch.bat`
- Skips menu, starts directly
- Quick launch option
- For experienced users

### Option C: Python Direct
**Command**:
```bash
python launcher.py        # Full menu
python main.py            # Direct app
python settings_ui.py     # Settings only
```

### Option D: Standalone EXE
**File**: `dist/AirTouch/AirTouch.exe`
- No Python required
- Portable
- Ready for distribution

---

## 🔍 TROUBLESHOOTING INSTALLATION

### Python Not Recognized
**Error**: "python: command not found" or "'python' is not recognized"

**Solution**:
1. Reinstall Python
2. Check "Add Python to PATH"
3. Restart terminal/CMD
4. Verify: `python --version`

### Module Not Found
**Error**: "ModuleNotFoundError: No module named 'mediapipe'"

**Solution**:
```bash
# Ensure venv is activated (should see (airtouch_env) in prompt)
pip install --upgrade pip
pip install mediapipe opencv-python pyautogui numpy
```

### Camera Not Detected
**Error**: No camera found in diagnostics

**Solution**:
1. Check camera is connected
2. Test in Windows Camera app
3. Check Device Manager
4. Try different USB port
5. Update camera drivers

### Low Performance
**Error**: FPS too low (< 15)

**Solution**:
1. Close background applications
2. Lower camera resolution (Settings → Camera)
3. Use Power Saving mode
4. Check system resources (Task Manager)

### Virtual Environment Issues
**Error**: Scripts not activating

**Solution**:
```bash
# Delete and recreate
rmdir /s airtouch_env
python -m venv airtouch_env
airtouch_env\Scripts\activate
pip install -r requirements.txt
```

---

## 📦 FILE STRUCTURE AFTER INSTALLATION

```
air_touch_interface/
├── launcher.py                 ← Start here!
├── AirTouch.bat               ← Or double-click this
├── start_airtouch.bat
├── settings_ui.py
├── main.py
├── hand_tracker.py
├── cursor_controller.py
├── gesture_engine.py
├── utils.py
├── config_advanced.json
├── config.json
├── requirements.txt
├── build_exe.py
├── enhanced_cursor_controller.py
├── enhanced_hand_tracker.py
├── theme_system.py
├── professional_logging.py
├── airtouch_env/              ← Virtual environment (if used)
├── logs/                      ← Session logs created here
├── assets/
│   ├── sounds/
│   └── icons/
├── dist/                      ← EXE folder (if built)
└── README_v35.md
```

---

## 🔐 SECURITY NOTES

- **Local Processing**: All hand tracking runs locally
- **No Cloud**: Data doesn't leave your computer
- **No Telemetry**: Doesn't send usage data
- **Open Source**: Code is transparent

---

## 🎓 NEXT STEPS

After installation:

1. **Read Quick Start**: `QUICKSTART_v35.md`
2. **Run Diagnostics**: Menu → Option 3
3. **Configure Settings**: Menu → Option 2
4. **Learn Gestures**: Menu → Option 5 (Help)
5. **Start Using**: Menu → Option 1

---

## 💾 UPDATE & UPGRADE

### Updating Dependencies
```bash
pip install --upgrade mediapipe opencv-python pyautogui numpy
```

### Upgrading to New Version
1. Backup `config_advanced.json`
2. Download new version
3. Copy old config to new folder
4. Delete `airtouch_env` folder
5. Run fresh installation

---

## 🆘 GETTING HELP

### Resources
- `README_v35.md` - Full documentation
- `QUICKSTART_v35.md` - Quick start guide
- Menu option 5 - Built-in help
- Menu option 3 - Diagnostics

### Diagnostics Menu
Run: `python launcher.py`
Select: Option 3 (Diagnostics)

Checks all systems and suggests fixes.

---

## ⚡ QUICK COMMANDS

```bash
# Run launcher menu
python launcher.py

# Run application directly
python main.py

# Open settings
python settings_ui.py

# Run diagnostics
python -c "from professional_logging import *; initialize_logging(); get_diagnostics().run_full_diagnostics()"

# Build EXE
python build_exe.py

# Check Python version
python --version

# Check dependencies
pip list | find "mediapipe"
```

---

## 📞 SUPPORT CHECKLIST

If experiencing issues:

- [ ] Python 3.8+ installed
- [ ] Dependencies installed (pip list)
- [ ] Camera working (Windows Camera app)
- [ ] Good lighting in room
- [ ] Diagnostics passing (Menu → 3)
- [ ] Tried different profile
- [ ] Checked logs (Menu → 7)
- [ ] Restarted application

---

## 🎉 READY TO GO!

Installation complete! 

**Start here:**
```bash
python launcher.py
```

Or simply double-click: **`AirTouch.bat`**

Enjoy gesture control!

---

**For detailed usage, see:** `README_v35.md` and `QUICKSTART_v35.md`
