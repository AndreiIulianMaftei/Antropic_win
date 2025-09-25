# /Complete workflow/founder_analysis_orchestrator.py
import os
import sys
import asyncio
import json
from typing import Dict, Any

# Adjust imports to use the new OpenAlex agent
from app.agents.linkedin_agent import create_linkedin_agent, fetch_profile_via_agent
from app.agents.openalex_agent import fetch_openalex_data # CORRECTED IMPORT
from app.agents.github_agent import GithubAgent

class FounderAnalysisOrchestrator:
    """
    Orchestrates the founder data gathering workflow using specialized agents.
    """
    def __init__(self, openrouter_api_key: str, tavily_api_key: str):
        print("Initializing agents...")
        # Pydantic-AI / Gemini based agents
        self.linkedin_agent = create_linkedin_agent()
        # The OpenAlex agent is now just a function call, no initialization needed.
        
        # OpenRouter based agent
        self.github_agent = GithubAgent(
            openrouter_api_key=openrouter_api_key,
            tavily_api_key=tavily_api_key
        )
        print("All agents initialized.")

    async def run(self, prospect_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Asynchronously processes a list of founders to gather data from various sources.
        """
        founders_list = prospect_data.get("data", {}).get("teamList", [])
        all_founder_tasks = [self._process_founder(founder) for founder in founders_list]
        processed_founders = await asyncio.gather(*all_founder_tasks)
        
        prospect_data["data"]["teamList"] = processed_founders
        prospect_data["analyzed_at"] = asyncio.get_event_loop().time()
        
        return prospect_data

    async def _process_founder(self, founder_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Gathers analysis for a single founder by running all relevant tasks concurrently.
        """
        founder_name = founder_data.get("name", "Unknown Founder")
        print(f"\n--- Processing Founder: {founder_name} ---")
        tasks = {}
        
        # Process each task sequentially
        results = []
        task_keys = []

        if founder_data.get("linkedin"):
            print(f"  -> Processing LinkedIn: {founder_data['linkedin']}")
            try:
                result = await fetch_profile_via_agent(self.linkedin_agent, founder_data["linkedin"])
                results.append(result)
                task_keys.append("linkedin_analysis")
            except Exception as e:
                results.append(e)
                task_keys.append("linkedin_analysis")

        if founder_data.get("github"):
            print(f"  -> Processing GitHub: {founder_data['github']}")
            try:
                result = await asyncio.to_thread(self.github_agent.analyze_profile, founder_data["github"])
                results.append(result)
                task_keys.append("github_analysis")
            except Exception as e:
                results.append(e)
                task_keys.append("github_analysis")

        if founder_data.get("university"):
            print(f"  -> Processing OpenAlex: {founder_name} at {founder_data['university']}")
            try:
                result = await fetch_openalex_data(founder_name, founder_data["university"])
                results.append(result)
                task_keys.append("openalex_analysis")
            except Exception as e:
                results.append(e)
                task_keys.append("openalex_analysis")

        founder_data["analysis"] = {}
        
        for i, result in enumerate(results):
            key = task_keys[i]
            if isinstance(result, Exception):
                print(f"  -> ERROR for {key}: {result}")
                founder_data["analysis"][key] = {"error": str(result)}
            else:
                # Handle both Pydantic models and regular dicts
                if hasattr(result, 'model_dump'):
                    founder_data["analysis"][key] = result.model_dump()
                else:
                    founder_data["analysis"][key] = result
        
        print(f"--- Finished Processing Founder: {founder_name} ---")
        return founder_data