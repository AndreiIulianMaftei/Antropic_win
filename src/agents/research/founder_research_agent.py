# src/agents/research/founder_research_agent.py
from tavily import TavilyClient

class FounderResearchAgent:
    """
    An agent that performs a comprehensive background search on a founder
    using the Tavily API to create a rich context for analysis.
    """
    def __init__(self, tavily_api_key: str):
        self.client = TavilyClient(api_key=tavily_api_key)

    def research_founder(self, founder_name: str, founder_role: str, urls: list[str]) -> str:
        """
        Executes a targeted search to gather a founder's professional background.

        Args:
            founder_name (str): The full name of the founder.
            founder_role (str): Their role ('technical' or 'non-technical').
            urls (list[str]): Their provided profile URLs to guide the search.

        Returns:
            A consolidated string of research context from various sources.
        """
        print(f"Agent [Research]: Starting comprehensive background search for {founder_name}...")

        # Create a single, powerful query. Including URLs helps Tavily find the exact profiles.
        # This is more efficient than searching for each URL separately.
        url_str = " ".join(urls)
        query = f"Professional background, skills, and projects of {founder_name}. Include information from these profiles if possible: {url_str}"

        try:
            # Use one 'advanced' search call per founder for maximum context with minimum credit usage.
            # include_raw_content is crucial for getting the text for our analysis agents.
            response = self.client.search(
                query=query,
                search_depth="advanced",
                max_results=5, # Get top 5 relevant pages
                include_raw_content=True
            )
            
            # Consolidate the content from all search results into one block of text
            consolidated_context = f"--- Research Dossier for {founder_name} ---\n\n"
            for result in response.get('results', []):
                consolidated_context += f"Source: {result.get('url')}\n"
                consolidated_context += f"Content: {result.get('raw_content')}\n\n---\n\n"
            
            print(f"Agent [Research]: Successfully compiled dossier for {founder_name}.")
            return consolidated_context

        except Exception as e:
            print(f"Agent [Research]: An error occurred during Tavily search for {founder_name}: {e}")
            return f"Error: Could not retrieve research for {founder_name}."