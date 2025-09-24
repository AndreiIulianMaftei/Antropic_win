# src/agents/synthesis/showcase_reporting_agent.py
import os
import sys
import json
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from src.core.base_agent import BaseAgent

class ShowcaseReportingAgent(BaseAgent):
    """
    Synthesizes the entire team analysis into a final, UI-friendly JSON report.
    """
    def create_report(self, full_analysis_data: dict) -> dict:
        """
        Transforms the detailed analysis data into the final showcase JSON.
        """
        print("Agent [Showcase]: Creating final UI showcase report...")
        
        data_str = json.dumps(full_analysis_data, indent=2)

        target_json_structure = {
          "team_overall_grade": "B+",
          "executive_summary": "A strong technical founder paired with an experienced operator creates a well-balanced team. While there's a slight gap in early-stage sales, their combined expertise presents a high potential for success.",
          "key_risks": [
            "First-time founder status for the business lead.",
            "No dedicated sales or marketing experience on the founding team."
          ],
          "founder_highlights": [
            {
              "name": "Jane Doe",
              "highlight": "Exceptional academic record (H-Index: 25) and a highly-starred GitHub profile indicate top-tier technical talent.",
              "score": "strong"
            },
            {
              "name": "John Smith",
              "highlight": "Proven operator with experience in senior leadership roles at established tech companies.",
              "score": "average"
            }
          ]
        }
        
        prompt = f"""
        You are a VC analyst responsible for creating the final summary for an investment memo. Distill the comprehensive analysis data below into a concise, high-level JSON report.

        --- COMPREHENSIVE ANALYSIS DATA ---
        {data_str}
        --- END DATA ---

        Your task is to populate the following JSON structure.
        - `team_overall_grade`: Use the grade from the synergy analysis.
        - `executive_summary`: Write a 1-2 sentence summary of the team's core dynamic.
        - `key_risks`: Extract the most critical gaps from the synergy analysis.
        - `founder_highlights`: For each founder, write a one-sentence highlight and assign a 'strong', 'average', or 'weak' score based on their assessment.

        Strictly adhere to this JSON structure:
        {json.dumps(target_json_structure, indent=2)}
        """
        
        messages = [
            {"role": "system", "content": "You are a VC analyst synthesizing a final team report for an investment committee."},
            {"role": "user", "content": prompt}
        ]
        
        return self._send_llm_request(messages)