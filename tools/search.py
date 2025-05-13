import os
import requests
from langchain_core.tools import Tool
import logging

def search_web(query: str) -> str:
    """Search the web using Tavily API."""
    try:
        # Get API key from environment variable
        api_key = os.environ.get("TAVILY_API_KEY")
        
        if not api_key:
            # Check if we have it in the config
            try:
                from config import TAVILY_API_KEY
                api_key = TAVILY_API_KEY
            except (ImportError, AttributeError):
                pass
        
        if not api_key:
            return f"TAVILY_API_KEY not set. Please add it to your environment variables or config.py file."
        
        # Tavily Search API endpoint
        url = "https://api.tavily.com/search"
        
        # Parameters for the search
        params = {
            "api_key": api_key,
            "query": query,
            "search_depth": "basic",
            "include_domains": [],
            "exclude_domains": [],
            "max_results": 5
        }
        
        # Send the request
        response = requests.post(url, json=params)
        
        # Check if request was successful
        if response.status_code == 200:
            result = response.json()
            
            if "results" not in result or not result["results"]:
                return f"No results found for: {query}"
            
            # Format the results
            output = f"## Web search results for: {query}\n\n"
            
            for idx, item in enumerate(result["results"], 1):
                output += f"### {idx}. {item.get('title', 'No title')}\n"
                output += f"**URL:** {item.get('url', 'No URL')}\n"
                output += f"**Content:** {item.get('content', 'No content')[:300]}...\n\n"
            
            return output
        else:
            logging.error(f"Tavily API error: {response.status_code} - {response.text}")
            return f"Error searching Tavily: {response.status_code} - {response.text}"
    
    except Exception as e:
        logging.error(f"Error in search_web: {str(e)}")
        return f"Error searching the web: {str(e)}"

def create_tavily_tool():
    """Create Tavily search tool."""
    return Tool(
        name="web_search",
        description="Search the web using Tavily search engine",
        func=search_web
    )