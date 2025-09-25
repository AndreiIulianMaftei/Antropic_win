# src/orchestrators/founder_analysis_orchestrator.py
import os
import sys
import json
import asyncio # << Step 1.1: Import asyncio
from typing import Any, Dict, List

# --- Core Imports ---
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src.core.base_agent import BaseAgent

# --- Agent Imports ---
# << Step 1.1: Import the specialized agents instead of the generic research agent
from src.agents.research.search_agent import SearchAgent
# NOTE: The following files (linkedin_agent.py, openalex_agent.py) should be placed
# in the 'src/agents/research/' directory for these imports to work.
from backend.app.agents.linkedin_agent.py import create_linkedin_agent, fetch_profile_via_agent
from backend.app.agents.openalex_agent.py import create_openalex_agent, fetch_author_metrics

from src.agents.analysis.tech_profile_assessor_agent import TechProfileAssessorAgent
from src.agents.analysis.business_acumen_assessor_agent import BusinessAcumenAssessorAgent
from src.agents.synthesis.team_synergy_agent import TeamSynergyAgent
from src.agents.synthesis.showcase_reporting_agent import ShowcaseReportingAgent

class FounderAnalysisOrchestrator(BaseAgent):
    """
    Orchestrates the entire founder analysis workflow using a multi-agent,
    source-specific research approach.
    """
    def __init__(self, api_key: str, tavily_api_key: str, model: str = "x-ai/grok-4-fast:free"):
        super().__init__(model, api_key)
        
        # << Step 1.1: Instantiate all required agents
        # General web search agent (for GitHub, news, etc.)
        self.search_agent = SearchAgent(api_key=tavily_api_key)
        
        # Specialized agents for structured data
        self.linkedin_agent = create_linkedin_agent()
        self.openalex_agent = create_openalex_agent()
        
        # Analysis and synthesis agents remain the same
        self.tech_assessor = TechProfileAssessorAgent(model, api_key)
        self.biz_assessor = BusinessAcumenAssessorAgent(model, api_key)
        self.synergy_agent = TeamSynergyAgent(model, api_key)
        self.reporting_agent = ShowcaseReportingAgent(model, api_key)
        
        self.intermediate_log_path = "intermediate_outputs/run_log.txt"
        self._setup_logging()

    def _setup_logging(self):
        output_dir = os.path.dirname(self.intermediate_log_path)
        if not os.path.exists(output_dir): os.makedirs(output_dir)
        with open(self.intermediate_log_path, "w", encoding="utf-8") as f:
            f.write("--- UNICORN RADAR INTERMEDIATE OUTPUT LOG ---\n\n")

    def _log_intermediate_output(self, content: str):
        with open(self.intermediate_log_path, "a", encoding="utf-8") as f: f.write(content)

    # << Step 1.3: New asynchronous method for intelligent, source-specific research
    async def _research_founder_async(self, founder: Dict[str, Any]) -> str:
        """
        Asynchronously gathers and consolidates research from multiple sources
        based on the founder's provided URLs and role.
        """
        print(f"Agent [Orchestrator]: Starting intelligent research for {founder['name']}...")
        
        tasks = []
        # Dispatch research tasks based on URLs
        for url in founder.get("urls", []):
            if "linkedin.com" in url:
                print(f"  -> Found LinkedIn URL, dispatching to LinkedIn Agent.")
                tasks.append(fetch_profile_via_agent(self.linkedin_agent, url))
            elif "github.com" in url:
                print(f"  -> Found GitHub URL, dispatching to Search Agent.")
                # Use the search agent to get a summary of the GitHub profile/repos
                query = f"Summarize the projects and activity of the GitHub user profile at {url}"
                # The search_agent is synchronous, so we run it in a thread pool
                # to avoid blocking the async event loop.
                tasks.append(asyncio.to_thread(self.search_agent.search, [query]))

        # For technical founders, always search for academic background
        if founder['role'] in ['technical', 'both']:
            print(f"  -> Technical role detected, dispatching to OpenAlex Agent.")
            # TODO: Future enhancement could be to extract affiliation from LinkedIn profile
            tasks.append(fetch_author_metrics(self.openalex_agent, founder['name']))

        # Run all dispatched tasks concurrently
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Consolidate results into a single dossier
        consolidated_context = f"--- COMPREHENSIVE RESEARCH DOSSIER FOR: {founder['name']} ---\n\n"
        
        for result in results:
            if isinstance(result, Exception):
                consolidated_context += f"--- An error occurred during research ---\n{str(result)}\n\n"
            # Handle LinkedIn Agent output (ProfileSummary Pydantic model)
            elif hasattr(result, 'experience_summary'): 
                consolidated_context += f"--- LinkedIn Profile Summary ---\n{json.dumps(result.model_dump(), indent=2)}\n\n"
            # Handle OpenAlex Agent output (AuthorMetrics Pydantic model)
            elif hasattr(result, 'works_count'):
                consolidated_context += f"--- Academic & Research Metrics (OpenAlex) ---\n{json.dumps(result.model_dump(), indent=2)}\n\n"
            # Handle Search Agent output (tuple of context and sources)
            elif isinstance(result, tuple) and len(result) == 2:
                search_content, _ = result
                consolidated_context += f"--- GitHub / Web Search Summary ---\n{search_content}\n\n"
            else:
                consolidated_context += f"--- Other Research Data ---\n{str(result)}\n\n"

        print(f"Agent [Orchestrator]: Finished intelligent research for {founder['name']}.")
        return consolidated_context

    # << Step 1.2: Main run method is now asynchronous
    async def run(self, team_data: Dict[str, Any]) -> Dict[str, Any]:
        print("--- UNICORN RADAR: STARTING FULL FOUNDER ANALYSIS (ASYNC WORKFLOW) ---")
        
        pipeline_errors, team_assessments = [], []

        for founder in team_data.get("founders", []):
            print(f"\n--- Processing Founder: {founder['name']} ({founder['role']}) ---")
            try:
                # << Step 1.3: Call the new async research method
                research_context = await self._research_founder_async(founder)

                if "Error:" in research_context: raise ValueError(research_context)
                self._log_intermediate_output(research_context)

                print(f"--- Assessing Founder: {founder['name']} ---")
                assessment = {}
                # The assessment logic remains the same, just with better data
                if founder['role'] == 'technical':
                    assessment['technical'] = self.tech_assessor.assess(research_context)
                    assessment['business'] = self.biz_assessor.assess(research_context) # Tech founders can have business skills
                elif founder['role'] == 'non-technical':
                     assessment['business'] = self.biz_assessor.assess(research_context)
                elif founder['role'] == 'both':
                    assessment['technical'] = self.tech_assessor.assess(research_context)
                    assessment['business'] = self.biz_assessor.assess(research_context)

                team_assessments.append({ "name": founder["name"], "role": founder["role"], "assessment": assessment })

            except Exception as e:
                error_msg = f"Failed to process founder {founder['name']}. Reason: {e}"
                print(f"!!! {error_msg}")
                pipeline_errors.append({"stage": f"Research/Assess {founder['name']}", "error": str(e)})

        print("\n--- Analyzing Team Synergy & Creating Final Report---")
        synergy_analysis = self.synergy_agent.analyze(team_assessments)
        self._log_intermediate_output(f"\n\n--- SYNERGY ANALYSIS OUTPUT ---\n{json.dumps(synergy_analysis, indent=2)}\n")
        
        comprehensive_data = { "individual_assessments": team_assessments, "synergy_analysis": synergy_analysis }
        final_report = self.reporting_agent.create_report(comprehensive_data)
        
        return {
            "showcase_report": final_report,
            "comprehensive_data": comprehensive_data,
            "errors": pipeline_errors
        }

if __name__ == '__main__':
    from dotenv import load_dotenv
    load_dotenv()
    api_key = os.getenv("API_KEY")
    tavily_api_key = os.getenv("TAVILY_API_KEY")

    if not api_key or not tavily_api_key:
        raise ValueError("API_KEY and TAVILY_API_KEY must be set in your .env file.")

    # Note: Define the 'both' role for founders who are technical and non-technical
    test_team_data = { "founders": [
            { "name": "Yann LeCun", "role": "technical", "urls": ["https://www.linkedin.com/in/yann-lecun/"]},
            { "name": "Sheryl Sandberg", "role": "non-technical", "urls": ["https://www.linkedin.com/in/sherylsandberg/"]},
            { "name": "Vitalik Buterin", "role": "both", "urls": ["https://github.com/vbuterin"]}
        ]}
    
    orchestrator = FounderAnalysisOrchestrator(api_key=api_key, tavily_api_key=tavily_api_key)
    
    # << Step 1.2: Use asyncio.run() to execute the async main method
    final_analysis_output = asyncio.run(orchestrator.run(test_team_data))

    print("\n\n--- FINAL ORCHESTRATOR OUTPUT ---")
    print(json.dumps(final_analysis_output, indent=2))