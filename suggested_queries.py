import chainlit as cl

# Document queries with emojis
DOCUMENT_QUERIES = [
    "💡 What methods are used for evaluating large language models?",
    "💡 Explain the key metrics for measuring AI performance",
    "💡 What are the challenges in AI evaluation according to the documents?",
    "💡 How do researchers measure LLM accuracy?",
    "💡 What are the limitations of current AI evaluation approaches?"
]

# Web search queries with emojis
WEB_QUERIES = [
    "🌐 Search for the latest LLM benchmarks",
    "🌐 Search for recent advances in AI evaluation",
    "🌐 Search for AI evaluation frameworks",
    "🌐 Search for hallucination detection methods"
]

# Academic research queries with emojis
ACADEMIC_QUERIES = [
    "📚 Find arxiv papers on AI alignment",
    "📚 What academic research exists on prompt engineering?",
    "📚 Find papers about AI evaluation metrics",
    "📚 What do researchers say about AI safety?"
]

@cl.on_chat_start
async def setup_suggested_queries():
    """Setup suggested queries at the start of the chat."""
    # Send welcome message with categories and suggested queries
    welcome_msg = """## Suggested Queries:
    
### Document Questions
"""
    for query in DOCUMENT_QUERIES:
        welcome_msg += f"- **{query}**\n"
    
    welcome_msg += "\n### Web Search\n"
    for query in WEB_QUERIES:
        welcome_msg += f"- **{query}**\n"
    
    welcome_msg += "\n### Academic Research\n"
    for query in ACADEMIC_QUERIES:
        welcome_msg += f"- **{query}**\n"
    
    # Send the welcome message with all suggestions
    await cl.Message(content=welcome_msg).send()
    
    # Create clickable elements (buttons) for easier selection
    elements = []
    for query in (DOCUMENT_QUERIES + WEB_QUERIES + ACADEMIC_QUERIES):
        elements.append(
            cl.Button(
                name=query,
                value=query,
                label=query[:30] + "..." if len(query) > 30 else query
            )
        )
    
    msg = cl.Message(content="Click a query to get started:", elements=elements)
    await msg.send()

@cl.on_element_click
async def handle_element_click(element: cl.Button):
    """Handle clicks on the buttons."""
    query = element.value
    
    # Send the query as if the user had typed it
    user_msg = cl.Message(content=query, author="User")
    await user_msg.send()
    
    # Store the query in the session
    cl.user_session.set("last_query", query) 