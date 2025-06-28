from supabase import create_client,Client
import json
import values
SUPABASE_URL = "https://gyixodkqsgazorbbifqa.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Imd5aXhvZGtxc2dhem9yYmJpZnFhIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTA1ODY5MjAsImV4cCI6MjA2NjE2MjkyMH0.CDQS91rJrsszqg2OGMfAvLRahmn5Vgb5lb4VSt5yYMw"
BUCKET_NAME = "accounts"
JSON_FILE_PATH = "account_ids.json"
COURSES_FILE_PATH="course_list.json"
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
                values.course_ids=account.get("courses")
                values.logged_in_user_email=account.get("email")
                values.logged_in_user_password=account.get("password")
                return True
        return False
    except Exception as e:
        print(f"Error parsing credentials: {e}")
        return False


def get_courses(raw_course_ids):
    print("get course course ids:", raw_course_ids)

    # Normalize course_ids to a flat list
    course_ids = []
    if isinstance(raw_course_ids, list):
        for entry in raw_course_ids:
            if isinstance(entry, dict) and "ids" in entry:
                course_ids.extend(entry["ids"])
            elif isinstance(entry, int):
                course_ids.append(entry)

    # Download all courses
    courses_response = supabase.storage.from_(BUCKET_NAME).download(COURSES_FILE_PATH)
    courses_data = json.loads(courses_response.decode('utf-8'))
    print("Raw course data:", courses_data)

    # Access actual course list inside the top-level dict
    course_list = courses_data.get("courses", [])

    # Filter by matching course_id
    filtered_courses = [
        course for course in course_list
        if isinstance(course, dict) and course.get("course_id") in course_ids
    ]
    return filtered_courses


def verify_change_password(old_pwd, new_pwd):
    if values.logged_in_user_password != old_pwd:
        print("Current password doesn't match")
        return False

    try:
        # 1. Download current accounts data
        response = supabase.storage.from_(BUCKET_NAME).download(JSON_FILE_PATH)
        if not response:
            print("Failed to fetch accounts data")
            return False

        accounts = json.loads(response.decode('utf-8'))

        # 2. Find and update the matching account
        updated = False
        for account in accounts:
            if account.get("email") == values.logged_in_user_email:
                account["password"] = new_pwd
                updated = True
                break

        if not updated:
            print("Account not found")
            return False

        # 3. Upload the updated JSON back to Supabase
        updated_json = json.dumps(accounts).encode('utf-8')

        # First try to remove existing file (if needed)
        try:
            supabase.storage.from_(BUCKET_NAME).remove([JSON_FILE_PATH])
        except Exception as remove_error:
            print(f"Warning: Could not remove old file (may not exist): {remove_error}")

        # Then upload new version
        upload_response = supabase.storage.from_(BUCKET_NAME).upload(
            JSON_FILE_PATH,
            updated_json
        )

        if upload_response:
            # Update local values if successful
            values.logged_in_user_password = new_pwd
            print("Password updated successfully")
            return True
        else:
            print("Failed to upload updated data")
            return False

    except Exception as e:
        print(f"Error updating password: {e}")
        return False