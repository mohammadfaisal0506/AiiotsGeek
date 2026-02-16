from langchain_text_splitters import RecursiveCharacterTextSplitter
from .utils import CHUNK_SIZE, CHUNK_OVERLAP

splitter = RecursiveCharacterTextSplitter(chunk_size=CHUNK_SIZE, chunk_overlap=CHUNK_OVERLAP)

def chunk_text(text: str):
    return splitter.split_text(text)
