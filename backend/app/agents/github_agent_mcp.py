import os
from typing import List, Optional
from pydantic import BaseModel, Field
from pydantic_ai import Agent
from pydantic_ai.mcp import MCPServerStdio
from dotenv import load_dotenv

load_dotenv()

class GitHubProfile(BaseModel):
    """Schema for author metrics from Github."""
    list_projects: List[str] = Field(..., description="List of GitHub repositories owned by the author.")
    total_stars: int = Field(..., description="Total number of stars across all repositories.")
    total_followers: int = Field(..., description="Total number of followers on GitHub  profile.")
    total_contributions: int = Field(..., description="Total number of contributions in the last year.")
    top_languages: List[str] = Field(..., description="List of top programming languages used in the repositories.")

def create_github_agent() -> Agent:
    """Create an agent for interacting with GitHub."""
    github_server = MCPServerStdio(
            command="uv",
            args=[
                "run", "python3",
                "simple-github-mcp-server/simple_github_mcp_server.py"
            ],
            env={"GITHUB_PERSONAL_ACCESS_TOKEN": os.getenv("GITHUB_PERSONAL_ACCESS_TOKEN")},
            timeout=30
        )

    # Load the system prompt
    with open("backend/app/core/prompts/github_system.txt", "r") as prompt_file:
        system_prompt = prompt_file.read()

    agent = Agent(
        model="anthropic:claude-3-7-sonnet-latest",
        output_type=GitHubProfile,
        system_prompt=system_prompt,
        toolsets=[github_server],
    )
    return agent

async def fetch_githuib_info(agent: Agent, github_repo_url: Optional[str] = None):
    """Fetch author metrics using the OpenAlex agent."""
    with open("backend/app/core/prompts/github_search.txt", "r") as prompt_file:
        prompt_template = prompt_file.read()

    prompt = prompt_template.format(
        github_repo_url=github_repo_url if github_repo_url else "any"
    )

    agent_response = await agent.run(prompt)
    return agent_response.output

# if __name__ == "__main__":
    # Example usage
agent = create_github_agent()


# Test with a well-known researcher
github_url = "https://github.com/OmranKaddah"
async def run(agent, github_url):
    response = await fetch_githuib_info(agent, github_url)
    return response

import asyncio
response = asyncio.run(run(agent, github_url))