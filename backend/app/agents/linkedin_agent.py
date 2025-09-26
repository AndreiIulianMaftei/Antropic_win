import asyncio
import os
from typing import List

from dotenv import load_dotenv
from pydantic import BaseModel, Field

from pydantic_ai import Agent
from pydantic_ai.mcp import MCPServerStdio

load_dotenv()

# Define the output schema for AI responses
class ProfileSummary(BaseModel):
    name: str = Field(..., description="Full name of the individual")
    experience_summary: str = Field(..., description="Professional headline")
    highest_education: str = Field(..., description="Highest education level")
    top_skills: List[str] = Field(..., description="List of top skills")
    notable_positions: List[str] = Field(..., description="List of notable positions held")

def create_linkedin_agent() -> Agent:
    linkedin_cookie = os.getenv("LINKEDIN_COOKIE")
    if not linkedin_cookie:
        raise ValueError("LINKEDIN_COOKIE environment variable is not set.")

    linkedIn_server = MCPServerStdio( 
        "docker",
        args=[
            "run", "--rm", "-i",
            "-e", "LINKEDIN_COOKIE",
            "stickerdaniel/linkedin-mcp-server:latest"
        ],
        env={"LINKEDIN_COOKIE": linkedin_cookie},
        timeout=60
    )

    # Load the system prompt from the new prompts directory
    with open("backend/app/core/prompts/linkedIn_system.txt", "r") as prompt_file:
        system_prompt = prompt_file.read()

    agent = Agent(
        model="anthropic:claude-3-7-sonnet-latest",
        output_type=ProfileSummary,
        system_prompt=system_prompt,
        toolsets=[linkedIn_server],
    )
    return agent

async def fetch_profile_via_agent(agent: Agent, url: str):
    """Ask the agent to call the appropriate LinkedIn tool to fetch a profile for a URL."""
    print(f"Fetching LinkedIn profile for URL: {url}")
    with open("backend/app/core/prompts/linkedIn_run.txt", "r") as prompt_file:
        prompt = prompt_file.read()
    # prompt.format({"url": url})
    agent_response = await agent.run(prompt + url)
    return agent_response.output