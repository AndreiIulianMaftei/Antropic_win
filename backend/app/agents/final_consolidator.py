import os
import sys
import json
from typing import Dict, Any
from dotenv import load_dotenv

# Add the project root directory to the Python path
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.append(PROJECT_ROOT)

from app.core.base_openrouter_agent import BaseOpenRouterAgent


# --- The Master Prompt is defined as a constant within the file ---
FINAL_ANALYSIS_PROMPT = """
You are a Senior Investment Partner at a top-tier venture capital firm called "Unicorn Radar". Your task is to synthesize preliminary research and founder interview analyses into a single, comprehensive, and data-driven investment report for the executive committee.

You will be provided with two JSON objects:
1.  **RESEARCH_DATA**: Contains automated analysis of the founders' public profiles (LinkedIn, GitHub, academic records).
2.  **INTERVIEW_ANALYSIS**: Contains a structured summary and analysis of interviews conducted with the founders.

Your job is to act as the final human-in-the-loop, combining these quantitative and qualitative data points into a polished, final report.

**CONTEXTUAL DATA:**
---
<RESEARCH_DATA>
{research_data}
</RESEARCH_DATA>

<INTERVIEW_ANALYSIS>
{interview_analysis}
</INTERVIEW_ANALYSIS>
---

**YOUR TASK:**
Carefully review all the provided data and generate a single, valid JSON object that strictly adheres to the following schema. Do NOT add any text or markdown before or after the JSON object.

**JSON OUTPUT SCHEMA:**
{{
  "overallScore": <A float from 0.0 to 10.0 representing the overall investment potential. Use the following strict scale:
    - 0: Fundamentally non-viable business.
    - 1: Severe red flags in all areas.
    - 2: Deeply flawed concept or team.
    - 3: Significant weaknesses outweigh any strengths.
    - 4: Subpar opportunity with high risk.
    - 5: Average, has some potential but faces major hurdles.
    - 6: Decent, a solid team/idea that warrants consideration.
    - 7: Good, a compelling opportunity with a clear path forward.
    - 8: Excellent, strong potential for high returns, a top-tier deal.
    - 9: Outstanding, a potential category leader.
    - 10: Exceptional, a generational company, a must-invest.>,
  "disruptionProbability": <A float from 0.0 to 10.0 on the likelihood of disrupting its market. Use the following strict scale:
    - 0: No market, no innovation.
    - 1: Follower in a saturated market.
    - 2: Minor incremental improvement.
    - 3: Some differentiation but no real moat.
    - 4: Could capture a small niche.
    - 5: Has a unique feature, but not a game-changer.
    - 6: Could become a significant player in a niche.
    - 7: Has the potential to challenge incumbents.
    - 8: Could reshape a significant market segment.
    - 9: Has the potential to create a new market category.
    - 10: A paradigm shift, will redefine the industry.>,
  "teamSynergy": <A float from 0.0 to 10.0 assessing founder collaboration. Use the following strict scale:
    - 0: Openly hostile or conflicting.
    - 1: Complete lack of alignment.
    - 2: Poor communication and undefined roles.
    - 3: Frequent disagreements, unresolved tension.
    - 4: Functional but lacking trust or rapport.
    - 5: Professional and respectful, but no clear synergy.
    - 6: Good communication and aligned on vision.
    - 7: Proactively support each other, clear trust.
    - 8: Highly effective, amplify each other's strengths.
    - 9: Seamless collaboration, anticipate each other's needs.
    - 10: A truly rare and exceptionally high-functioning partnership.>,
  "complementaryScore": <A float from 0.0 to 10.0 on how well founders' skills complement each other. Use the following strict scale:
    - 0: No relevant skills on the team.
    - 1: Identical skill sets, massive gaps elsewhere.
    - 2: Significant overlap and critical roles un-filled.
    - 3: Some skill diversity but key areas (e.g., tech, product) are missing.
    - 4: Most skills are redundant.
    - 5: Covers basic needs but lacks depth in key areas.
    - 6: Reasonably well-rounded, covers major bases.
    - 7: Good balance of technical, product, and business skills.
    - 8: Strong, distinct expertise in all critical domains.
    - 9: Each founder is a 10/10 in their respective, essential domain.
    - 10: Perfect yin-yang, the ideal blend of visionary, builder, and seller.>,
  "researchDepth": {{
    "hIndex": <An integer representing the highest h-index found among the founders from the research data, or 0 if not available.>
  }},
  "founderHighlights": [
    // For each founder, create an object.
    {{
      "name": "<The founder's full name>",
      "highlights": [
        "<A key highlight based on their LinkedIn profile (e.g., 'Ex-Google AI researcher with 5 years of experience in NLP').>",
        "<A key highlight based on their GitHub profile (e.g., 'Lead contributor to a popular open-source data visualization library').>",
        "<A key highlight based on their educational background (e.g., 'PhD in Computer Science from Stanford University').>"
      ],
      "comments": "<A 1-2 sentence summary of the founder's strengths and potential weaknesses based on the research data.>"
    }}
  ],
  "interviewHighlights": [
    // For each key question/theme from the interview analysis, create an object.
    {{
      "question": "<The core question or theme from the interview (e.g., 'Co-founder Conflict Resolution').>",
      "summary": "<A concise summary of the founder's response and the AI's analysis of it.>",
      "keyInsights": [
        "<A critical insight derived from their answer.>",
        "<Another important observation or red flag.>"
      ],
      "score": <A float score from 0.0 to 10.0 for this specific interview aspect. Use the scale: 0=Terrible, 5=Average, 10=Exceptional.>,
      "person": "<The name of the founder who was asked or whose response is being highlighted.>"
    }}
  ]
}}

**INSTRUCTIONS:**
- Adhere strictly to the scoring rubrics provided for each metric.
- Be objective and data-driven. Reference specific details from the context.
- The `overallScore` should be a holistic assessment.
- The `founderHighlights` must be derived directly from the `RESEARCH_DATA`.
- The `interviewHighlights` must be derived directly from the `INTERVIEW_ANALYSIS`.
- Ensure all floating-point numbers have one decimal place.
"""


class ConsolidatorAgent(BaseOpenRouterAgent):
    """
    An agent that synthesizes research and interview data into a final
    investment report for the front end.
    """
    def __init__(self, openrouter_api_key: str):
        # Using a powerful model for this complex synthesis task
        super().__init__(api_key=openrouter_api_key, model="x-ai/grok-4-fast:free")

    def synthesize_report(self, research_data: Dict[str, Any], interview_analysis: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generates the final analysis report by synthesizing all available data.

        Args:
            research_data: The output from the initial research orchestrator.
            interview_analysis: The output from the interview analysis process.

        Returns:
            A dictionary containing the final, consolidated report.
        """
        print("Agent [Consolidator]: Starting final synthesis...")

        # Convert the input dictionaries to formatted JSON strings for the prompt
        research_data_str = json.dumps(research_data, indent=2)
        interview_analysis_str = json.dumps(interview_analysis, indent=2)

        # Populate the master prompt with the context
        prompt = FINAL_ANALYSIS_PROMPT.format(
            research_data=research_data_str,
            interview_analysis=interview_analysis_str
        )

        messages = [
            {"role": "system", "content": "You are a VC investment partner creating a final JSON report according to a strict schema and rubric."},
            {"role": "user", "content": prompt}
        ]

        # Send the request to the LLM and get the structured JSON output
        final_report = self._send_llm_request(messages)

        if "error" in final_report:
            print(f"Agent [Consolidator]: Failed to generate report. Error: {final_report['error']}")
            return final_report
        
        print("Agent [Consolidator]: Synthesis complete.")
        return final_report

# ==============================================================================
# Test Block for Standalone Execution
# ==============================================================================
if __name__ == '__main__':
    print("--- Running Consolidator Agent Standalone Test (with Enhanced Rubric) ---")
    
    # Load API keys from .env file
    # Make sure you have a .env file in your project root with API_KEY="your_openrouter_key"
    dotenv_path = os.path.join(os.path.dirname(__file__), '..', '..', '.env')
    load_dotenv(dotenv_path=dotenv_path)
    
    openrouter_api_key = os.getenv("API_KEY")

    if not openrouter_api_key:
        raise ValueError("API_KEY must be set in your .env file to run the test.")

    # --- 1. Define Mock Input Data ---
    # This simulates the data that would be passed to the agent in your workflow

    # MOCK RESEARCH DATA (from FounderAnalysisOrchestrator)
    mock_research_data = {
        "id": "2",
        "data": {
            "startupInfo": {"name": "DeepResearch AI"},
            "teamList": [
                {
                    "id": "1",
                    "name": "Sarah Chen",
                    "linkedin": "https://www.linkedin.com/in/sarahchen-ai",
                    "university": "Stanford University",
                    "analysis": {
                        "linkedin_analysis": {
                            "name": "Sarah Chen",
                            "experience_summary": "AI Researcher at Google Brain",
                            "highest_education": "PhD in Computer Science, Stanford University",
                            "top_skills": ["Machine Learning", "Natural Language Processing", "Python"]
                        },
                        "openalex_analysis": {
                           "author_metrics": {"h_index": 15, "cited_by_count": 2500}
                        }
                    }
                },
                {
                    "id": "2",
                    "name": "Marcus Rodriguez",
                    "github": "https://github.com/marcus-rodriguez",
                    "university": "MIT",
                     "analysis": {
                        "github_analysis": {
                           "key_languages": ["TypeScript", "Python"],
                           "notable_repositories": ["vision-stream-processor"],
                           "technical_focus": "Real-time data processing and cloud infrastructure"
                        }
                    }
                }
            ]
        }
    }

    # MOCK INTERVIEW ANALYSIS (from interview analysis process)
    mock_interview_analysis = {
        "overall_compatibility_score": 88,
        "executive_summary": "The founders show strong alignment on vision and possess highly complementary skills. Communication is direct and effective. A key challenge will be navigating market entry speed.",
        "detailed_scores": {
            "vision_alignment": {"score": 92, "analysis": "Both founders clearly articulated the same long-term vision for the company."},
            "complementary_skills": {"score": 95, "analysis": "Sarah's deep AI research background perfectly complements Marcus's expertise in scalable cloud engineering."},
            "communication_style": {"score": 85, "analysis": "They exhibit a respectful and efficient communication style, even when discussing disagreements."}
        },
        "strengths": ["Strong technical foundation", "Shared product vision", "Clear division of roles"],
        "challenges": ["Limited go-to-market experience", "Potential for over-engineering solutions"]
    }

    # --- 2. Instantiate and Run the Agent ---
    agent = ConsolidatorAgent(openrouter_api_key=openrouter_api_key)
    
    final_analysis_report = agent.synthesize_report(
        research_data=mock_research_data,
        interview_analysis=mock_interview_analysis
    )

    # --- 3. Print the Final Result ---
    print("\n--- FINAL CONSOLIDATED REPORT ---")
    print(json.dumps(final_analysis_report, indent=2))
    print("--- End of Test ---")