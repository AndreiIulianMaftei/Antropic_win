import asyncio
import os
from typing import List

from dotenv import load_dotenv
from pydantic import BaseModel, Field

from pydantic_ai import Agent
from pydantic_ai.mcp import MCPServerStdio

load_dotenv()

# Define the output schema for AI responses
class AnalysisReport(BaseModel):
    startup_name: str = Field(..., description="Name of the startup")
    disruption_probability: float = Field(..., description="Probability that the startup will make a disruption on a scale from 0 to 1")
    founders_synergy: float = Field(..., description="founders synergy score on a scale from 0 to 10")
    complementary_score: float = Field(..., description="Complementary score on a scale from 0 to 10 how well the startup founders complement each other")
    founder_highlights: List[str] = Field(..., description="List of key highlights about the founders")

def create_analysis_agent() -> Agent:
    """Create an agent for generating analysis reports."""
    # Load the system prompt from the new prompts directory
    with open("backend/app/core/prompts/analysis_report_system.txt", "r") as prompt_file:
        system_prompt = prompt_file.read()

    agent = Agent(
        model="anthropic:claude-4-sonnet-20250514",
        output_type=AnalysisReport,
        system_prompt=system_prompt,
    )
    return agent

async def run_analysis_agent(agent: Agent, teams_data: str):
    """Ask the agent to call the appropriate LinkedIn tool to fetch a profile for a URL."""

    with open("backend/app/core/prompts/analysis_report_search.txt", "r") as prompt_file:
        prompt = prompt_file.read()
    agent_response = await agent.run(prompt+ teams_data)
    return agent_response.output