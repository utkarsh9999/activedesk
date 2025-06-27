import tkinter as tk
import vlc

def start_video_plater():
    root = tk.Tk()
    root.title("Video Player with Sound & Controls")
    root.geometry("800x600")

    # --- Separate Frame for Video ---
    video_frame = tk.Frame(root)
    video_frame.pack(expand=True, fill=tk.BOTH)

    # --- Controls Frame ---
    controls_frame = tk.Frame(root)
    controls_frame.pack(fill=tk.X, pady=10)

    # VLC setup
    instance = vlc.Instance()
    player = instance.media_player_new()
    media = instance.media_new("https://activetektraining.com/wp-content/vid/Call-Notice/1.%29%20Call%20Notice%20Overview.mp4")
    player.set_media(media)

    root.update()
    player.set_hwnd(video_frame.winfo_id())  # For Windows

    # --- UI controls and callback functions ---

    progress = tk.DoubleVar()

    def play_video():
        player.play()

    def pause_video():
        player.pause()

    def set_position(val):
        pos = float(val) / 100
        player.set_position(pos)

    def update_slider():
        if player.is_playing():
            pos = player.get_position() * 100
            progress.set(pos)
        root.after(500, update_slider)

    # Buttons
    play_btn = tk.Button(controls_frame, text="▶ Play", command=play_video)
    play_btn.pack(side=tk.LEFT, padx=10)

    pause_btn = tk.Button(controls_frame, text="⏸ Pause", command=pause_video)
    pause_btn.pack(side=tk.LEFT)

    # Trackbar
    trackbar = tk.Scale(controls_frame, variable=progress, from_=0, to=100,
                        orient=tk.HORIZONTAL, length=400, command=set_position)
    trackbar.pack(side=tk.RIGHT, padx=20)

    # Start updating slider
    root.after(1000, update_slider)

    root.mainloop()

start_video_plater()
