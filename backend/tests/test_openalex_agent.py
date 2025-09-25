import asyncio
import os
import pytest
from dotenv import load_dotenv
from backend.app.agents.openalex_agent import create_openalex_agent, fetch_author_metrics

# Load environment variables from .env file
load_dotenv()

@pytest.mark.asyncio
async def test_openalex_agent():
    """Test the OpenAlex agent by fetching metrics for a known author."""
    agent = create_openalex_agent()
    
    # Test with a well-known researcher
    author_name = "Yann LeCun"
    affiliation = "Meta AI"
    
    response = await fetch_author_metrics(agent, author_name, affiliation)
    
    assert response is not None, "The agent did not return a response"
    assert response.display_name is not None, "Display name should not be None"
    assert response.works_count > 0, "Works count should be greater than 0"
    assert response.cited_by_count > 0, "Cited by count should be greater than 0"
    
    print(f"Test passed: Retrieved metrics for {response.display_name}")
    print(f"Works count: {response.works_count}")
    print(f"Citations: {response.cited_by_count}")
    print(f"h-index: {response.h_index}")
    print(f"Institution: {response.last_known_institution}")