import os, time, threading, sys

# Fix for HuggingFace caching on Windows without admin privileges (WinError 1314)
os.environ["HF_HUB_DISABLE_SYMLINKS_WARNING"] = "1"
os.environ["HF_HUB_DISABLE_SYMLINKS"] = "1"

# Fix for PyInstaller --noconsole mode: redirect to a local log file instead of devnull
# This helps debug background crashes.
log_path = "error.log"
if getattr(sys, 'frozen', False):
    log_path = os.path.join(os.path.dirname(sys.executable), "error.log")

log_file = open(log_path, 'a', encoding='utf-8')

if sys.stdout is None:
    sys.stdout = log_file
if sys.stderr is None:
    sys.stderr = log_file

from recorder import AudioRecorder
from transcriber import Transcriber
from refiner import TextRefiner
from output_handler import OutputHandler
from hotkey_handler import HotkeyHandler
from vad import trim_silence
from overlay import Overlay
from tray_app import TrayApp

def get_config_path():
    if getattr(sys, 'frozen', False):
        # Running as compiled EXE
        exe_dir = os.path.dirname(sys.executable)
        config_next_to_exe = os.path.join(exe_dir, "config.yaml")
        if os.path.exists(config_next_to_exe):
            return config_next_to_exe
        return os.path.join(sys._MEIPASS, "config.yaml")
    # Running as script
    return "config.yaml"

CONFIG = get_config_path()

recorder = AudioRecorder()
transcriber = Transcriber(CONFIG)      # loads Whisper model once at startup
refiner = TextRefiner(CONFIG)
output = OutputHandler(CONFIG)
hotkey = HotkeyHandler(CONFIG)
overlay = Overlay()

_recording = False
_stt_enabled = True
_lock = threading.Lock()

def on_hotkey_press():
    global _recording
    if not _stt_enabled:
        return
        
    with _lock:
        if not _recording:
            _recording = True
            overlay.show()
            recorder.start()

def on_hotkey_release():
    global _recording
    if not _stt_enabled:
        return
        
    with _lock:
        if _recording:
            _recording = False
            overlay.hide()

            # Do heavy work off the main thread so keys remain responsive
            threading.Thread(target=process_audio, daemon=True).start()

def process_audio():
    wav_path = recorder.stop()
    clean_path = None
    try:
        # Optional: trim silence edges
        clean_path = trim_silence(wav_path)

        # Transcribe
        raw_text = transcriber.transcribe(clean_path)
        print(f"🗣️  Raw: {raw_text}")

        # Refine
        refined = refiner.refine(raw_text)
        print(f"✨ Refined: {refined}")

        # Deliver to clipboard / active window
        output.deliver(refined)
    finally:
        # Clean up temp files
        for p in [wav_path, clean_path]:
            if p and os.path.exists(p):
                try:
                    os.remove(p)
                except Exception:
                    pass

def on_quit():
    hotkey.stop()
    print("\n👋 Stopped.")
    os._exit(0)

def on_toggle(enabled):
    global _stt_enabled
    _stt_enabled = enabled
    print(f"STT Enabled: {_stt_enabled}")

if __name__ == "__main__":
    print("🚀 Loqui started — running in background")
    
    overlay.start()
    
    exe_dir = "."
    if getattr(sys, 'frozen', False):
        exe_dir = os.path.dirname(sys.executable)
    flag_path = os.path.join(exe_dir, ".loqui_setup")
    
    def notify_success():
        time.sleep(0.5)
        overlay.show_message("Loqui Active ✅", 3000)

    # Check if first time setup is needed
    if not os.path.exists(flag_path):
        from wizard import SetupWizard
        
        def _on_wizard_close():
            threading.Thread(target=notify_success, daemon=True).start()
            
        wizard = SetupWizard(on_close_callback=_on_wizard_close)
        wizard.run()
    else:
        # Subsequent runs: just show overlay
        threading.Thread(target=notify_success, daemon=True).start()

    hotkey.start(on_hotkey_press, on_hotkey_release)
    
    tray = TrayApp(on_quit_callback=on_quit, on_toggle_callback=on_toggle)
    # This blocks the main thread
    tray.run()
