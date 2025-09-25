"""
Clean Eleven Labs Agent Creator
Takes text file, creates agent, returns web link and agent ID
"""

import os
import sys
import requests
from typing import Optional, Dict
from dotenv import load_dotenv

load_dotenv()


class ElevenLabsAgentCreator:
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv('ELEVENLABS_API_KEY')
        if not self.api_key:
            raise ValueError("ELEVENLABS_API_KEY required")
        self.base_url = "https://api.elevenlabs.io"
    
    def create_agent(self, instructions: str, name: str = "Agent") -> Dict[str, str]:
        """Create agent and return both web link and agent ID"""
        payload = {
            "conversation_config": {
                "agent": {
                    "prompt": {
                        "prompt": instructions
                    }
                }
            },
            "name": name
        }
        
        response = requests.post(
            f"{self.base_url}/v1/convai/agents/create",
            headers={
                "xi-api-key": self.api_key,
                "Content-Type": "application/json"
            },
            json=payload
        )
        
        if response.status_code != 200:
            raise Exception(f"API error: {response.status_code} - {response.text}")
        
        agent_id = response.json()["agent_id"]
        web_link = f"https://elevenlabs.io/app/talk-to?agent_id={agent_id}"
        
        return {
            "web_link": web_link,
            "agent_id": agent_id
        }
    
    def save_agent_id_to_file(self, agent_id: str, filename: str = "agent_ids.txt") -> str:
        """Save agent ID to text file"""
        from datetime import datetime
        
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        entry = f"{timestamp} - {agent_id}\n"
        
        with open(filename, 'a', encoding='utf-8') as f:
            f.write(entry)
        
        return filename
    
    def delete_all_conversations(self) -> Dict[str, int]:
        """Delete all conversations and return summary"""
        # Get all conversations
        conversations = self._get_all_conversations()
        total = len(conversations)
        deleted = 0
        
        print(f"Found {total} conversations to delete...")
        
        for conv in conversations:
            conversation_id = conv.get("conversation_id")
            if conversation_id and self._delete_conversation(conversation_id):
                deleted += 1
                print(f"✅ Deleted {conversation_id}")
        
        return {"total": total, "deleted": deleted}
    
    def _get_all_conversations(self) -> list:
        """Get all conversations with pagination"""
        all_conversations = []
        cursor = None
        
        while True:
            params = {"page_size": 100}
            if cursor:
                params["cursor"] = cursor
            
            response = requests.get(
                f"{self.base_url}/v1/convai/conversations",
                headers={"xi-api-key": self.api_key},
                params=params
            )
            
            if response.status_code != 200:
                break
            
            data = response.json()
            all_conversations.extend(data.get("conversations", []))
            
            if not data.get("has_more", False):
                break
            cursor = data.get("next_cursor")
        
        return all_conversations
    
    def _delete_conversation(self, conversation_id: str) -> bool:
        """Delete a specific conversation"""
        response = requests.delete(
            f"{self.base_url}/v1/convai/conversations/{conversation_id}",
            headers={"xi-api-key": self.api_key}
        )
        return response.status_code == 200


def main(txt_file_path: str) -> Dict[str, str]:
    """
    Main function: takes text file, creates agent, returns link and ID
    
    Args:
        txt_file_path: Path to text file with agent instructions
        
    Returns:
        Dictionary with web_link and agent_id
    """
    try:
        # Read instructions from file
        with open(txt_file_path, 'r', encoding='utf-8') as f:
            instructions = f.read().strip()
        
        creator = ElevenLabsAgentCreator()
        
        # Clean up old conversations
        print("🗑️ Cleaning up conversations...")
        delete_result = creator.delete_all_conversations()
        print(f"✅ Deleted {delete_result['deleted']}/{delete_result['total']} conversations\n")
        
        # Create new agent
        print(f"📖 Creating agent from: {txt_file_path}")
        result = creator.create_agent(instructions, "Custom Agent")
        
        # Save agent ID to file
        id_file = creator.save_agent_id_to_file(result['agent_id'])
        
        print(f"✅ Agent created!")
        print(f"🌐 Link: {result['web_link']}")
        print(f"🆔 ID: {result['agent_id']}")
        print(f"💾 ID saved to: {id_file}")
        
        return result
        
    except Exception as e:
        print(f"❌ Error: {e}")
        raise


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python elevenlabs_create_agent.py <text_file>")
        print("Example: python elevenlabs_create_agent.py instructions.txt")
        sys.exit(1)
    
    result = main(sys.argv[1])

    print(f"\n📋 Result: {result}")