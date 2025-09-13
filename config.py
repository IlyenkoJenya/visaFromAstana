import os
from dotenv import load_dotenv

load_dotenv()  # Загружаем .env

LOGIN = os.getenv("LOGIN")
PASSWORD = os.getenv("PASSWORD")
CHECK_PAGE = os.getenv("CHECK_PAGE")

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID_SERVICE = os.getenv("CHAT_ID_SERVICE")
CHAT_ID = os.getenv("CHAT_ID")