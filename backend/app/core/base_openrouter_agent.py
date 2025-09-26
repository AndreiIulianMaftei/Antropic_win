# /Complete workflow/core/base_openrouter_agent.py
import json
from openai import OpenAI

class BaseOpenRouterAgent:
    """A base class for Agents that use the OpenRouter API."""
    def __init__(self, api_key: str, model: str = "anthropic/claude-3.7-sonnet"):
        if not api_key:
            raise ValueError("OpenRouter API key (API_KEY) is not set.")
        
        self.client = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=api_key,
        )
        self.model = model
        self.extra_headers = {
            "HTTP-Referer": "https://unicorn-radar.app", 
            "X-Title": "Unicorn Radar Founder Analysis",
        }

    def _send_llm_request(self, messages: list[dict]) -> dict:
        """Sends a request to the LLM and returns a parsed JSON object or an error dict."""
        response_content = None
        try:
            completion = self.client.chat.completions.create(
                extra_headers=self.extra_headers,
                model=self.model,
                messages=messages,
                response_format={"type": "json_object"}
            )
            response_content = completion.choices[0].message.content
            if not response_content:
                return {"error": "LLM returned empty content."}
            return json.loads(response_content)
        # --- START: IMPROVED ERROR HANDLING ---
        except json.JSONDecodeError:
            error_msg = f"Failed to decode LLM JSON. Raw response: '{response_content}'"
            print(f"ERROR: {error_msg}")
            return {"error": error_msg}
        except Exception as e:
            error_msg = f"An API error occurred with OpenRouter: {e}"
            print(f"ERROR: {error_msg}")
            return {"error": error_msg}
        # --- END: IMPROVED ERROR HANDLING ---