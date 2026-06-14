# Loqui Deployment Guide

This guide explains how to package, share, and set up the **Loqui** application on other Windows laptops.

---

## 1. What Files to Send

Because the application is packaged in **Directory mode** (to ensure the app launches instantly in under 2 seconds instead of taking 30+ seconds to extract on every launch), **you must share the entire `Loqui` directory**, not just the `.exe` file.

### Inside your project folder, locate:
`d:\Programming\STT\whispr-local\dist\Loqui`

This folder contains:
*   📁 **`_internal/`** — Contains the Python runtime, PyTorch, Pyinstaller dependencies, and libraries.
*   📄 **`Loqui.exe`** — The main executable application.
*   📄 **`config.yaml`** — The user configuration file (hotkeys, models, custom filler words).

### How to package it:
1. Go to `d:\Programming\STT\whispr-local\dist`.
2. Right-click the folder named **`Loqui`**.
3. Select **Compress to ZIP file** (or *Send to* -> *Compressed (zipped) folder*).
4. You will get a file named **`Loqui.zip`** (around 500-600MB due to PyTorch and deep learning libraries).
5. **Send this `Loqui.zip` file** to the other laptops (via USB drive, shared network folder, OneDrive/Google Drive, or email link).

---

## 2. Setting Up on Target Laptops

Follow these steps on the destination laptops to set up and run the application:

### Step A: Extract the Files
1. Copy the `Loqui.zip` file onto the target laptop.
2. Move it to a permanent folder, such as:
   *   `C:\Users\<Username>\Documents\Loqui` or `C:\Loqui`
3. **Right-click** on `Loqui.zip` and select **Extract All...** to extract the folder.
4. Open the extracted `Loqui` directory.

> [!WARNING]
> Do **NOT** run `Loqui.exe` directly inside the `.zip` file preview. It must be extracted first, otherwise it won't find the config file or dependencies, and will fail silently or crash.

### Step B: Run the Application (Online vs. Offline Mode)

The deep learning models (Whisper and Silero VAD) need to be loaded on startup. Choose **one** of the two methods below depending on the internet availability of the target laptop:

#### Method 1: Internet Connection (Easiest, Recommended)
On the very first launch, ensure the target laptop has an active internet connection.
1. Double-click **`Loqui.exe`**.
2. Windows Defender SmartScreen might pop up saying *"Windows protected your PC"* (since the binary is self-signed). Click **More Info** -> **Run anyway**.
3. The app will automatically connect to Hugging Face and PyTorch Hub, download the models (approx. 76MB total), and cache them locally.
4. Once downloaded, the **Loqui Setup Wizard** will pop up on the screen confirming the setup was successful! 
5. Click **Get Started** to close the wizard. 
6. **From now on**, the app is cached. The laptop can go completely offline, and subsequent launches will be instantaneous, showing only a brief "Loqui Active ✅" notification.

#### Method 2: Offline Setup (Without Internet)
If the target laptop has no internet access, you can copy the pre-downloaded model cache folders from your machine.
1. On your machine, press `Win + R`, paste `%USERPROFILE%\.cache`, and press Enter.
2. Locate these two directories:
   *   📁 `huggingface`
   *   📁 `torch`
3. Copy these folders to a USB drive.
4. On the target laptop, open the `%USERPROFILE%\.cache` directory (create the `.cache` folder if it doesn't exist under `C:\Users\<Username>\`).
5. Paste the `huggingface` and `torch` folders there.
6. Now, double-click **`Loqui.exe`** on the target laptop. The Setup Wizard will launch instantly!

---

## 3. Configuration & Customization

The user can open and edit the **`config.yaml`** file using Notepad on the target laptop to customize how it behaves:

*   **Change Hotkeys**: Edit the `hotkey.keys` list (e.g., change `["ctrl", "shift"]` to `["alt", "space"]`).
*   **Custom Filler Words**: Add/remove specific words under `refiner.filler_words` to remove words like *"um"*, *"uh"*, *"hmm"*, or specific words they repeat often.
*   **Model Options**: Change the `model.size` (e.g. from `"base.en"` to `"tiny.en"` for faster speeds on very old laptops, or `"small.en"` for higher accuracy on beefy machines).
*   **Behavior Toggles**: Change `auto_paste: false` if they want to copy only to clipboard without auto-typing it.

---

## 4. How to Use the Application

1. **Verify Launch**: Look at the Windows System Tray (bottom-right taskbar arrow). You should see the **Loqui icon** (a microphone/audio icon).
2. **To Disable/Enable**: Right-click the tray icon and toggle **STT Enabled**.
3. **To Exit**: Right-click the tray icon and click **Exit Application**.
4. **Recording Speech**:
   *   Place the mouse cursor inside any text field (Notepad, Word, web browser, etc.).
   *   **Press and hold** the hotkey (default: `Ctrl + Shift`).
   *   A semi-transparent overlay saying **`🎙️ Recording...`** will appear at the bottom-center of the screen.
   *   Speak your sentence.
   *   **Release** the hotkey. The overlay will disappear, the app will transcribe the recording, clean it up, and paste it into the active text field.

---

## 5. Troubleshooting & Log Files

If anything goes wrong or the Setup Wizard does not show up:
*   Inside the `Loqui` folder on the target laptop, check the **`error.log`** file.
*   This file automatically captures any runtime errors, network download timeouts, or hardware incompatibilities (like missing audio inputs).
*   If they get a crash, they can send you the `error.log` to see exactly what failed.
*   Make sure they have a working microphone set as the **Default Recording Device** in Windows Sound Settings.
