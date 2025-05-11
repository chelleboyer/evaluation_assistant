from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolNode
from config import AGENT_MODEL
from utils.state import AgentState
from tools.rag import create_rag_tool
from langchain_core.messages import HumanMessage

def create_agent_graph(vector_store, tavily_tool, arxiv_tool):
    """Create an agent graph with RAG, Tavily, and ArXiv tools."""
    retriever = vector_store.as_retriever(search_kwargs={"k": 5})
    ai_rag_tool = create_rag_tool(retriever)
    
    tool_belt = [
        tavily_tool,
        arxiv_tool,
        ai_rag_tool
    ]
    
    model = ChatOpenAI(model=AGENT_MODEL, temperature=0)
    model = model.bind_tools(tool_belt)
    
    tool_node = ToolNode(tool_belt)
    uncompiled_graph = StateGraph(AgentState)
    
    def call_model(state):
        messages = state["messages"]
        response = model.invoke(messages)
        return {
            "messages": [response],
            "context": state.get("context", [])
        }
    
    uncompiled_graph.add_node("agent", call_model)
    uncompiled_graph.add_node("action", tool_node)
    
    uncompiled_graph.set_entry_point("agent")
    
    def should_continue(state):
        last_message = state["messages"][-1]
        
        if last_message.tool_calls:
            return "action"
        
        return END
    
    uncompiled_graph.add_conditional_edges(
        "agent",
        should_continue
    )
    
    uncompiled_graph.add_edge("action", "agent")
    
    return uncompiled_graph.compile()