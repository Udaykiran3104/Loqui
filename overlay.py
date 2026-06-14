import tkinter as tk
import threading

class Overlay:
    def __init__(self):
        self.root = None

    def _create_window(self):
        self.root = tk.Tk()
        self.root.overrideredirect(True)
        self.root.attributes("-topmost", True)
        self.root.config(bg="#222222")
        
        # Position at bottom center
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        
        # Window size
        w = 180
        h = 40
        x = (screen_width // 2) - (w // 2)
        y = screen_height - 80
        
        self.root.geometry(f"{w}x{h}+{x}+{y}")
        
        self.label = tk.Label(self.root, text="🎤 Recording...", font=("Arial", 14, "bold"), fg="#ff4444", bg="#222222")
        self.label.pack(expand=True, fill="both")
        
        self.root.withdraw() # Hide initially
        self.root.mainloop()

    def start(self):
        threading.Thread(target=self._create_window, daemon=True).start()

    def show(self, text="🎤 Recording...", fg="#ff4444"):
        if self.root:
            def _update():
                self.label.config(text=text, fg=fg)
                self.root.deiconify()
            self.root.after(0, _update)

    def hide(self):
        if self.root:
            self.root.after(0, self.root.withdraw)
            
    def show_message(self, text, duration_ms=3000):
        self.show(text=text, fg="#44ff44")
        if self.root:
            self.root.after(duration_ms, self.hide)
