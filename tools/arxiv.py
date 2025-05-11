from langchain_community.tools.arxiv.tool import ArxivQueryRun

def create_arxiv_tool():
    """Create ArXiv query tool."""
    return ArxivQueryRun()