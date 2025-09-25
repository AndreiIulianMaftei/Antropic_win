# src/agents/analysis/business_acumen_assessor_agent.py
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from src.core.base_agent import BaseAgent

class BusinessAcumenAssessorAgent(BaseAgent):
    """
    Analyzes a non-technical founder's profile from a consolidated research dossier.
    """
    def assess(self, research_context: str) -> dict:
        """
        Performs assessment based on a rich text context from the research agent.
        """
        print("Agent [BusinessAssessor]: Assessing business profile from research dossier...")
        
        prompt = f"""
        You are a Venture Partner evaluating a founder's business background based *only* on the provided research dossier.

        **Research Dossier:**
        ---
        {research_context}
        ---

        **Your Task:**
        1.  Extract key experiences, previous companies, and indicators of leadership or founding experience.
        2.  Based *only* on this information, provide a summary and scores.
        3.  If you find evidence of prior founding experience, score that highly. If not, score it neutrally and note it. Do not invent information.

        Your response must be a single JSON object with this exact schema:
        {{
          "scores": {{
            "founder_experience_score": {{
              "value": "<Score 1-10. Score high (e.g., 9-10) for prior founding experience, low (e.g., 5-6) otherwise.>",
              "grade": "<A-F>",
              "note": "<e.g., 'Clear evidence of prior founding experience.' or 'Appears to be a first-time founder based on context.'>"
            }},
            "career_progression_score": {{
              "value": "<Score 1-10 based on seniority of roles and quality of companies mentioned.>",
              "grade": "<A-F>",
              "note": "<Justify your score, e.g., 'Demonstrates strong career progression with leadership roles at notable companies.'>"
            }}
          }},
          "summary": {{
            "core_competency": "<Identify their likely core business skill (e.g., Sales, Marketing, Operations) from the text>",
            "execution_capability_assessment": "<Briefly assess their potential to execute and lead a company.>"
          }}
        }}
        """
        messages = [
            {"role": "system", "content": "You are a VC Partner evaluating a business founder's dossier."},
            {"role": "user", "content": prompt}
        ]
        
        return self._send_llm_request(messages) or {"error": "Failed to generate assessment."}