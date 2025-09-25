# src/agents/extraction/profile_parser_agent.py
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from src.core.base_agent import BaseAgent

class ProfileParserAgent(BaseAgent):
    """An LLM-powered agent that parses raw text from profiles into structured JSON."""

    def parse_profile(self, raw_text: str, profile_type: str) -> dict | None:
        """
        Parses raw text content into a structured format based on the profile type.

        Args:
            raw_text (str): The raw text scraped from a webpage.
            profile_type (str): The type of profile ('linkedin', 'github', 'gscholar').

        Returns:
            A dictionary with the parsed, structured data or None if parsing fails.
        """
        print(f"Agent [Parser]: Parsing raw text for a '{profile_type}' profile...")

        system_prompt = "You are an expert data extraction agent. Your task is to parse raw text scraped from a webpage and convert it into a structured JSON object. You must adhere strictly to the requested schema and use `null` for any fields you cannot find."
        
        user_prompt = self._get_prompt_for_type(raw_text, profile_type)
        if not user_prompt:
            print(f"Error: Unknown profile type '{profile_type}'")
            return None

        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]

        return self._send_llm_request(messages)

    def _get_prompt_for_type(self, raw_text: str, profile_type: str) -> str | None:
        """Returns the specific prompt and schema for a given profile type."""
        
        common_start = f"Based on the following raw text, extract the information into the specified JSON format.\\n\\n--- RAW TEXT ---\\n{raw_text[:15000]}\\n--- END TEXT ---"

        if profile_type == 'linkedin':
            return f"""
            {common_start}

            Your JSON output must follow this exact schema:
            {{
              "headline": "<The user's professional headline, e.g., 'Co-founder & CEO at Unicorn Radar'>",
              "summary": "<The user's 'About' section summary>",
              "experience": [
                {{
                  "role": "<Job Title>",
                  "company": "<Company Name>",
                  "duration": "<e.g., 'Jan 2022 - Present · 1 yr 9 mos'>"
                }}
              ],
              "education": [
                {{
                  "institution": "<Name of University or School>",
                  "degree": "<e.g., 'Master of Business Administration - MBA'>"
                }}
              ]
            }}
            """
        elif profile_type == 'github':
            return f"""
            {common_start}

            Your JSON output must follow this exact schema:
            {{
              "username": "<The user's GitHub username>",
              "bio": "<The user's bio>",
              "pinned_repositories": [
                {{
                  "name": "<Repository Name>",
                  "description": "<A brief description of the repo>",
                  "language": "<Primary programming language used>",
                  "stars": "<Number of stars as an integer>"
                }}
              ],
              "contribution_stats": {{
                "total_contributions_last_year": "<Total contributions in the last year as an integer>"
              }}
            }}
            """
        elif profile_type == 'gscholar':
            return f"""
            {common_start}

            Your JSON output must follow this exact schema:
            {{
              "name": "<The researcher's full name>",
              "affiliation": "<The researcher's listed affiliation>",
              "h_index": "<The h-index as an integer>",
              "total_citations": "<The total number of citations as an integer>",
              "top_publications": [
                {{
                  "title": "<Title of the publication>",
                  "authors": "<List of authors>",
                  "journal_year": "<Journal or conference and year, e.g., 'Nature, 2023'>",
                  "cited_by": "<Number of citations for this paper as an integer>"
                }}
              ]
            }}
            """
        return None