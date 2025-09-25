# src/agents/research/founder_research_agent.py
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from src.agents.research.search_agent import SearchAgent

class FounderResearchAgent:
    """
    Uses the SearchAgent infrastructure to perform PRECISE content extraction from a list of URLs.
    """
    def __init__(self, search_agent: SearchAgent):
        self.search_agent = search_agent

    def research_founder(self, founder_name: str, urls: list[str]) -> str:
        """
        Extracts content from a list of URLs by performing a targeted search for each
        and strictly filtering the results to match the source URL.

        Args:
            founder_name (str): The full name of the founder (for labeling).
            urls (list[str]): The specific profile URLs to extract content from.

        Returns:
            A consolidated string of research context from ONLY the provided URLs.
        """
        print(f"Agent [Research]: Starting targeted content extraction for {founder_name} from {len(urls)} URLs...")
        
        consolidated_context = f"--- Research Dossier for {founder_name} ---\n\n"

        # --- CRITICAL REFACTOR ---
        # We now iterate through each URL to ensure we only get content from that specific source.
        for url in urls:
            print(f"Agent [Research]: Targeting URL: {url}")
            # We search for the URL itself, which will make it the top result.
            # We ask for only a few results to be efficient.
            search_context, sources = self.search_agent.search(queries=[url], search_depth="advanced")
            
            # This is the most important step: Find the specific result that matches our target URL.
            found_content = False
            for result_url, result_content in zip(sources, search_context.split("--- Source")):
                # The search_context is a big string, we need to parse it carefully
                if url in result_url.get('url', ''):
                    consolidated_context += f"--- Source (URL: {url}) ---\n"
                    # We need to find the content associated with this specific source
                    # A simple way is to split the context and find the right block
                    content_blocks = search_context.split("--- Source")
                    for block in content_blocks:
                        if url in block:
                             # Extract the actual content part of the block
                            content_part = block.split("---\n", 1)[-1]
                            consolidated_context += content_part
                            found_content = True
                            break # Found the content for this URL
                    if found_content:
                        break # Move to the next URL
            
            if not found_content:
                print(f"Agent [Research]: WARNING - Could not isolate content for the specific URL: {url}")
                consolidated_context += f"--- Source (URL: {url}) ---\n[Content extraction failed for this specific URL]\n\n"
        # --- END REFACTOR ---

        if not consolidated_context.strip():
            error_message = f"Error: Could not retrieve any content for {founder_name} from the provided URLs."
            print(f"Agent [Research]: {error_message}")
            return error_message

        print(f"Agent [Research]: Successfully compiled precise dossier for {founder_name}.")
        return consolidated_context