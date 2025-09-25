# src/agents/analysis/tech_profile_assessor_agent.py
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from src.core.base_agent import BaseAgent

class TechProfileAssessorAgent(BaseAgent):
    """
    Analyzes a technical founder's profile from a consolidated research dossier.
    """
    def assess(self, research_context: str) -> dict:
        """
        Performs assessment based on a rich text context from the research agent.
        """
        print("Agent [TechAssessor]: Assessing technical profile from research dossier...")
        
        prompt = f"""
        You are a seasoned CTO performing technical due diligence on a founder based *only* on the provided research dossier.

        **Research Dossier:**
        ---
        {research_context}
        ---

        **Your Task:**
        1.  Scour the dossier for any mention of GitHub projects, technical skills, or academic achievements (like an H-Index).
        2.  Based *only* on the information present, provide a summary and scores.
        3.  If specific information (like an H-Index or notable projects) is NOT found, explicitly state that and assign a neutral/low score for that category. Do not invent information.

        Your response must be a single JSON object with this exact schema:
        {{
          "scores": {{
            "academic_impact_score": {{
              "value": "<Score 1-10. Score low (e.g., 5) if no academic record found.>",
              "grade": "<A-F>",
              "note": "<Justify your score, e.g., 'No publications or H-Index found in the provided context.'>"
            }},
            "engineering_influence_score": {{
              "value": "<Score 1-10 based on GitHub projects, stars, or contributions found. Score low if not found.>",
              "grade": "<A-F>",
              "note": "<Justify your score, e.g., 'Found several relevant projects on GitHub like X and Y.'>"
            }}
          }},
          "summary": {{
            "domain_expertise": "<Identify their primary field of deep tech expertise based on the text>",
            "impact_assessment": "<Provide a brief assessment of their potential for impactful work based on the dossier.>"
          }}
        }}
        """
        messages = [
            {"role": "system", "content": "You are a CTO evaluating a technical founder's dossier."},
            {"role": "user", "content": prompt}
        ]
        
        return self._send_llm_request(messages) or {"error": "Failed to generate assessment."}