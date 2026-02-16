import os
import logging
from dotenv import load_dotenv
load_dotenv()

DATA_DIR = os.getenv("DATA_DIR", "./data")
os.makedirs(DATA_DIR, exist_ok=True)

def get_env(key, default=None):
    return os.getenv(key, default)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("website-rag")
