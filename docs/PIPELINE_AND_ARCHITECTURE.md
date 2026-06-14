# Loqui: Pipeline & Architecture

This document explains the flow of data within Loqui, detailing how a user's voice is captured, processed, and ultimately typed into an application.

## High-Level Pipeline

The pipeline of Loqui can be broken down into five distinct layers:

1. **Input & Trigger Layer**
   - The application constantly runs in the background.
   - `hotkey_handler.py` monitors system-wide keyboard events using `pynput`.
   - When the user presses and holds the configured global hotkey (e.g., `Ctrl + Shift`), a trigger is activated.
   - `overlay.py` immediately displays a non-intrusive "🎙️ Recording..." HUD widget on the screen using `tkinter`.
   - `recorder.py` begins capturing raw microphone audio using the `sounddevice` library at 16,000 Hz.

2. **Audio Pre-processing Layer (VAD)**
   - When the user releases the hotkey, the recording stops and the audio is saved to a temporary `.wav` file.
   - The audio is then passed to `vad.py`.
   - Here, the PyTorch **Silero VAD** (Voice Activity Detection) model analyzes the waveform.
   - It identifies the exact timestamps where speech occurs, effectively stripping away leading and trailing silence. This significantly speeds up the subsequent transcription phase and prevents AI hallucinations.

3. **Transcription Layer**
   - The trimmed audio is passed to `transcriber.py`.
   - Loqui uses `faster-whisper`, a highly optimized inference engine for OpenAI's Whisper model.
   - The audio is transcribed into text using the `base.en` model (or as configured in `config.yaml`).
   - A specific "initial prompt" is fed to the model to encourage it to naturally ignore conversational filler words during transcription.

4. **Refinement & Post-processing Layer**
   - The raw transcribed text is passed to `refiner.py`.
   - This layer acts as a safety net. It uses Regular Expressions (RegEx) to strip out any stubborn filler words ("um", "uh", "hmm") that the Whisper model might have missed.
   - It also ensures grammatical correctness by capitalizing the first word and appending an appropriate end-of-sentence punctuation mark (like a period).

5. **Output Delivery Layer**
   - Finally, the polished text is handed over to `output_handler.py`.
   - The text is copied to the Windows Clipboard using `pyperclip`.
   - The `pyautogui` library then simulates a physical `Ctrl + V` keypress.
   - Because the user released the hotkey while focused on their original application (e.g., Microsoft Word, Chrome), the text is instantly typed into their active text field.
   - Temporary audio files are deleted, and the application returns to a standby state.

## Application State Management

- **`main.py`**: The central orchestrator. It manages threading so the UI remains responsive while heavy AI transcription happens in the background.
- **System Tray (`tray_app.py`)**: Provides the user with a way to interact with the background service (Enable/Disable/Exit).
- **Setup Wizard (`wizard.py`)**: Runs only on the first launch. It acts as a friendly onboarding screen, verifying that all AI models were downloaded successfully.
