import os, logging
from dotenv import load_dotenv
load_dotenv()

DATA_DIR = os.getenv("DATA_DIR", "./app/data")
os.makedirs(DATA_DIR, exist_ok=True)

FAISS_INDEX_FILE = os.getenv("FAISS_INDEX_FILE", os.path.join(DATA_DIR, "faiss.index"))
METADATA_STORE_FILE = os.getenv("METADATA_STORE_FILE", os.path.join(DATA_DIR, "metadata.pkl"))

CHUNK_SIZE = int(os.getenv("CHUNK_SIZE", "1000"))
CHUNK_OVERLAP = int(os.getenv("CHUNK_OVERLAP", "200"))

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)

logger = logging.getLogger("rag-app")