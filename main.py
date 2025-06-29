import tkinter as tk
from tkinter import ttk, messagebox
from verifyCreds import check_credentials
from userDashboard import launch_dashboard
from back import starter_thread
from progress import start_progress

def login_form(role, login_handler):
    login_window = tk.Toplevel(root)
    login_window.title(f"{role} Login")
    login_window.geometry("350x250")
    login_window.resizable(False, False)

    login_window.update_idletasks()
    w = login_window.winfo_width()
    h = login_window.winfo_height()
    x = (login_window.winfo_screenwidth() // 2) - (w // 2)
    y = (login_window.winfo_screenheight() // 2) - (h // 2)
    login_window.geometry(f"+{x}+{y}")

    login_window.columnconfigure(0, weight=1)
    login_window.rowconfigure(0, weight=1)

    frame = ttk.Frame(login_window, padding=20)
    frame.grid(row=0, column=0)
    frame.columnconfigure(0, weight=1)

    ttk.Label(frame, text="Email ID :", font=('Segoe UI', 10)).grid(row=0, column=0, sticky="W", pady=(0, 5))
    username_entry = ttk.Entry(frame, width=30)
    username_entry.grid(row=1, column=0, pady=(0, 10))

    ttk.Label(frame, text="Password :", font=('Segoe UI', 10)).grid(row=2, column=0, sticky="W", pady=(0, 5))
    password_entry = ttk.Entry(frame, show="*", width=30)
    password_entry.grid(row=3, column=0, pady=(0, 5))

    def toggle_password():
        if show_password.get():
            password_entry.config(show="")
        else:
            password_entry.config(show="*")

    show_password = tk.BooleanVar()
    show_password.set(False)
    ttk.Checkbutton(frame, text="Show Password", variable=show_password, command=toggle_password).grid(row=4, column=0, sticky="W", pady=(0, 10))

    def submit_login():
        username = username_entry.get()
        password = password_entry.get()
        login_handler(username, password, login_window)

    ttk.Button(frame, text="Login", command=submit_login).grid(row=5, column=0, pady=10)


def user_login_handler(username, password, window):
    if check_credentials(username, password):
        def after_progress():
            messagebox.showinfo("Login Success", f"Welcome User: {username}!")
            window.destroy()
            for i in range(file_menu.index("end") + 1):
                file_menu.entryconfig(i, state="disabled")
            root.iconify()
            launch_dashboard()

        start_progress(after_progress)
    else:
        messagebox.showerror("Login Failed", "Invalid User credentials.")



def admin_login_handler(username, password, window):
    if username == "admin" and password == "admin123":
        messagebox.showinfo("Admin Panel", f"Welcome Admin: {username}!")
        window.destroy()

    else:
        messagebox.showerror("Access Denied", "Incorrect Admin credentials.")

def user_login():
    login_form("User", user_login_handler)

def admin_login():
    login_form("Admin", admin_login_handler)

def exit_app():
    root.quit()

# Main Window
root = tk.Tk()
root.title("ActiveTek Training")

window_width = 400
window_height = 300
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
x = (screen_width // 2) - (window_width // 2)
y = (screen_height // 2) - (window_height // 2)
root.geometry(f"{window_width}x{window_height}+{x}+{y}")

# Menu
menu_bar = tk.Menu(root)
file_menu = tk.Menu(menu_bar, tearoff=0)
file_menu.add_command(label="User Login", command=user_login)
file_menu.add_command(label="Admin Login", command=admin_login)
file_menu.add_command(label="Exit", command=exit_app)
menu_bar.add_cascade(label="Login", menu=file_menu)
root.config(menu=menu_bar)
starter_thread();
root.mainloop()
