# src/agents/research/search_agent.py
from tavily import TavilyClient
import time

class SearchAgent:
    """An agent dedicated to executing search queries using the Tavily API."""
    def __init__(self, api_key: str):
        self.client = TavilyClient(api_key=api_key)

    def search(self, queries: list[str], search_depth: str = "basic") -> tuple[str, list[dict]]:
        """Executes searches, consolidates content, and de-duplicates sources."""
        print(f"Agent [Search]: Executing {len(queries)} search(es) with depth '{search_depth}'...")
        consolidated_context = ""
        unique_sources = {}
        
        for i, query in enumerate(queries):
            print(f"\n--- Searching Query {i+1}/{len(queries)}: '{query}' ---")
            try:
                search_result = self.client.search(
                    query=query, search_depth="advanced", max_results=3, include_raw_content=True
                )
                
                print(f"Found {len(search_result.get('results', []))} results for query.")

                for res in search_result.get('results', []):
                    if res.get('url') and res['url'] not in unique_sources:
                        unique_sources[res['url']] = {'title': res.get('title'), 'url': res.get('url')}
                        if res.get('raw_content'):
                            consolidated_context += f"--- Source (URL: {res['url']}) ---\n{res['raw_content']}\n\n"
            except Exception as e:
                print(f"Error: Search for query '{query}' failed. Error: {e}")
        
        return consolidated_context, list(unique_sources.values())