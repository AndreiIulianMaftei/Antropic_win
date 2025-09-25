import asyncio
import os
import pytest
from dotenv import load_dotenv
from backend.app.agents.linkedin_agent import create_linkedin_agent, fetch_profile_via_agent

# Load environment variables from .env file
load_dotenv()

@pytest.mark.asyncio
async def test_linkedin_agent():
    """Test the LinkedIn agent by simulating a profile fetch."""
    agent = create_linkedin_agent()
    url = "https://www.linkedin.com/in/omran-kadah-41b784b3/"
    response = await fetch_profile_via_agent(agent, url)

    assert response is not None, "The agent did not return a response."
    print("Test passed: Response received.")