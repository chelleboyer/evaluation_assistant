from langchain_openai import OpenAIEmbeddings
from config import EMBEDDING_MODEL

def create_embeddings():
    """Create OpenAI embeddings model."""
    return OpenAIEmbeddings(model=EMBEDDING_MODEL)