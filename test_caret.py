import ctypes
from ctypes.wintypes import DWORD, HWND, RECT
import time

class GUITHREADINFO(ctypes.Structure):
    _fields_ = [
        ("cbSize", DWORD),
        ("flags", DWORD),
        ("hwndActive", HWND),
        ("hwndFocus", HWND),
        ("hwndCapture", HWND),
        ("hwndMenuOwner", HWND),
        ("hwndMoveSize", HWND),
        ("hwndCaret", HWND),
        ("rcCaret", RECT)
    ]

def has_text_cursor():
    gui_info = GUITHREADINFO()
    gui_info.cbSize = ctypes.sizeof(GUITHREADINFO)
    hwnd_active = ctypes.windll.user32.GetForegroundWindow()
    thread_id = ctypes.windll.user32.GetWindowThreadProcessId(hwnd_active, 0)
    ctypes.windll.user32.GetGUIThreadInfo(thread_id, ctypes.byref(gui_info))
    return bool(gui_info.hwndCaret)

for i in range(10):
    print("Has caret:", has_text_cursor())
    time.sleep(1)
