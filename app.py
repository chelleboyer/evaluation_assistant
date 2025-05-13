import os
import chainlit as cl
from langchain_core.messages import HumanMessage
from utils.data import load_documents, split_documents
from utils.vector_store import create_vector_store
from models.embeddings import create_embeddings, create_huggingface_embeddings
from tools.search import create_tavily_tool
from tools.arxiv import create_arxiv_tool
from graphs.agent_graph import create_agent_graph
import dotenv
import logging
import traceback
from config import EMBEDDING_MODEL, HUGGINGFACE_MODEL

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Load environment variables
dotenv.load_dotenv()

from aimakerspace.text_utils import CharacterTextSplitter, TextFileLoader, PDFLoader
from aimakerspace.openai_utils.prompts import (
    UserRolePrompt,
    SystemRolePrompt,
    AssistantRolePrompt,
)
from aimakerspace.openai_utils.embedding import EmbeddingModel
from aimakerspace.vectordatabase import VectorDatabase
from aimakerspace.openai_utils.chatmodel import ChatOpenAI

# Initialize components
logging.info("Loading documents...")
text_splitter = CharacterTextSplitter()
docs = load_documents()
logging.info(f"Loaded {len(docs)} documents")

logging.info("Splitting documents...")
split_docs = split_documents(docs)
logging.info(f"Split into {len(split_docs)} chunks")

logging.info("Creating embeddings...")
embeddings = create_embeddings(split_docs)
logging.info(f"Created {len(embeddings)} embeddings")

logging.info("Creating vector store...")
vector_store = create_vector_store(embeddings, split_docs)
logging.info("Vector store created successfully")

logging.info("Creating tools...")
tavily_tool = create_tavily_tool()
arxiv_tool = create_arxiv_tool()
logging.info("Tools created successfully")

logging.info("Creating agent graph...")
compiled_graph = create_agent_graph(vector_store, tavily_tool, arxiv_tool)
logging.info("Agent graph compiled successfully")

# Suggested queries to try
DOCUMENT_QUERIES = [
    "What methods are used for evaluating large language models?",
    "Explain the key metrics for measuring AI performance",
    "What are the challenges in AI evaluation according to the documents?",
]

WEB_QUERIES = [
    "Search for the latest LLM benchmarks",
    "Search for recent advances in AI evaluation",
]

ACADEMIC_QUERIES = [
    "Find arxiv papers on AI alignment",
    "What academic research exists on prompt engineering?",
]

@cl.on_chat_start
async def start():
    cl.user_session.set("graph", compiled_graph)
    logging.info("New chat session started")
    
    # Welcome message with suggested queries
    welcome_message = """# 🔍 AI Evaluation Assistant

Welcome to the AI Evaluation Assistant! This tool helps you analyze documents about AI evaluation methods and techniques.

## Available Tools
- **Document Search**: Query information from loaded research papers about llm evaluations
- **Web Search**: Find real-time information about any topic
- **ArXiv**: Access academic papers and research
"""   
    welcome_message += "\n\n*Simply type your question and I'll help find the most relevant information!*"
    
    await cl.Message(content=welcome_message).send()

@cl.on_message
async def handle(message: cl.Message):
    try:
        # Log incoming message
        logging.info(f"Received message: {message.content}")
        
        # Check if we have a last_query set from an action click
        last_query = cl.user_session.get("last_query")
        if last_query:
            message.content = last_query
            cl.user_session.set("last_query", None)
            logging.info(f"Using stored query: {message.content}")
        
        graph = cl.user_session.get("graph")
        if not graph:
            logging.error("Graph not found in user session")
            await cl.Message(content="There was an error with your session. Please refresh the page.").send()
            return
            
        state = {"messages": [HumanMessage(content=message.content)]}
        
        # Add a thinking message
        thinking = cl.Message(content="Thinking...", author="Assistant")
        await thinking.send()
        logging.info("Sent thinking message")
        
        # Process the request
        logging.info("Invoking agent graph")
        try:
            response = await graph.ainvoke(state)
            logging.info(f"Got response: {str(response)[:100]}...")
        except Exception as e:
            logging.error(f"Error invoking graph: {str(e)}")
            logging.error(traceback.format_exc())
            response = {
                "messages": [HumanMessage(content=f"I encountered an error processing your request: {str(e)}")]
            }
        
        # Remove the thinking message
        await thinking.remove()
        
        # Send the actual response
        if response and "messages" in response and len(response["messages"]) > 0:
            await cl.Message(content=response["messages"][-1].content).send()
            logging.info("Sent response to user")
        else:
            await cl.Message(content="I'm sorry, I couldn't generate a response. Please try again.").send()
            logging.warning("Empty response from graph")
            
    except Exception as e:
        logging.error(f"Unhandled exception: {str(e)}")
        logging.error(traceback.format_exc())
        await cl.Message(content=f"An unexpected error occurred: {str(e)}").send()