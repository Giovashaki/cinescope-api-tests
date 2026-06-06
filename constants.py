import os
from dotenv import load_dotenv

load_dotenv()

AUTH_URL = "https://auth.dev-cinescope.coconutqa.ru"
MOVIES_URL = "https://api.dev-cinescope.coconutqa.ru"

HEADERS = {
    "Content-Type": "application/json",
    "Accept": "application/json"
}

LOGIN_ENDPOINT = "/login"
REGISTER_ENDPOINT = "/register"
MOVIES_ENDPOINT = "/movies"

ADMIN_EMAIL = os.getenv("ADMIN_EMAIL")
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD")