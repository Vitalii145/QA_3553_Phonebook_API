import os

from dotenv import load_dotenv

load_dotenv(verbose=True)

API_BASE_URL = os.getenv("API_BASE_URL")
TEST_USER_EMAIL = os.getenv("TEST_USER_EMAIL")
TEST_USER_PASSWORD = os.getenv("TEST_USER_PASSWORD")