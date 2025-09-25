# /Complete workflow/agents/research/github_agent.py
import os
import sys
import json
from dotenv import load_dotenv
from tavily import TavilyClient

# Add the project root directory to the Python path
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.append(PROJECT_ROOT)

from core.base_openrouter_agent import BaseOpenRouterAgent

# --- Prompt is now a constant inside the Python file ---
GITHUB_ANALYSIS_PROMPT = """
You are an expert CTO performing technical due diligence on a software developer's GitHub profile. Based *only* on the provided detailed context, which includes a profile overview and summaries of their featured repositories, your task is to perform a comprehensive analysis.

**SEARCH CONTEXT:**
---
{search_context}
---

**Your Task:**
Extract, analyze, and summarize the developer's GitHub presence into a structured JSON object. Focus on tangible evidence of skill, project complexity, and influence.

- Identify the most prominent programming languages.
- List 1-3 of their most notable or complex repositories mentioned in the context.
- From the repository summaries, assess the technical complexity and purpose of their main projects.
- Provide a concise summary of their primary technical focus or domain (e.g., "Web Development with React," "Data Engineering," "Cloud Infrastructure").
- If no information is found for a field, use an empty list or "N/A".

Your response must be a single JSON object with this exact schema:
{{
  "User_Profile": "<A concise summary of their profile, e.g., 'A software engineer with a focus on open-source contributions and web development.'>",
  "key_languages": ["<List of languages, e.g., 'Python', 'TypeScript'>"],
  "notable_repositories": ["<List of repo names, e.g., 'unicorn-radar-backend'>"],
  "project_complexity_assessment": "<Analyze the complexity and purpose of their key projects based on the README summaries. Is this a simple portfolio or complex software?>",
  "technical_focus": "<A concise summary of their likely expertise, e.g., 'Frontend Development with a focus on data visualization.'>"
}}
"""

class GithubAgent(BaseOpenRouterAgent):
    """
    An agent for performing in-depth analysis of a developer's GitHub profile.
    It directly extracts content from the profile and featured repositories to
    provide a rich context for LLM analysis.
    """
    def __init__(self, openrouter_api_key: str, tavily_api_key: str):
        super().__init__(api_key=openrouter_api_key)
        if not tavily_api_key:
            raise ValueError("Tavily API key is not set.")
        self.tavily_client = TavilyClient(api_key=tavily_api_key)
        # The prompt path is no longer needed.

    def _extract_repo_urls_from_content(self, profile_content: str, base_url: str) -> list[str]:
        """Uses an LLM to parse the raw content and find repository URLs."""
        print("  -> Using LLM to extract repository URLs from profile content...")
        
        prompt = f"""
        From the following raw web page content of a GitHub profile, extract the full URLs of the user's pinned or featured repositories.
        The base URL for the profile is {base_url}. The repository URLs will start with this base URL.

        **Content:**
        ---
        {profile_content[:15000]} 
        ---

        Your response must be a single JSON object with a single key "repository_urls", which is a list of strings.
        Example: {{"repository_urls": ["https://github.com/user/repo1", "https://github.com/user/repo2"]}}
        """
        
        messages = [
            {"role": "system", "content": "You are a precise information extraction tool. Your only task is to find GitHub repository URLs in text and return them as a JSON list."},
            {"role": "user", "content": prompt}
        ]
        
        response = self._send_llm_request(messages)
        return response.get("repository_urls", []) if isinstance(response, dict) else []

    def analyze_profile(self, github_url: str) -> dict:
        print(f"Agent [GitHub]: Starting direct extraction analysis for: {github_url}")
        if not github_url or "github.com" not in github_url:
            return {"error": "Invalid GitHub URL provided."}
            
        try:
            # --- Stage 1: Extract content from the main profile page ---
            print(f"  -> Stage 1: Extracting content from main profile URL...")
            profile_extract_result = self.tavily_client.extract([github_url], extract_depth='advanced')
            
            if not profile_extract_result or not profile_extract_result.get('results'):
                return {"error": f"Failed to extract content from {github_url}"}
            
            profile_content = profile_extract_result['results'][0].get('raw_content', '')
            if not profile_content:
                return {"error": "Extracted content was empty."}

            # --- Stage 2: Parse the profile content to find repository URLs ---
            top_repo_urls = self._extract_repo_urls_from_content(profile_content, github_url)

            # --- Stage 3: Extract content from the discovered repositories ---
            consolidated_repos_content = "No specific repositories were analyzed."
            if top_repo_urls:
                print(f"  -> Stage 3: Found {len(top_repo_urls)} repos. Extracting their content: {top_repo_urls}")
                repo_extract_results = self.tavily_client.extract(top_repo_urls, extract_depth='advanced')
                
                content_parts = []
                for result in repo_extract_results.get('results', []):
                    content_parts.append(f"--- REPO: {result['url']} ---\n{result.get('raw_content', 'No content found.')}\n\n")
                consolidated_repos_content = "".join(content_parts)
            else:
                print("  -> Stage 3: No featured repository URLs found by the LLM.")

            # --- Stage 4: Consolidate all content and generate the final analysis ---
            print("  -> Stage 4: Consolidating all extracted content for final analysis...")
            final_context = (
                f"**Main Profile Page Content:**\n{profile_content[:5000]}\n\n"
                f"**Featured Repositories Content (from their READMEs):**\n{consolidated_repos_content}"
            )

            # Use the in-file prompt constant directly













            prompt = GITHUB_ANALYSIS_PROMPT.format(search_context=final_context)
            messages = [{"role": "system", "content": "You are a CTO analyzing GitHub activity from extracted web content, outputting a JSON object."}, {"role": "user", "content": prompt}]
            
            final_analysis = self._send_llm_request(messages)
            print(f"Agent [GitHub]: Finished analysis for {github_url}")
            return final_analysis

        except Exception as e:
            print(f"An unexpected fatal error occurred in GithubAgent for {github_url}: {e}")
            return {"error": str(e)}

# ==============================================================================
# Test Block for Standalone Execution
# ==============================================================================
if __name__ == '__main__':
    print("--- Running GitHub Agent Standalone Test (Self-Contained Prompt) ---")
    
    dotenv_path = os.path.join(PROJECT_ROOT, '.env')
    load_dotenv(dotenv_path=dotenv_path)
    
    openrouter_api_key = os.getenv("API_KEY")
    tavily_api_key = os.getenv("TAVILY_API_KEY")

    if not openrouter_api_key or not tavily_api_key:
        raise ValueError("API_KEY and TAVILY_API_KEY must be set in your .env file to run the test.")

    agent = GithubAgent(openrouter_api_key=openrouter_api_key, tavily_api_key=tavily_api_key)
    
    test_github_url = "https://github.com/karpathy"
    
    analysis_result = agent.analyze_profile(test_github_url)
    
    print("\n--- ANALYSIS COMPLETE ---")
    print(json.dumps(analysis_result, indent=2))
    print("--- End of Test ---")