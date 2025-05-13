from aimakerspace.vectordatabase import VectorDatabase
import asyncio
import numpy as np
from langchain_core.documents import Document
from typing import List, Dict, Any, Callable

class SimpleRetriever:
    """A simpler retriever class that doesn't rely on Pydantic."""
    
    def __init__(self, vector_db, text_map, k=5):
        """Initialize the retriever.
        
        Args:
            vector_db: The vector database
            text_map: Mapping of IDs to full text content
            k: Number of results to return
        """
        self.vector_db = vector_db
        self.text_map = text_map
        self.k = k
    
    def invoke(self, query: str) -> List[Document]:
        """Get documents relevant to the query."""
        results = self.vector_db.search_by_text(query, k=self.k, return_as_text=False)
        
        # Return actual document content instead of just IDs
        documents = []
        for doc_id, score in results:
            if doc_id in self.text_map:
                documents.append(Document(
                    page_content=self.text_map[doc_id],
                    metadata={"score": score, "id": doc_id}
                ))
            else:
                # Fallback for IDs without content
                documents.append(Document(
                    page_content=f"Document {doc_id} content not available",
                    metadata={"score": score, "id": doc_id}
                ))
        
        return documents
    
    # Make the class callable like a function
    def __call__(self, query):
        return self.invoke(query)

def create_vector_store(embeddings, texts=None):
    """Create vector store from embeddings and texts.
    
    Args:
        embeddings: List of embeddings
        texts: List of text documents corresponding to embeddings
    """
    vector_db = VectorDatabase()
    
    # Create a mapping of document IDs to actual content
    text_map = {}
    
    # Add the embeddings and content to the vector database
    if texts and len(texts) == len(embeddings):
        for i, (text, embedding) in enumerate(zip(texts, embeddings)):
            doc_id = f"text_{i}"
            vector_db.insert(doc_id, embedding)
            text_map[doc_id] = text
    else:
        for i, embedding in enumerate(embeddings):
            doc_id = f"text_{i}"
            vector_db.insert(doc_id, embedding)
            text_map[doc_id] = f"Content for document {doc_id} not available"
    
    # Add a simple retriever as the as_retriever method
    vector_db.as_retriever = lambda search_kwargs=None: SimpleRetriever(
        vector_db=vector_db,
        text_map=text_map,
        k=search_kwargs.get("k", 5) if search_kwargs else 5
    )
    
    return vector_db 