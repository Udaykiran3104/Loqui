# Loqui: Project Overview

## What is Loqui?
**Loqui** (Latin for "to speak") is a blazing-fast, 100% local, privacy-first, open-source Speech-to-Text (STT) application for Windows desktop. It allows users to dictate text using their voice and seamlessly pastes the transcribed, refined text into any active application (like Microsoft Word, web browsers, Notepad, etc.).

## Why was it created?
Most high-quality speech-to-text solutions today are cloud-based (e.g., Google Cloud STT, OpenAI Whisper API). These services require an active internet connection, can be slow due to network latency, and most importantly, send your private voice data to third-party servers.

Loqui was created to solve these problems by providing:
1. **Privacy & Security**: 100% offline processing. No voice data ever leaves your computer.
2. **Speed**: By running locally and utilizing optimized AI models, it achieves near-instantaneous dictation.
3. **Seamless Integration**: Instead of opening a separate app to dictate and then copy-pasting, Loqui acts as a global background service that types directly into your active window.
4. **Natural Dictation**: It automatically removes filler words ("um", "uh") and applies basic punctuation and capitalization, reducing the need for manual editing.

## Requirements and Versions
The project is built on **Python 3.9+** and requires the following system specifications for optimal performance:
- **OS**: Windows 10 or Windows 11 (64-bit).
- **RAM**: Minimum 4GB (8GB recommended).
- **CPU**: Modern multi-core CPU (Intel i5 8th Gen or better). GPU is supported but not strictly required.
- **Disk Space**: ~1GB for the application and offline AI models.
- **Internet**: Only required *once* on the first launch to download the AI models (~76MB).

### Core Dependency Versions (see `requirements.txt`)
- `faster-whisper`: Used for CTranslate2-based Whisper transcription.
- `sounddevice`, `numpy`, `scipy`: For handling raw audio capture.
- `pynput`: For global hotkey detection.
- `pyautogui`, `pyperclip`, `plyer`: For clipboard manipulation, text pasting, and system notifications.
- `PyYAML`: For reading user configuration.
- `torch`, `torchaudio`, `torchcodec`: For the Silero Voice Activity Detection (VAD) model.
- `pystray`, `pillow`: For the system tray icon management.
- `pyinstaller`: For packaging the application into a standalone executable.

For a detailed breakdown of the internal pipeline, please see [PIPELINE_AND_ARCHITECTURE.md](./PIPELINE_AND_ARCHITECTURE.md). For a deep dive into each technology, see [TECHNOLOGIES.md](./TECHNOLOGIES.md).
