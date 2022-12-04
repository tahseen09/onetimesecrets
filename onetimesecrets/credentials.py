import os
from dotenv import load_dotenv
from pathlib import Path

# ! Hack to load env file properly
BASE_DIR = Path(__file__).resolve().parent.parent
path = os.path.join(BASE_DIR, ".env")

load_dotenv(path)

API_BASE_URL = os.environ["API_BASE_URL"]

ENCRYPTION_KEY = bytes(os.environ["ENCRYPTION_KEY"], "utf-8")

DJANGO_SECRET_KEY = os.environ["DJANGO_SECRET_KEY"]