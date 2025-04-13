import os

from dotenv import load_dotenv

load_dotenv()
LINKEDIN_EMAIL = os.getenv('LINKEDIN_USERNAME')
LINKEDIN_PASSWORD = os.getenv('LINKEDIN_PASSWORD')
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_ACCESS_TOKEN')
TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')