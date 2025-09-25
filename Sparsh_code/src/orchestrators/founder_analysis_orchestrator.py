# src/orchestrators/founder_analysis_orchestrator.py
import os
import sys
import json
from typing import Any, Dict, List

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from src.core.base_agent import BaseAgent
from src.agents.research.search_agent import SearchAgent
from src.agents.research.founder_research_agent import FounderResearchAgent
from src.agents.analysis.tech_profile_assessor_agent import TechProfileAssessorAgent
from src.agents.analysis.business_acumen_assessor_agent import BusinessAcumenAssessorAgent
from src.agents.synthesis.team_synergy_agent import TeamSynergyAgent
from src.agents.synthesis.showcase_reporting_agent import ShowcaseReportingAgent

class FounderAnalysisOrchestrator(BaseAgent):
    """
    Orchestrates the entire founder analysis workflow using a research-first approach.
    """
    def __init__(self, api_key: str, tavily_api_key: str, model: str = "claude-3-haiku-20240307"):
        super().__init__(model, api_key)
        
        search_agent = SearchAgent(api_key=tavily_api_key)
        self.research_agent = FounderResearchAgent(search_agent)
        
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
            
    def run(self, team_data: Dict[str, Any]) -> Dict[str, Any]:
        print("--- UNICORN RADAR: STARTING FULL FOUNDER ANALYSIS (RESEARCH WORKFLOW) ---")
        
        pipeline_errors, team_assessments = [], []

        for founder in team_data.get("founders", []):
            print(f"\n--- Processing Founder: {founder['name']} ({founder['role']}) ---")
            try:
                research_context = self.research_agent.research_founder(
                    founder_name=founder["name"],
                    urls=founder.get("urls", [])
                )
                if "Error:" in research_context: raise ValueError(research_context)
                self._log_intermediate_output(research_context)

                print(f"--- Assessing Founder: {founder['name']} ---")
                assessment = {}
                if founder['role'] == 'technical':
                    assessment['technical'] = self.tech_assessor.assess(research_context)
                    assessment['business'] = self.biz_assessor.assess(research_context)
                elif founder['role'] == 'non-technical':
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

    test_team_data = { "founders": [
            { "name": "Sparsh Tyagi", "role": "technical", "urls": ["https://www.linkedin.com/in/sparsh-tyagi/", "https://github.com/SparshTyagi"]},
            { "name": "Valentin Hornung", "role": "technical", "urls": ["https://www.linkedin.com/in/valentin-hornung/", "https://github.com/muhuuh"]},
            { "name": "Carolin Spitzer", "role": "non-technical", "urls": ["https://www.linkedin.com/in/carolin-spitzer/"]}
        ]}
    
    orchestrator = FounderAnalysisOrchestrator(api_key=api_key, tavily_api_key=tavily_api_key)
    final_analysis_output = orchestrator.run(test_team_data)

    print("\n\n--- FINAL ORCHESTRATOR OUTPUT ---")
    print(json.dumps(final_analysis_output, indent=2))