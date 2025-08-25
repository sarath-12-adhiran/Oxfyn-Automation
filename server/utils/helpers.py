import random
import string
import os
from datetime import date
import time


def generate_username(length=4):
    random_string = ''.join(random.choices(string.ascii_lowercase + string.digits, k=length))
    return f'Atester{random_string}'

def generate_mobile_number():
    first_digit = str(random.choice([6, 7, 8, 9]))
    remaining_digits = ''.join(random.choices(string.digits, k=9))
    return first_digit + remaining_digits

def generate_utr():
    integer = str(random.randint(1,10))
    character = ''.join(random.choices(string.ascii_letters, k=5))
    combined = list(integer + ''.join(character))
    random.shuffle(combined)
    return ''.join(combined)

def take_screenshots(driver, filename):
    if not os.path.exists('screenshots'):
        os.mkdir("screenshots")
    today_date = date.today()
    driver.save_screenshot(f"screenshots/{today_date}_{filename}.png")


def generate_campaign_code(length=3):
    random_string = ''.join(random.choices(string.digits, k=length))
    return f'AUTO-{random_string}'

def generate_account_number(length=12):
    return ''.join(random.choices(string.digits, k=length))

def BASE_DIR(filename):
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_dir, "static", filename)

def retry(times, delay=2):
    def decorator(func):
        def wrapper(*args, **kwargs):
            for i in range(times):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    print(f"Retry {i+1}/{times} failed: {e}")
                    time.sleep(delay)
            raise Exception("All retries failed.")
        return wrapper
    return decorator

def generate_lobby_name():
    random_string = ''.join(random.choices(string.digits, k=3))
    return f'Lobby-{random_string}'

