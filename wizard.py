import tkinter as tk
import os

class SetupWizard:
    def __init__(self, on_close_callback=None):
        self.root = None
        self.on_close_callback = on_close_callback

    def _create_window(self):
        self.root = tk.Tk()
        self.root.overrideredirect(True) # Borderless window
        self.root.attributes("-topmost", True)
        self.root.config(bg="#1e1e1e") # Sleek dark theme
        
        # Window size
        w = 480
        h = 420
        
        # Position at center
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width // 2) - (w // 2)
        y = (screen_height // 2) - (h // 2)
        
        self.root.geometry(f"{w}x{h}+{x}+{y}")
        
        # Add a colored top border accent
        top_border = tk.Frame(self.root, bg="#4a90e2", height=4)
        top_border.pack(fill="x")
        
        # Content frame
        content = tk.Frame(self.root, bg="#1e1e1e", padx=30, pady=20)
        content.pack(expand=True, fill="both")
        
        # Header "Loqui"
        title = tk.Label(content, text="Loqui", font=("Segoe UI", 28, "bold"), fg="#ffffff", bg="#1e1e1e")
        title.pack(pady=(10, 0))
        
        # Subtitle
        subtitle = tk.Label(content, text="Setup Successful! 🎉", font=("Segoe UI", 12), fg="#44ff44", bg="#1e1e1e")
        subtitle.pack(pady=(0, 20))
        
        # Instructions
        instructions_text = (
            "How to use:\n\n"
            "1. Click inside any text field.\n"
            "2. Hold your Hotkey (Default: Ctrl + Shift).\n"
            "3. Speak your sentence, then release the keys.\n"
            "4. Loqui will transcribe and type it for you.\n\n"
            "Right-click the microphone icon in your system tray to manage."
        )
        instructions = tk.Label(content, text=instructions_text, font=("Segoe UI", 10), fg="#cccccc", bg="#1e1e1e", justify="left")
        instructions.pack(pady=(0, 20))
        
        # Get Started Button
        def on_enter(e):
            btn.config(bg="#357abd")
        def on_leave(e):
            btn.config(bg="#4a90e2")
            
        btn = tk.Button(
            content, 
            text="Get Started", 
            font=("Segoe UI", 11, "bold"), 
            bg="#4a90e2", 
            fg="#ffffff", 
            activebackground="#357abd", 
            activeforeground="#ffffff",
            relief="flat",
            padx=20,
            pady=8,
            cursor="hand2",
            command=self._close
        )
        btn.pack(pady=(10, 10))
        btn.bind("<Enter>", on_enter)
        btn.bind("<Leave>", on_leave)
        
        self.root.mainloop()

    def _close(self):
        # Create .loqui_setup flag file
        try:
            exe_dir = "."
            import sys
            if getattr(sys, 'frozen', False):
                exe_dir = os.path.dirname(sys.executable)
            flag_path = os.path.join(exe_dir, ".loqui_setup")
            with open(flag_path, "w") as f:
                f.write("Setup complete")
        except Exception as e:
            print(f"Failed to write setup flag: {e}")
            
        if self.on_close_callback:
            self.on_close_callback()
        self.root.destroy()

    def run(self):
        self._create_window()
