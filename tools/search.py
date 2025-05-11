from langchain_community.tools.tavily_search import TavilySearchResults

def create_tavily_tool():
    """Create Tavily search tool."""
    return TavilySearchResults(max_results=5)