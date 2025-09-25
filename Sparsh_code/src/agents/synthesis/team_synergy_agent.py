# src/agents/synthesis/team_synergy_agent.py
import os
import sys
import json
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from src.core.base_agent import BaseAgent

class TeamSynergyAgent(BaseAgent):
    """
    Analyzes the entire founding team for balance, synergy, and potential gaps.
    """
    def analyze(self, team_assessments: list[dict]) -> dict:
        """
        Generates a holistic analysis of the team's composition.

        Args:
            team_assessments (list[dict]): A list of individual assessment reports
                                            from the other assessor agents.
        Returns:
            A dictionary containing the final team synergy analysis.
        """
        print("Agent [Synergy]: Analyzing team composition for synergy and balance...")
        
        assessments_str = json.dumps(team_assessments, indent=2)

        prompt = f"""
        You are a senior partner at a venture capital firm. Your task is to provide a final, holistic analysis of a founding team based on their individual profiles and scores.

        **Individual Founder Assessments:**
        {assessments_str}

        **Your Analysis Must Cover:**
        1.  **Team Balance:** Is there a good mix of technical and business expertise? Is one side significantly stronger or weaker?
        2.  **Collective Strengths:** What makes this team compelling *as a unit*?
        3.  **Key Gaps & Risks:** What critical skillsets (e.g., sales, marketing, deep tech expertise) are missing from the founding team? This is the most important part of your analysis.
        4.  **Overall Potential:** Provide a final grade for the team's overall potential (A, B, C) and a justification.

        Your response must be a JSON object with this exact schema:
        {{
          "team_balance_assessment": "<Your analysis of the tech/business balance>",
          "collective_strengths": ["<List of 2-3 key strengths of the team as a whole>"],
          "identified_gaps": ["<List of 1-2 critical missing skills or experience>"],
          "overall_potential": {{
            "grade": "<A | B | C>",
            "justification": "<A concise reason for your overall grading of the team.>"
          }}
        }}
        """
        
        messages = [
            {"role": "system", "content": "You are a VC senior partner evaluating team dynamics."},
            {"role": "user", "content": prompt}
        ]
        
        return self._send_llm_request(messages)