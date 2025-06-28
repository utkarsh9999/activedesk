import tkinter as tk
from tkinter import ttk, messagebox
import values
from verifyCreds import get_courses
def on_item_selected(event):
    selected_item = tree.selection()
    if selected_item:
        item_text = tree.item(selected_item[0], "text")
        content_label.config(text=f"You selected: {item_text}")

def setup_treeview(parent,courses):
    global tree
    tree = ttk.Treeview(parent)
    print("treeview : ",courses)
    tree.grid(row=0, column=0, sticky="nsew")  # Use grid instead of pack
    tree.column("#0", width=150, stretch=False)

    module1 = tree.insert("", "end", text="📁 Module 1", open=True)
    tree.insert(module1, "end", text="📄 Video 1")
    tree.insert(module1, "end", text="📄 Video 2")

    module2 = tree.insert("", "end", text="📁 Module 2", open=False)
    tree.insert(module2, "end", text="📄 Topic A")
    tree.insert(module2, "end", text="📄 Topic B")

    tree.bind("<<TreeviewSelect>>", on_item_selected)



def change_password():
    messagebox.showinfo("Change Password", "This would open the Change Password dialog.")

def logout():
    should_logout = messagebox.askyesno("Logout", "Are you sure you want to logout?")
    if should_logout:
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
    global content_label, root
    print("values user dashboard", values.course_ids)

    # ✅ Extract course IDs from [{'ids': [101, 102]}]
    raw_ids = values.course_ids
    course_ids = []
    for item in raw_ids:
        course_ids.extend(item.get("ids", []))

    courses = get_courses(course_ids)

    root = tk.Tk()
    root.title("User Dashboard")
    root.geometry("900x600")

    root.columnconfigure(0, weight=0)
    root.columnconfigure(1, weight=1)
    root.rowconfigure(0, weight=1)

    # Menu bar
    setup_menu(root)

    # Sidebar
    sidebar = ttk.Frame(root, width=160)
    sidebar.grid(row=0, column=0, sticky="ns")
    sidebar.grid_propagate(False)
    sidebar.rowconfigure(0, weight=1)

    # Main content
    content = ttk.Frame(root)
    content.grid(row=0, column=1, sticky="nsew", padx=(5, 10), pady=10)
    content.columnconfigure(0, weight=1)
    content.rowconfigure(0, weight=1)

    content_label = ttk.Label(content, text="Select an item from the list", font=("Segoe UI", 14))
    content_label.grid(row=0, column=0, sticky="n", pady=20)

    # ✅ Pass filtered courses
    setup_treeview(sidebar, courses)

    root.mainloop()

