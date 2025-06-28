import tkinter as tk
from tkinter import ttk, messagebox
import vlc
import values
from verifyCreds import get_courses

# Global VLC player instance
player = None
media_instance = None
progress = None  # for slider


def on_item_selected(event):
    selected_item = tree.selection()
    if selected_item:
        item_id = selected_item[0]
        parent_id = tree.parent(item_id)

        item_text = tree.item(item_id, "text")
        content_label.config(text=f"You selected: {item_text}")

        if parent_id:  # It's a video, not a folder
            url = tree.item(item_id, "values")[0]
            root.title(f"User Dashboard - {item_text}")
            play_selected_video(url)
        else:
            root.title("User Dashboard")


def play_selected_video(url):
    global player, media_instance

    if player:
        player.stop()

    media_instance = vlc.Instance()
    player = media_instance.media_player_new()
    media = media_instance.media_new(url)
    player.set_media(media)

    player.set_hwnd(video_frame.winfo_id())

    player.play()


def setup_treeview(parent, courses):
    global tree
    container = parent

    # Configure style for the Treeview (to set text color)
    style = ttk.Style()
    style.configure("Custom.Treeview",
                    background="#2c2c2c",  # Dark background (optional)
                    foreground="white",   # White text color
                    fieldbackground="#2c2c2c")  # Background of non-tree columns

    vsb = ttk.Scrollbar(container, orient="vertical")
    hsb = ttk.Scrollbar(container, orient="horizontal")

    # Apply the custom style to Treeview
    tree = ttk.Treeview(
        container,
        columns=("url",),
        show="tree",
        yscrollcommand=vsb.set,
        xscrollcommand=hsb.set,
        style="Custom.Treeview"  # <-- Use the custom style
    )
    tree.grid(row=0, column=0, columnspan=2, sticky="nsew")

    vsb.config(command=tree.yview)
    vsb.grid(row=0, column=2, sticky="ns")

    hsb.config(command=tree.xview)
    hsb.grid(row=1, column=0, columnspan=2, sticky="ew")

    # Configure columns (ensure URL column is hidden but styled)
    tree.column("#0", minwidth=300, width=300, stretch=True)
    tree.column("url", width=0, stretch=False)  # Hide URL column (but keep data)

    container.rowconfigure(0, weight=1)
    container.columnconfigure(0, weight=1)

    # Populate tree
    for course in courses:
        course_name = course.get("course_name", "Untitled Course")
        contents = course.get("course_content_urls", [])
        course_node = tree.insert("", "end", text=f"📁 {course_name}", open=True)
        for content in contents:
            title = content.get("title", "Untitled").strip()
            if "http" in title:
                title = title.split("http")[0].strip()
            url = content.get("url", "")
            tree.insert(course_node, "end", text=f"📄 {title}", values=(url,))

    tree.bind("<<TreeviewSelect>>", on_item_selected)

def setup_video_controls(parent):
    global progress
    controls_frame = tk.Frame(parent)
    controls_frame.grid(row=2, column=0, sticky="ew", pady=10)

    progress = tk.DoubleVar()

    def pause_video():
        if player:
            player.pause()

    def resume_video():
        if player:
            player.play()

    def set_position(val):
        if player:
            pos = float(val) / 100
            player.set_position(pos)

    def update_slider():
        if player and player.is_playing():
            try:
                pos = player.get_position() * 100
                progress.set(pos)
            except:
                pass
        parent.after(500, update_slider)

    play_btn = tk.Button(controls_frame, text="▶ Play", command=resume_video)
    play_btn.pack(side=tk.LEFT, padx=10)

    pause_btn = tk.Button(controls_frame, text="⏸ Pause", command=pause_video)
    pause_btn.pack(side=tk.LEFT)

    trackbar = tk.Scale(
        controls_frame,
        variable=progress,
        from_=0,
        to=100,
        orient=tk.HORIZONTAL,
        length=400,
        command=set_position
    )
    trackbar.pack(side=tk.RIGHT, padx=20)

    parent.after(1000, update_slider)


def change_password():
    # Create a new top-level window
    password_window = tk.Toplevel()
    password_window.title("Change Password")
    password_window.geometry("400x300")
    password_window.resizable(False, False)

    # Current Password
    tk.Label(password_window, text="Current Password:").pack(pady=(20, 5))
    current_pass_entry = ttk.Entry(password_window, show="*")
    current_pass_entry.pack()

    # New Password
    tk.Label(password_window, text="New Password:").pack(pady=(10, 5))
    new_pass_entry = ttk.Entry(password_window, show="*")
    new_pass_entry.pack()

    # Confirm New Password
    tk.Label(password_window, text="Confirm New Password:").pack(pady=(10, 5))
    confirm_pass_entry = ttk.Entry(password_window, show="*")
    confirm_pass_entry.pack()

    # Show Password Checkbox
    show_pass_var = tk.BooleanVar()
    show_pass_check = ttk.Checkbutton(
        password_window,
        text="Show Passwords",
        variable=show_pass_var,
        command=lambda: toggle_password_visibility(
            show_pass_var.get(),
            current_pass_entry,
            new_pass_entry,
            confirm_pass_entry
        )
    )
    show_pass_check.pack(pady=10)

    # Submit Button
    def submit_password_change():
        current = current_pass_entry.get()
        new = new_pass_entry.get()
        confirm = confirm_pass_entry.get()

        if not current or not new or not confirm:
            messagebox.showerror("Error", "All fields are required!")
            return

        if new != confirm:
            messagebox.showerror("Error", "New passwords don't match!")
            return

        # Here you would add your actual password change logic
        messagebox.showinfo("Success", "Password changed successfully!")
        password_window.destroy()

    ttk.Button(
        password_window,
        text="Change Password",
        command=submit_password_change
    ).pack(pady=10)


def toggle_password_visibility(show, *entries):
    """Toggle password visibility for all provided entry widgets"""
    show_char = "" if show else "*"
    for entry in entries:
        entry.config(show=show_char)

def logout():
    should_logout = messagebox.askyesno("Logout", "Are you sure you want to logout?")
    if should_logout:
        if player:
            player.stop()
            player.release()
        if media_instance:
            media_instance.release()
        root.destroy()


def setup_menu(root):
    menubar = tk.Menu(root)
    options_menu = tk.Menu(menubar, tearoff=0)
    options_menu.add_command(label="Change Password", command=change_password)
    options_menu.add_separator()
    options_menu.add_command(label="Logout", command=logout)

    menubar.add_cascade(label="Options", menu=options_menu)
    root.config(menu=menubar)


def launch_dashboard():
    global content_label, root, video_frame, player, media_instance
    print("values user dashboard", values.course_ids)

    raw_ids = values.course_ids
    course_ids = []
    for item in raw_ids:
        course_ids.extend(item.get("ids", []))

    courses = get_courses(course_ids)

    root = tk.Tk()
    root.title("User Dashboard")
    root.geometry("1200x700")

    root.columnconfigure(0, weight=0)
    root.columnconfigure(1, weight=1)
    root.rowconfigure(0, weight=1)

    def on_closing():
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            # Clean up VLC resources
            if player:
                player.stop()
                player.release()
            if media_instance:
                media_instance.release()
            root.destroy()

    root.protocol("WM_DELETE_WINDOW", on_closing)

    setup_menu(root)

    sidebar = ttk.Frame(root, width=250)
    sidebar.grid(row=0, column=0, sticky="ns")
    sidebar.grid_propagate(False)
    sidebar.rowconfigure(0, weight=1)
    sidebar.columnconfigure(0, weight=1)

    main_content = tk.Frame(root)
    main_content.grid(row=0, column=1, sticky="nsew")
    main_content.columnconfigure(0, weight=1)
    main_content.rowconfigure(1, weight=1)
    main_content.rowconfigure(2, weight=0)

    content_label = ttk.Label(main_content, text="Select an item from the list", font=("Segoe UI", 14))
    content_label.grid(row=0, column=0, pady=10)

    video_frame = tk.Frame(main_content, bg="black")
    video_frame.grid(row=1, column=0, sticky="nsew", padx=10, pady=5)

    setup_video_controls(main_content)
    setup_treeview(sidebar, courses)

    root.mainloop()