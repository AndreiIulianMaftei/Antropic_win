import os
from typing import List, Optional
from pydantic import BaseModel, Field
from pydantic_ai import Agent
from pydantic_ai.mcp import MCPServerStdio
from dotenv import load_dotenv

load_dotenv()

class AuthorMetrics(BaseModel):
    """Schema for author metrics from OpenAlex."""
    display_name: str = Field(..., description="Author's display name")
    works_count: int = Field(..., description="Number of works by the author")
    cited_by_count: int = Field(..., description="Number of citations")
    h_index: Optional[int] = Field(None, description="H-index of the author")
    i10_index: Optional[int] = Field(None, description="i10-index of the author")
    last_known_institution: Optional[str] = Field(None, description="Last known institution of the author")
    orcid: Optional[str] = Field(None, description="Author's ORCID identifier")

def create_openalex_agent() -> Agent:
    """Create an agent for interacting with OpenAlex."""
    openalex_server = MCPServerStdio(
        "uvx",
        args=[
            "--from", "git+https://github.com/drAbreu/alex-mcp.git@4.1.0",
            "alex-mcp"        
        ],
        env={"OPENALEX_MAILTO": os.getenv("OPENALEX_MAILTO")},
        timeout=60
    )

    # Load the system prompt
    with open("backend/app/core/prompts/openalex_system.txt", "r") as prompt_file:
        system_prompt = prompt_file.read()

    agent = Agent(
        model="gemini-2.0-flash",
        output_type=AuthorMetrics,
        system_prompt=system_prompt,
        toolsets=[openalex_server],
    )
    return agent

async def fetch_author_metrics(agent: Agent, author_name: str, affiliation: Optional[str] = None):
    """Fetch author metrics using the OpenAlex agent."""
    with open("backend/app/core/prompts/openalex_search.txt", "r") as prompt_file:
        prompt_template = prompt_file.read()

    prompt = prompt_template.format(
        author_name=author_name,
        affiliation=affiliation if affiliation else "any"
    )

    agent_response = await agent.run(prompt)
    return agent_response.output

if __name__ == "__main__":
    # Example usage
    agent = create_openalex_agent()

    # Test with a well-known researcher
    author_name = "Yann LeCun"
    affiliation = "Meta AI"
    async def run(agent, author_name, affiliation):
        response = await fetch_author_metrics(agent, author_name, affiliation)
        return response

    import asyncio
    response = asyncio.run(run(agent, author_name, affiliation))