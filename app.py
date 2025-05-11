import chainlit as cl
from langchain_core.messages import HumanMessage

from utils.data import load_documents, split_documents
from models.embeddings import create_embeddings
from utils.vector_store import create_vector_store
from tools.search import create_tavily_tool
from tools.arxiv import create_arxiv_tool
from graphs.agent_graph import create_agent_graph

# Initialize components
docs = load_documents()
split_docs = split_documents(docs)
embeddings = create_embeddings()
vector_store = create_vector_store(embeddings, split_docs)
tavily_tool = create_tavily_tool()
arxiv_tool = create_arxiv_tool()
compiled_graph = create_agent_graph(vector_store, tavily_tool, arxiv_tool)

@cl.on_chat_start
async def start():
    cl.user_session.set("graph", compiled_graph)

@cl.on_message
async def handle(message: cl.Message):
    graph = cl.user_session.get("graph")
    state = {"messages": [HumanMessage(content=message.content)]}
    response = await graph.ainvoke(state)
    await cl.Message(content=response["messages"][-1].content).send()