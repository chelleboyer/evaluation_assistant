import arxiv
from langchain_core.tools import Tool

def search_arxiv(query: str) -> str:
    """Search ArXiv for papers and return the top 3 results."""
    try:
        client = arxiv.Client()
        search = arxiv.Search(
            query=query,
            max_results=3,
            sort_by=arxiv.SortCriterion.Relevance
        )
        
        results = list(client.results(search))
        
        if not results:
            return f"No papers found on ArXiv for query: {query}"
        
        output = f"## ArXiv search results for: {query}\n\n"
        
        for paper in results:
            output += f"### {paper.title}\n"
            output += f"**Authors:** {', '.join(author.name for author in paper.authors)}\n"
            output += f"**Published:** {paper.published.strftime('%Y-%m-%d')}\n"
            output += f"**Link:** {paper.entry_id}\n"
            summary = paper.summary.replace('\n', ' ')
            output += f"**Summary:** {summary[:300]}...\n\n"
            
        return output
    except Exception as e:
        return f"Error searching ArXiv: {str(e)}"

def create_arxiv_tool():
    """Create ArXiv query tool."""
    return Tool(
        name="arxiv",
        description="Search for academic papers on ArXiv",
        func=search_arxiv
    )
