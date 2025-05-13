from typing_extensions import TypedDict, List
from langchain_core.messages import BaseMessage
from langchain_core.documents import Document

class AgentState(TypedDict):
    """Agent state for the graph."""
    messages: List[BaseMessage]
    context: List[str]

class State(TypedDict):
    """State for the RAG graph."""
    question: str
    context: List[Document]
    response: str 