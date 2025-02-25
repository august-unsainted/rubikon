import hashlib
from datetime import datetime


def generate_daily_password():
    today = datetime.now().strftime('%Y-%m-%d')
    password_string = today + "RubyAdmin"
    hashed_password = hashlib.sha256(password_string.encode()).hexdigest()
    middle_index = len(hashed_password) // 2
    daily_password = hashed_password[middle_index - 2:middle_index + 3]
    return daily_password


if __name__ == "__main__":
    print(generate_daily_password())
