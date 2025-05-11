from langchain_core.tools import tool
from langchain_core.messages import HumanMessage
from graphs.rag_graph import create_rag_graph

def create_rag_tool(retriever):
    """Create a RAG tool that uses a retriever to answer AI-related questions."""
    rag_graph = create_rag_graph(retriever)
    
    @tool
    def ai_rag_tool(question: str) -> str:
        """Useful for when you need to answer questions about artificial intelligence. 
        Input should be a fully formed question."""
        response = rag_graph.invoke({"question": question})
        return {
            "messages": [HumanMessage(content=response["response"])],
            "context": response["context"]
        }
    
    return ai_rag_tool