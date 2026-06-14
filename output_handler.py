import pyperclip, subprocess, time, yaml

class OutputHandler:
    def __init__(self, config_path="config.yaml"):
        with open(config_path) as f:
            cfg = yaml.safe_load(f)["output"]
        self.copy = cfg.get("copy_to_clipboard", True)
        self.paste = cfg.get("auto_paste", True)
        self.notify = cfg.get("notify", True)

    def deliver(self, text: str):
        if not text:
            return

        print(f"\n📋 Result: {text}\n")

        if self.copy:
            pyperclip.copy(text)

        if self.paste:
            # Small delay so clipboard is ready
            time.sleep(0.1)
            # Linux: xdotool   |   Mac: osascript   |   Windows: pyautogui
            try:
                subprocess.run(['xdotool', 'key', 'ctrl+v'], check=True)
            except FileNotFoundError:
                # Fallback for Mac / Windows
                import pyautogui
                pyautogui.hotkey('ctrl', 'v')

        if self.notify:
            try:
                from plyer import notification
                notification.notify(
                    title="Loqui",
                    message=text[:80] + ("…" if len(text) > 80 else ""),
                    timeout=3
                )
            except Exception:
                pass
