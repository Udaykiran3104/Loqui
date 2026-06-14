import pystray
from PIL import Image, ImageDraw

class TrayApp:
    def __init__(self, on_quit_callback=None, on_toggle_callback=None):
        self.icon = None
        self.is_enabled = True
        self.on_quit_callback = on_quit_callback
        self.on_toggle_callback = on_toggle_callback

    def _create_icon_image(self, enabled):
        image = Image.new('RGBA', (64, 64), (0, 0, 0, 0))
        draw = ImageDraw.Draw(image)
        color = "#00ff00" if enabled else "#888888"
        
        # Draw a simple mic (circle and a line)
        draw.rounded_rectangle((24, 10, 40, 36), radius=8, fill=color)
        draw.arc((16, 20, 48, 48), start=0, end=180, fill=color, width=4)
        draw.line((32, 48, 32, 58), fill=color, width=4)
        draw.line((20, 58, 44, 58), fill=color, width=4)
        
        return image

    def toggle_state(self, icon, item):
        self.is_enabled = not self.is_enabled
        icon.icon = self._create_icon_image(self.is_enabled)
        if self.on_toggle_callback:
            self.on_toggle_callback(self.is_enabled)
        
    def quit_app(self, icon, item):
        icon.stop()
        if self.on_quit_callback:
            self.on_quit_callback()

    def run(self):
        menu = pystray.Menu(
            pystray.MenuItem('STT Enabled', self.toggle_state, checked=lambda item: self.is_enabled),
            pystray.MenuItem('Exit Application', self.quit_app)
        )
        self.icon = pystray.Icon("Loqui", self._create_icon_image(self.is_enabled), "Loqui", menu)
        self.icon.run()
