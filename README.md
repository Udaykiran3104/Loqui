# Loqui

A blazing-fast, 100% local, privacy-first, open-source Speech-to-Text application.
Loqui (Latin for "to speak") is designed to be a lightweight alternative to cloud-based dictation services. It runs completely offline on your Windows desktop, instantly transcribing your voice and seamlessly pasting it into any active application.

---

## 🌟 Features

*   **Lightning Fast & 100% Offline**: Uses `faster-whisper` (`base.en` model) to transcribe speech instantly without any network calls after the initial setup.
*   **Global Hotkey**: Press and hold `Ctrl + Shift` (or your custom combination) from anywhere in Windows to record.
*   **Auto-Typing**: Automatically copies the refined transcription to your clipboard and pastes it directly into your active text field (Word, Browser, Notepad).
*   **Smart Post-Processing**: 
    *   Auto-trims silence using PyTorch **Silero VAD**.
    *   Naturally eliminates filler words ("um", "hmm", "uh") at the AI-prompt level.
    *   Automatically capitalizes the first word and adds ending punctuation.
*   **System Tray Integration**: Runs silently in the background. Right-click the taskbar microphone icon to Enable/Disable or Exit.
*   **On-Screen HUD**: Displays a discrete, frameless `🎙️ Recording...` indicator while the hotkey is held.
*   **First-Launch Setup Wizard**: A beautiful UI that guides you through the initial setup process.
*   **Highly Customizable**: Edit the `config.yaml` file to change hotkeys, model sizes, and specific filler words.

---

## 🛠️ Technology Stack & Requirements

### Built With:
*   **Python 3.9+**
*   **faster-whisper**: For high-speed CTranslate2-based Whisper transcription.
*   **PyTorch (Silero VAD)**: For accurate Voice Activity Detection and silence trimming.
*   **pynput & pyautogui**: For global hotkey listening and keyboard simulation.
*   **tkinter & pystray**: For the On-Screen Display HUD and System Tray management.
*   **PyInstaller**: For packaging into a standalone Windows executable.

### System Requirements (For Deployment):
*   **OS**: Windows 10 or Windows 11 (64-bit).
*   **RAM**: At least 4GB (8GB recommended for larger Whisper models).
*   **CPU**: Modern multi-core CPU (Intel i5 8th Gen or better recommended).
*   **Internet**: Required *only* on the very first launch to download the AI models (~76MB).

---

## 🚀 Setup Instructions (For Developers)

If you want to run Loqui from source or modify the code:

1. **Clone the repository**:
   ```bash
   git clone https://github.com/Udaykiran3104/loqui.git
   cd loqui
   ```
2. **Create a virtual environment**:
   ```bash
   python -m venv .venv
   .\.venv\Scripts\activate
   ```
3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
4. **Run the Application**:
   ```bash
   python main.py
   ```
   *Note: On the first run, it will download the Whisper and Silero models to your `%USERPROFILE%\.cache` folder.*

---

## 📦 Build Instructions

To package Loqui into a standalone Windows executable that you can share with anyone:

1. Open a PowerShell or Command Prompt terminal in the project directory.
2. Ensure your virtual environment is active and requirements are installed.
3. Run the included build script:
   ```powershell
   .\build.bat
   ```
4. PyInstaller will compile the application. This process may take a few minutes.
5. Once complete, you will find a new folder at `dist\Loqui`.

---

## 🌍 Deployment

Because the application depends on large AI libraries, it is built in "Directory Mode" to ensure it launches instantly.

1. Navigate to `dist\Loqui`.
2. Right-click the `Loqui` folder and **Compress to ZIP file**.
3. Send this ZIP file to the target Windows laptop.
4. On the target laptop, **Extract** the ZIP file to a permanent location (e.g., `C:\Loqui`).
5. Double-click `Loqui.exe`. The Setup Wizard will appear upon successful initialization!

For more detailed deployment steps, including how to set up the application completely offline without internet, please read the included [deployment_guide.md](deployment_guide.md).

For an in-depth look at the codebase and folder structure, refer to [architecture.md](architecture.md).
