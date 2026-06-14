# Loqui: Technologies Used

This document outlines all the major technologies and libraries used to build Loqui, explaining *what* they are and *why* they were chosen for this specific project.

## Core Language & Build Tools

### Python (3.9+)
- **What it is**: A high-level, versatile programming language.
- **Why we used it**: Python is the absolute standard for AI and machine learning integration. It offers the richest ecosystem of libraries for speech recognition, audio processing, and OS-level automation, allowing rapid development of this application.

### PyInstaller
- **What it is**: A tool that bundles a Python application and all its dependencies into a single package.
- **Why we used it**: To distribute Loqui to end-users on Windows, they shouldn't need to install Python, Pip, or any virtual environments. PyInstaller compiles the entire project into a standalone executable (`.exe`), making deployment a simple drag-and-drop process.

---

## AI & Audio Processing

### Faster-Whisper
- **What it is**: A reimplementation of OpenAI's Whisper model using `CTranslate2`, which is a fast inference engine for Transformer models.
- **Why we used it**: Standard `openai-whisper` is too slow for real-time dictation, especially on CPUs. `faster-whisper` provides up to 4x faster transcription with significantly lower memory usage. This is the core engine that turns the user's voice into text completely offline.

### PyTorch (`torch`, `torchaudio`)
- **What it is**: A premier open-source machine learning framework developed by Meta.
- **Why we used it**: PyTorch is required to run the Silero VAD model. It provides the deep learning backend needed to analyze audio tensors.

### Silero VAD
- **What it is**: An enterprise-grade Voice Activity Detection model.
- **Why we used it**: When a user holds a hotkey, they might not speak immediately, or might hold it for a second after finishing. Sending empty silence to Whisper causes hallucinations and wastes processing time. Silero VAD perfectly crops the audio so *only* the spoken words are sent to Whisper.

### SoundDevice & NumPy / SciPy
- **What it is**: Libraries for reading and writing audio arrays.
- **Why we used it**: To record audio from the Windows microphone in real-time. `sounddevice` provides low-latency audio capture, and `numpy`/`scipy` help format the raw audio data into standard `.wav` files at the required 16,000 Hz sample rate.

---

## Operating System Integration

### Pynput
- **What it is**: A library that allows you to control and monitor input devices.
- **Why we used it**: To create the global hotkey mechanism. Loqui needs to know when the user presses `Ctrl + Shift` even if Loqui is hidden in the background and the user is typing in Google Chrome. `pynput` listens to system-wide keyboard events.

### PyAutoGUI & Pyperclip
- **What it is**: Libraries for cross-platform GUI automation and clipboard management.
- **Why we used it**: To achieve the "Auto-Typing" feature. `pyperclip` quietly places the transcribed text into the Windows clipboard. `pyautogui` then instantly simulates the keyboard pressing `Ctrl + V`, effectively pasting the text into whatever application the user is currently using.

### PyStray & Pillow
- **What it is**: `pystray` creates system tray icons, and `Pillow` is an image processing library.
- **Why we used it**: Because Loqui is a background service, it shouldn't have a constant window taking up taskbar space. `pystray` places a small microphone icon in the system tray (bottom right corner of Windows) for the user to access settings or exit the app.

### Tkinter
- **What it is**: Python's de-facto standard GUI package.
- **Why we used it**: Used for creating the On-Screen Display (OSD). The semi-transparent `🎙️ Recording...` overlay and the First-Launch Setup Wizard are both built with `tkinter` because it is lightweight and comes pre-installed with Python, requiring no heavy external UI frameworks like Qt.

---

## Configuration

### PyYAML
- **What it is**: A YAML parser and emitter for Python.
- **Why we used it**: To parse `config.yaml`. YAML was chosen over JSON because it is much more readable and easier for non-technical end-users to edit (e.g., to change their hotkeys or add custom filler words).
