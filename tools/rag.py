from langchain_core.tools import tool
from langchain_core.messages import HumanMessage
from graphs.rag_graph import create_rag_graph
import logging

def create_rag_tool(retriever):
    """Create a RAG tool that uses a retriever to answer AI-related questions."""
    logging.info("Creating RAG graph for the tool")
    rag_graph = create_rag_graph(retriever)
    logging.info("RAG graph created successfully")
    
    @tool
    def ai_rag_tool(question: str) -> str:
        """Useful for when you need to answer questions about artificial intelligence. 
        Input should be a fully formed question."""
        logging.info(f"RAG tool processing question: {question}")
        try:
            state = {"question": question}
            logging.info(f"Invoking RAG graph with state: {state}")
            response = rag_graph.invoke(state)
            logging.info(f"RAG graph response: {str(response)[:100]}...")
            
            # Simplified return structure
            if "response" in response:
                return {
                    "response": response["response"]
                }
            else:
                logging.warning(f"Unexpected response structure: {response.keys()}")
                return {
                    "response": "I couldn't find relevant information about that topic in the documents."
                }
                
        except Exception as e:
            logging.error(f"Error in RAG tool: {str(e)}")
            return {
                "response": f"Error processing your question: {str(e)}"
            }
    
    return ai_rag_tool