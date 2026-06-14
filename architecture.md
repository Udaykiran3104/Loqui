# Loqui Architecture & Codebase Overview

This document provides a comprehensive overview of the **Loqui** Speech-To-Text application's architecture, detailing the role of each file and how the components interact.

## High-Level Architecture

Loqui is built as a multi-threaded, background-running Windows desktop application. Its core philosophy is to provide **blazing-fast, entirely offline, privacy-first** voice dictation with natural filler word elimination.

The architecture is divided into the following key layers:
1. **Input Layer**: Hotkey detection (`pynput`) and Audio Recording (`sounddevice`).
2. **Processing Layer**: Voice Activity Detection (Silero VAD) and Transcription (`faster-whisper`).
3. **Refinement Layer**: Post-processing (capitalization, punctuation, and filler word elimination).
4. **Output Layer**: Clipboard management and active window pasting (`pyautogui` / `xdotool`).
5. **UI & Management Layer**: System Tray controls (`pystray`), on-screen HUD (`tkinter`), and a First-Launch Setup Wizard.

---

## Folder Structure

```text
Loqui/
├── .venv/                  # Python virtual environment containing all dependencies
├── build/                  # Temporary PyInstaller build artifacts
├── dist/                   
│   └── Loqui/              # The final deployable standalone application folder
│       ├── _internal/      # Bundled Python runtime and dependencies
│       ├── Loqui.exe       # The compiled executable
│       └── config.yaml     # The live configuration file (auto-copied here)
├── main.py                 # The main entry point of the application
├── transcriber.py          # Whisper model initialization and transcription logic
├── vad.py                  # Voice Activity Detection (Silero VAD) logic
├── recorder.py             # Microphone audio capture logic
├── refiner.py              # Text post-processing and cleanup
├── output_handler.py       # Clipboard and keyboard simulation
├── hotkey_handler.py       # Global hotkey listening logic
├── tray_app.py             # System tray icon and context menu
├── overlay.py              # On-screen "Recording..." HUD widget
├── wizard.py               # First-launch "Setup Successful" UI
├── config.yaml             # Source configuration file
├── requirements.txt        # Python package dependencies
├── build.bat               # Windows batch script to compile the application
└── Loqui.spec              # PyInstaller specification file
```

---

## Component Breakdown (File by File)

### 1. `main.py`
The orchestrator of the entire application. It initializes all classes, reads the configuration, and sets up threading. It checks for the presence of the `.loqui_setup` file to determine whether to show the First-Launch Setup Wizard or start silently. It wires the hotkey press/release events to the recording and transcription functions.

### 2. `transcriber.py`
Contains the `Transcriber` class. This file is responsible for initializing the `faster-whisper` model (`base.en` by default). It loads the model into memory (using `int8` quantization for speed) and handles the core transcription of audio segments. It also passes the `initial_prompt` to naturally suppress filler words at the AI level.

### 3. `vad.py`
Contains the `trim_silence` function. It downloads and loads the PyTorch **Silero VAD** (Voice Activity Detection) model. Before audio is sent to Whisper, Silero analyzes the waveform to detect exact speech timestamps, stripping away leading and trailing silence. This makes transcription drastically faster and prevents hallucinations.

### 4. `recorder.py`
Contains the `AudioRecorder` class. Uses the `sounddevice` library to capture raw audio from the default Windows microphone at 16,000 Hz. It runs a background thread while the hotkey is held and saves the captured audio to a temporary `.wav` file in the system `%TEMP%` folder.

### 5. `refiner.py`
Contains the `TextRefiner` class. It takes the raw text output from Whisper and cleans it up. It applies auto-capitalization to the first word, ensures the sentence ends with a period, and uses regex to strip out any stubborn filler words defined in `config.yaml` that the Whisper prompt might have missed.

### 6. `output_handler.py`
Contains the `OutputHandler` class. It manages the final delivery of the text. It copies the refined text to the Windows Clipboard using `pyperclip` and then simulates a `Ctrl + V` keypress using `pyautogui` (or `xdotool` on Linux) to automatically type the text into whatever window the user currently has focused.

### 7. `hotkey_handler.py`
Contains the `HotkeyHandler` class. Uses `pynput` to globally monitor the keyboard for the configured hotkey combination (e.g., `Ctrl + Shift`). It ensures the hotkey works no matter what application is in focus.

### 8. `tray_app.py`
Contains the `TrayApp` class. Uses `pystray` to create the microphone icon in the Windows taskbar system tray. It handles user interactions like toggling the STT state (Enable/Disable) or fully exiting the application.

### 9. `overlay.py`
Contains the `Overlay` class. Uses `tkinter` to create a frameless, transparent, "always-on-top" UI widget at the bottom center of the screen. It displays the `🎙️ Recording...` indicator while the hotkey is held, providing immediate visual feedback to the user.

### 10. `wizard.py`
Contains the `SetupWizard` class. A premium, borderless `tkinter` window that appears only on the very first successful launch. It informs the user that the background model downloads were successful, provides brief usage instructions, and creates a hidden `.loqui_setup` flag when closed so it never interrupts the user again.

### 11. `config.yaml`
The central configuration file. It allows users to easily customize the application without touching Python code. It defines the hotkey combination, the Whisper model size (`base.en`), filler words to strip, and behavior toggles (like auto-pasting vs just copying).

### 12. `build.bat`
A Windows batch script that automates the deployment process. It runs PyInstaller with `--noconsole` and `--onedir` flags, collects all necessary hidden data (like PyTorch binaries and Faster-Whisper models), copies the `config.yaml` file, and outputs the final portable package to the `dist/Loqui` directory.
