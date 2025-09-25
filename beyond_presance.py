import argparse
import json
import os
from datetime import datetime

import requests
from dotenv import load_dotenv

API_URL = "https://api.bey.dev/v1"


def get_last_call_for_agent(api_key: str, agent_id: str, actor_name: str) -> None:
    calls_response = requests.get(
        f"{API_URL}/calls",
        headers={"x-api-key": api_key},
    )

    if calls_response.status_code != 200:
        error_result = {
            "error": True,
            "status_code": calls_response.status_code,
            "message": f"Error fetching calls: {calls_response.status_code} - {calls_response.text}",
            "actor": actor_name
        }
        print(f"\n=== {actor_name} ===")
        print(json.dumps(error_result, indent=2))
        return

    calls = calls_response.json()["data"]
    
    # Filter calls for the specific agent
    agent_calls = [call for call in calls if call["agent_id"] == agent_id]
    
    if not agent_calls:
        no_calls_result = {
            "error": True,
            "message": f"No calls found for agent {agent_id}",
            "agent_id": agent_id,
            "actor": actor_name
        }
        print(f"\n=== {actor_name} ===")
        print(json.dumps(no_calls_result, indent=2))
        return

    # Get the last call (most recent) by sorting by started_at timestamp
    last_call = max(agent_calls, key=lambda x: x["started_at"])
    
    call_id = last_call["id"]
    call_started_at = last_call["started_at"]
    call_ended_at = last_call["ended_at"]

    messages_response = requests.get(
        f"{API_URL}/calls/{call_id}/messages",
        headers={"x-api-key": api_key},
    )
    if messages_response.status_code != 200:
        error_result = {
            "error": True,
            "status_code": messages_response.status_code,
            "message": f"Error fetching messages for call {call_id}: {messages_response.status_code} - {messages_response.text}",
            "call_id": call_id,
            "actor": actor_name
        }
        print(f"\n=== {actor_name} ===")
        print(json.dumps(error_result, indent=2))
        return

    messages = messages_response.json()
    
    # Create the JSON result
    result = {
        "success": True,
        "actor": actor_name,
        "agent_id": agent_id,
        "last_call": {
            "call_id": call_id,
            "started_at": call_started_at,
            "ended_at": call_ended_at,
            "messages": messages
        }
    }
    
    # Save to file with actor name and timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{actor_name.lower().replace(' ', '_')}_last_call_{timestamp}.json"
    
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(result, f, indent=2, ensure_ascii=False)
    
    print(f"\n=== {actor_name} ===")
    print(json.dumps(result, indent=2))
    print(f"\nData saved to: {filename}")


def main() -> None:
    load_dotenv()
    if (api_key := os.getenv("BEY_API_KEY")) is None:
        raise ValueError("Please set the BEY_API_KEY environment variable in .env")

    # Define the two agents with their IDs
    agents = [
        {
            "agent_id": "96a7d634-d54c-4804-9a66-a9b9b639f77a",  # Replace with actual agent 1 ID
            "actor_name": "Actor 1"
        },
        {
            "agent_id": "e2851df0-b25a-4b68-9a73-d619533e4d09",  # Replace with actual agent 2 ID
            "actor_name": "Actor 2"
        }
    ]
    
    print("Fetching last calls for both actors...")
    
    # Process each agent
    for agent in agents:
        get_last_call_for_agent(
            api_key=api_key,
            agent_id=agent["agent_id"],
            actor_name=agent["actor_name"]
        )


if __name__ == "__main__":
    main()
