"""
Eleven Labs Transcript Saver
Takes agent IDs and saves transcripts of their last conversations
"""

import os
import json
import requests
from datetime import datetime
from typing import Optional, Dict, Any, List
from dotenv import load_dotenv

load_dotenv()


class ElevenLabsTranscriptSaver:
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv('ELEVENLABS_API_KEY')
        if not self.api_key:
            raise ValueError("ELEVENLABS_API_KEY required")
        self.base_url = "https://api.elevenlabs.io"
    
    def get_last_conversation_transcript(self, agent_id: str) -> Optional[Dict[str, Any]]:
        """Get the transcript of the last conversation for an agent"""
        # Get conversations for agent
        response = requests.get(
            f"{self.base_url}/v1/convai/conversations",
            headers={"xi-api-key": self.api_key},
            params={"agent_id": agent_id, "page_size": 1}
        )
        
        if response.status_code != 200:
            raise Exception(f"Failed to get conversations: {response.status_code}")
        
        conversations = response.json().get("conversations", [])
        if not conversations:
            return None
        
        # Get full transcript for the most recent conversation
        conversation_id = conversations[0]["conversation_id"]
        response = requests.get(
            f"{self.base_url}/v1/convai/conversations/{conversation_id}",
            headers={"xi-api-key": self.api_key}
        )
        
        if response.status_code != 200:
            raise Exception(f"Failed to get transcript: {response.status_code}")
        
        return response.json()
    
    def save_transcript(self, transcript_data: Dict[str, Any]) -> str:
        """Save transcript to JSON file"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        conversation_id = transcript_data.get("conversation_id", "unknown")
        filename = f"transcript_{conversation_id}_{timestamp}.json"
        
        os.makedirs("transcripts", exist_ok=True)
        filepath = os.path.join("transcripts", filename)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(transcript_data, f, indent=2, ensure_ascii=False)
        
        return filepath


def save_agent_transcripts(agent_ids: list) -> Dict[str, Any]:
    """Save transcripts for multiple agents"""
    saver = ElevenLabsTranscriptSaver()
    results = {}
    
    for agent_id in agent_ids:
        try:
            print(f"Processing agent: {agent_id}")
            transcript_data = saver.get_last_conversation_transcript(agent_id)
            
            if not transcript_data:
                results[agent_id] = {"error": "No conversations found"}
                continue
            
            filepath = saver.save_transcript(transcript_data)
            results[agent_id] = {
                "file": filepath,
                "conversation_id": transcript_data.get("conversation_id")
            }
            print(f"✅ Saved: {filepath}")
            
        except Exception as e:
            results[agent_id] = {"error": str(e)}
            print(f"❌ Error with {agent_id}: {e}")
    
    return results


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python eleven_labs_transcript.py <agent_id1> [agent_id2] ...")
        sys.exit(1)
    
    agent_ids = sys.argv[1:]
    print(f"Getting transcripts for {len(agent_ids)} agent(s)")
    
    try:
        results = save_agent_transcripts(agent_ids)
        
        successful = sum(1 for r in results.values() if "file" in r)
        print(f"\n✅ Success: {successful}/{len(agent_ids)} agents")
        
    except Exception as e:
        print(f"❌ Error: {e}")


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python eleven_labs_transcript.py <agent_id1> [agent_id2] ...")
        sys.exit(1)
    
    agent_ids = sys.argv[1:]
    print(f"Getting transcripts for {len(agent_ids)} agent(s)")
    
    try:
        results = save_agent_transcripts(agent_ids)
        
        successful = sum(1 for r in results.values() if "file" in r)
        print(f"\n✅ Success: {successful}/{len(agent_ids)} agents")
        
    except Exception as e:
        print(f"❌ Error: {e}")
