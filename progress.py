import tkinter as tk
from tkinter import ttk

def start_progress(callback_after_progress):
    progress_win = tk.Toplevel()
    progress_win.title("Login Progress")
    progress_win.resizable(False, False)
    progress_win.attributes("-topmost", True)

    width = 300
    height = 100
    screen_width = progress_win.winfo_screenwidth()
    screen_height = progress_win.winfo_screenheight()
    x = (screen_width // 2) - (width // 2)
    y = (screen_height // 2) - (height // 2)
    progress_win.geometry(f"{width}x{height}+{x}+{y}")

    label = tk.Label(progress_win, text="Logging in now . . . ", font=("Segoe UI", 12))
    label.pack(pady=10)

    pb = ttk.Progressbar(progress_win, mode="indeterminate", length=250)
    pb.pack(pady=5)
    pb.start(10)

    def finish():
        pb.stop()
        progress_win.destroy()
        callback_after_progress()

    progress_win.after(10000, finish)
