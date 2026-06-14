# Loqui: GitHub Developer Setup Guide

This guide is intended for developers who want to clone the Loqui repository from GitHub, run it from source, and contribute to the codebase.

## Prerequisites
Before you begin, ensure you have the following installed on your Windows machine:
1. **Git**: To clone the repository.
2. **Python 3.9 to 3.11**: (3.12+ may have compatibility issues with certain PyTorch/PyInstaller versions).
3. **A working microphone**: Set as the default recording device in Windows Sound Settings.

---

## 1. Clone the Repository

Open your terminal (PowerShell or Command Prompt) and clone the repository to your local machine:

```bash
git clone https://github.com/yourusername/loqui.git
cd loqui
```

---

## 2. Set Up a Virtual Environment

It is highly recommended to use a virtual environment to prevent dependency conflicts with other Python projects.

```bash
# Create a virtual environment named .venv
python -m venv .venv

# Activate the virtual environment
# On Command Prompt:
.\.venv\Scripts\activate.bat

# On PowerShell:
.\.venv\Scripts\Activate.ps1
```

*Note: If PowerShell blocks the script execution, run `Set-ExecutionPolicy Unrestricted -Scope CurrentUser` as Administrator first.*

---

## 3. Install Dependencies

With the virtual environment active, install all required packages using `pip`:

```bash
pip install -r requirements.txt
```

This will download essential libraries including `faster-whisper`, `torch`, `sounddevice`, `pynput`, and `pyinstaller`.

---

## 4. Initial Run & Model Download

The first time you run the application, it requires an active internet connection to download the required AI models (`base.en` Whisper model and Silero VAD model).

```bash
python main.py
```

- Watch the terminal output. You should see Hugging Face downloading the model weights into your `%USERPROFILE%\.cache` directory.
- Once the downloads complete (approx. 76MB), a graphical First-Launch Setup Wizard will appear.
- Click **"Get Started"** to close the wizard.
- You will see the Loqui microphone icon appear in your Windows System Tray (bottom right).

---

## 5. Test the Application

1. Open Notepad or click inside any text box.
2. Press and hold the default global hotkey: **`Ctrl + Shift`**.
3. A `🎙️ Recording...` overlay should appear at the bottom center of your screen.
4. Speak a test sentence (e.g., *"Hello world, this is a test of the dictation system."*).
5. Release the hotkey.
6. The application will transcribe your audio and automatically paste it into your active text box.

---

## 6. How to Build the Executable

If you have made changes and want to package the application into a `.exe` to share with non-developers:

1. Ensure your virtual environment is active.
2. Run the provided build batch script:
   ```cmd
   .\build.bat
   ```
3. PyInstaller will package the application in "Directory mode".
4. Once completed, navigate to the `dist\Loqui` folder. This entire folder is your standalone application.

For more details on how to deploy this built folder to other computers, read [deployment_guide.md](../deployment_guide.md).

---

## 7. Troubleshooting

- **`WinError 1314` from Hugging Face**: The application automatically sets environment variables to disable symlink warnings, so this should not occur. However, if it does, run your terminal as Administrator.
- **Audio Device Errors**: Ensure you don't have another application exclusively locking your microphone.
- **Background Crashes**: Since the built app runs without a console (`--noconsole`), errors are logged to `dist\Loqui\error.log`. Always check this file if the executable fails to launch.
