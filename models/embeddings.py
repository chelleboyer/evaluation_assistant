from langchain_openai import OpenAIEmbeddings
from langchain_community.embeddings import HuggingFaceEmbeddings
from config import EMBEDDING_MODEL

def create_embeddings(texts):
    """Create OpenAI embeddings model."""
    all_texts = []
    all_texts.extend(texts)
    if not all_texts:
        return {"success": False, "error": "No text chunks were extracted from any files", "files": []}

    embeddings_model = OpenAIEmbeddings(model=EMBEDDING_MODEL)
    # Generate embeddings for all texts
    embeddings = embeddings_model.embed_documents(all_texts)
    return embeddings

def create_huggingface_embeddings(texts, model_name, model_kwargs=None, encode_kwargs=None):
    """Create Hugging Face embeddings model using a fine-tuned model."""
    all_texts = []
    all_texts.extend(texts)
    if not all_texts:
        return {"success": False, "error": "No text chunks were extracted from any files", "files": []}
    
    embeddings_model = HuggingFaceEmbeddings(model_name=model_name, model_kwargs=model_kwargs, encode_kwargs=encode_kwargs)
    return embeddings_model.embed_documents(all_texts)