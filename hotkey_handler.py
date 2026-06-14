from pynput import keyboard
import yaml

class HotkeyHandler:
    def __init__(self, config_path="config.yaml"):
        with open(config_path) as f:
            cfg = yaml.safe_load(f)["hotkey"]

        # Parse key names into pynput Key objects
        self.combo = set()
        for k in cfg["keys"]:
            try:
                self.combo.add(getattr(keyboard.Key, k))
            except AttributeError:
                self.combo.add(keyboard.KeyCode.from_char(k))

        self._held = set()
        self.on_press_cb = None
        self.on_release_cb = None

    def _is_combo_held(self):
        return self.combo.issubset(self._held)

    def _normalize_key(self, key):
        if key in (keyboard.Key.ctrl_l, keyboard.Key.ctrl_r):
            return keyboard.Key.ctrl
        if key in (keyboard.Key.shift_l, keyboard.Key.shift_r):
            return keyboard.Key.shift
        if key in (keyboard.Key.alt_l, keyboard.Key.alt_r, getattr(keyboard.Key, 'alt_gr', None)):
            return keyboard.Key.alt
        if key in (keyboard.Key.cmd_l, keyboard.Key.cmd_r):
            return keyboard.Key.cmd
        return key

    def _on_press(self, key):
        key = self._normalize_key(key)
        self._held.add(key)
        if self._is_combo_held() and self.on_press_cb:
            self.on_press_cb()

    def _on_release(self, key):
        key = self._normalize_key(key)
        was_active = self._is_combo_held()
        self._held.discard(key)
        if was_active and not self._is_combo_held():
            if self.on_release_cb:
                self.on_release_cb()

    def start(self, on_press, on_release):
        self.on_press_cb = on_press
        self.on_release_cb = on_release
        self._listener = keyboard.Listener(
            on_press=self._on_press,
            on_release=self._on_release
        )
        self._listener.start()
        print(f"🎹 Listening for hotkey: {self.combo}")

    def stop(self):
        self._listener.stop()
