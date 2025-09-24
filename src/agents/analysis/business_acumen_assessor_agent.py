# src/agents/analysis/business_acumen_assessor_agent.py
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from src.core.base_agent import BaseAgent

class BusinessAcumenAssessorAgent(BaseAgent):
    """
    Analyzes and scores a non-technical founder's profile for business acumen.
    """
    def assess(self, linkedin_data: dict | None) -> dict:
        """
        Performs a quantitative and qualitative assessment of a business profile.
        
        Args:
            linkedin_data (dict | None): Parsed data from a LinkedIn profile.

        Returns:
            A dictionary containing scores and a summary.
        """
        print("Agent [BusinessAssessor]: Assessing business profile...")
        if not linkedin_data or not linkedin_data.get("experience"):
            return {"scores": {}, "summary": {"error": "LinkedIn data is missing or incomplete."}}
        
        scores = {}
        
        # --- Experience Scoring ---
        # A simple scoring model: +3 for Founder/CEO roles, +2 for Director/VP, +1 for other senior roles
        experience_score = 0
        is_prior_founder = False
        for exp in linkedin_data.get("experience", []):
            role = exp.get("role", "").lower()
            if "founder" in role or "chief executive officer" in role or "ceo" in role:
                experience_score += 3
                is_prior_founder = True
            elif "director" in role or "vp" in role or "vice president" in role:
                experience_score += 2
            elif "manager" in role or "lead" in role or "head of" in role:
                experience_score += 1

        if is_prior_founder:
            scores["founder_experience_score"] = {"value": 10, "grade": "A", "note": "Has prior founding experience."}
        else:
            scores["founder_experience_score"] = {"value": 6, "grade": "C+", "note": "Appears to be a first-time founder."}

        if experience_score >= 5:   scores["career_progression_score"] = {"value": 9, "grade": "A-", "note": "Demonstrates strong career progression and leadership."}
        elif experience_score >= 3: scores["career_progression_score"] = {"value": 8, "grade": "B+", "note": "Solid track record of senior roles."}
        else:                       scores["career_progression_score"] = {"value": 7, "grade": "B", "note": "Shows relevant professional experience."}
        
        # --- LLM-based Qualitative Summary ---
        synthesis_prompt = f"""
        Based on the following LinkedIn experience, provide a summary of this person's business acumen. Identify their likely core competency (e.g., Sales, Marketing, Operations, Product Management).

        **Experience:**
        {linkedin_data.get('experience')}

        Your response must be a JSON object with this schema:
        {{
          "core_competency": "<Identified core business skill>",
          "execution_capability_assessment": "<Briefly assess their potential to execute and lead a company.>"
        }}
        """
        messages = [
            {"role": "system", "content": "You are a VC analyst evaluating a founder's business background."},
            {"role": "user", "content": synthesis_prompt}
        ]

        summary = self._send_llm_request(messages)

        return {
            "scores": scores,
            "summary": summary or {"error": "Failed to generate summary."}
        }