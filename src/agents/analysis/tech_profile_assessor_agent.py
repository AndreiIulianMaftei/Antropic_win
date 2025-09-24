# src/agents/analysis/tech_profile_assessor_agent.py
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from src.core.base_agent import BaseAgent

class TechProfileAssessorAgent(BaseAgent):
    """
    Analyzes and scores a technical founder's profile based on objective criteria.
    """
    def assess(self, gscholar_data: dict | None, github_data: dict | None) -> dict:
        """
        Performs a quantitative and qualitative assessment of a technical profile.

        Args:
            gscholar_data (dict | None): Parsed data from a Google Scholar profile.
            github_data (dict | None): Parsed data from a GitHub profile.

        Returns:
            A dictionary containing scores and a summary.
        """
        print("Agent [TechAssessor]: Assessing technical profile...")
        
        scores = {}
        # --- H-Index Scoring (Academic Impact) ---
        h_index = (gscholar_data or {}).get("h_index", 0)
        if h_index >= 30: scores["academic_impact_score"] = {"value": 10, "grade": "A", "note": "Exceptional academic influence."}
        elif h_index >= 20: scores["academic_impact_score"] = {"value": 9, "grade": "A-", "note": "Very strong academic influence."}
        elif h_index >= 10: scores["academic_impact_score"] = {"value": 8, "grade": "B+", "note": "Significant academic influence."}
        elif h_index >= 5:  scores["academic_impact_score"] = {"value": 7, "grade": "B", "note": "Established academic record."}
        else:               scores["academic_impact_score"] = {"value": 5, "grade": "C", "note": "Early-stage academic record."}

        # --- GitHub Scoring (Engineering Influence) ---
        total_stars = 0
        if github_data and github_data.get("pinned_repositories"):
            for repo in github_data["pinned_repositories"]:
                total_stars += repo.get("stars", 0)
        
        if total_stars >= 1000: scores["engineering_influence_score"] = {"value": 10, "grade": "A", "note": "Highly influential open-source contributor."}
        elif total_stars >= 500:  scores["engineering_influence_score"] = {"value": 9, "grade": "A-", "note": "Strong open-source presence."}
        elif total_stars >= 100:  scores["engineering_influence_score"] = {"value": 8, "grade": "B+", "note": "Recognized contributions to open-source."}
        elif total_stars >= 20:   scores["engineering_influence_score"] = {"value": 7, "grade": "B", "note": "Active and engaged in open-source."}
        else:                     scores["engineering_influence_score"] = {"value": 5, "grade": "C", "note": "Personal or early-stage projects."}

        # --- LLM-based Qualitative Summary ---
        synthesis_prompt = self._create_synthesis_prompt(gscholar_data, github_data)
        messages = [
            {"role": "system", "content": "You are a CTO evaluating a technical founder. Based on their profile data, provide a concise summary of their deep tech expertise and potential impact. Identify their core domain (e.g., AI/ML, Quantum Computing)."},
            {"role": "user", "content": synthesis_prompt}
        ]
        
        summary = self._send_llm_request(messages)

        return {
            "scores": scores,
            "summary": summary or {"error": "Failed to generate summary."}
        }

    def _create_synthesis_prompt(self, gscholar_data, github_data):
        prompt = "Synthesize the following technical profile data into a report.\\n\\n"
        if gscholar_data:
            prompt += f"**Google Scholar Profile:**\\n- H-Index: {gscholar_data.get('h_index')}\\n- Top Publication: {gscholar_data.get('top_publications', [{}])[0].get('title', 'N/A')}\\n\\n"
        if github_data:
            prompt += f"**GitHub Profile:**\\n- Bio: {github_data.get('bio')}\\n- Pinned Repositories exist: {bool(github_data.get('pinned_repositories'))}\\n\\n"
        
        prompt += """
        Your response must be a JSON object with this schema:
        {
          "domain_expertise": "<Identify their primary field of deep tech expertise>",
          "impact_assessment": "<Provide a brief assessment of their potential for impactful work.>"
        }
        """
        return prompt