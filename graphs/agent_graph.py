from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, END, START
from config import AGENT_MODEL
from utils.state import AgentState
from tools.rag import create_rag_tool
from langchain_core.messages import HumanMessage, AIMessage
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def create_agent_graph(vector_store, tavily_tool, arxiv_tool):
    """Create a simplified agent graph with direct tool invocation."""
    logging.info("Creating agent graph with tools")
    
    try:
        retriever = vector_store.as_retriever(search_kwargs={"k": 5})
        logging.info("Successfully created retriever")
    except Exception as e:
        logging.error(f"Error creating retriever: {e}")
        raise
        
    try:
        ai_rag_tool = create_rag_tool(retriever)
        logging.info("Successfully created RAG tool")
    except Exception as e:
        logging.error(f"Error creating RAG tool: {e}")
        raise
    
    # Create the LLM
    logging.info(f"Creating LLM with model: {AGENT_MODEL}")
    llm = ChatOpenAI(model=AGENT_MODEL, temperature=0)
    
    # Create simplified graph
    graph = StateGraph(AgentState)
    
    # Keywords that trigger RAG for our example document
    evaluation_keywords = [
        "ai", "artificial intelligence", "llm", "language model", "evaluation", 
        "metric", "metrics", "benchmark", "benchmarks", "mmlu", "humaneval", 
        "truthfulqa", "big-bench", "accuracy", "factual", "reasoning", "turing",
        "red team", "red teaming", "challenge", "challenges", "linguistic"
    ]
    
    def agent_node(state):
        """Process user input and decide which tool to use."""
        user_input = state["messages"][-1].content.lower()
        logging.info(f"Processing user input: {user_input}")
        
        # Simple rule-based tool selection
        response = ""
        try:
            if "search" in user_input:
                logging.info("Using search tool")
                try:
                    response = tavily_tool(user_input)
                except Exception as e:
                    logging.error(f"Search tool error: {e}")
                    response = f"I encountered an error with the search tool: {str(e)}"
            elif "arxiv" in user_input or "paper" in user_input or "academic" in user_input:
                logging.info("Using arxiv tool")
                try:
                    response = arxiv_tool(user_input)
                except Exception as e:
                    logging.error(f"ArXiv tool error: {e}")
                    response = f"I encountered an error with the ArXiv tool: {str(e)}"
            elif any(kw in user_input for kw in evaluation_keywords):
                logging.info("Using RAG tool for AI evaluation query")
                try:
                    result = ai_rag_tool.invoke(user_input)
                    if result and "response" in result:
                        response = result["response"]
                    else:
                        response = "I couldn't find specific information about that in our documents."
                except Exception as e:
                    logging.error(f"Error using RAG tool: {e}")
                    response = "I encountered an error when searching our documents. Let me provide a general response instead."
                    # Fall back to direct LLM if RAG fails
                    prompt = f"""
                    The user asked: "{user_input}"
                    
                    Provide a helpful response about LLM evaluation based on standard knowledge.
                    """
                    response = llm.invoke(prompt).content
            else:
                # Simple prompt for direct chat
                logging.info("Using direct LLM response")
                prompt = f"Answer this question concisely: {user_input}"
                response = llm.invoke(prompt).content
        except Exception as e:
            logging.error(f"Error processing request: {e}")
            response = f"I encountered an error processing your request: {str(e)}"
        
        logging.info(f"Generated response: {response[:100]}...")
        return {
            "messages": state["messages"] + [AIMessage(content=response)],
            "context": state.get("context", [])
        }
    
    # Add the agent node
    graph.add_node("agent", agent_node)
    
    # Set up the graph flow
    graph.add_edge(START, "agent")
    graph.add_edge("agent", END)
    
    return graph.compile()