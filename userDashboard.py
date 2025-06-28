import tkinter as tk
from tkinter import ttk, messagebox
import values
from verifyCreds import get_courses

def on_item_selected(event):
    selected_item = tree.selection()
    if selected_item:
        item_id = selected_item[0]
        parent_id = tree.parent(item_id)  # Get parent to check if this is a child node

        if parent_id:  # Only proceed if it's a child (i.e., has a parent)
            item_text = tree.item(item_id, "text")
            content_label.config(text=f"You selected: {item_text}")
            root.title(f"User Dashboard - {item_text}")
        else:
            # It's a folder/course name (not a child), do not change title
            item_text = tree.item(item_id, "text")
            content_label.config(text=f"Course: {item_text}")


def setup_treeview(parent, courses):
    global tree
    container = ttk.Frame(parent)
    container.grid(row=0, column=0, sticky="nsew")

    # Treeview
    tree = ttk.Treeview(container, columns=("url",), show="tree")
    tree.grid(row=0, column=0, sticky="nsew")

    # Scrollbars
    vsb = ttk.Scrollbar(container, orient="vertical", command=tree.yview)
    vsb.grid(row=0, column=1, sticky="ns")

    hsb = ttk.Scrollbar(container, orient="horizontal", command=tree.xview)
    hsb.grid(row=1, column=0, sticky="ew")  # <-- Uncommented this line

    tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)

    # Force wide column to enable scrolling
    tree.column("#0", minwidth=600, width=600, stretch=False)

    container.columnconfigure(0, weight=1)
    container.rowconfigure(0, weight=1)

    # Add nodes
    for course in courses:
        course_name = course.get("course_name", "Untitled Course")
        contents = course.get("course_content_urls", [])
        course_node = tree.insert("", "end", text=f"📁 {course_name}", open=True)
        for content in contents:
            title = content.get("title", "Untitled")
            url = content.get("url", "")
            tree.insert(course_node, "end", text=f"📄 {title}", values=(url,))

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

