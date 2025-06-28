from supabase import create_client,Client
import json

SUPABASE_URL = "https://gyixodkqsgazorbbifqa.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Imd5aXhvZGtxc2dhem9yYmJpZnFhIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTA1ODY5MjAsImV4cCI6MjA2NjE2MjkyMH0.CDQS91rJrsszqg2OGMfAvLRahmn5Vgb5lb4VSt5yYMw"
BUCKET_NAME = "accounts"
JSON_FILE_PATH = "account_ids.json"

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
def print_all_data():
    response = supabase.storage.from_(BUCKET_NAME).download(JSON_FILE_PATH)

    if response:
        json_data = json.loads(response.decode('utf-8'))
        print(json_data)
    else:
        print("Failed to fetch JSON file.")


def check_credentials(username, password):
    response = supabase.storage.from_(BUCKET_NAME).download(JSON_FILE_PATH)
    if not response:
        return False

    try:
        accounts = json.loads(response.decode("utf-8"))  # Expecting a list, not a dict
        for account in accounts:
            if account.get("email") == username and account.get("password") == password:
                course_ids=account.get("courses")
                print(course_ids)
                return True
        return False
    except Exception as e:
        print(f"Error parsing credentials: {e}")
        return False



