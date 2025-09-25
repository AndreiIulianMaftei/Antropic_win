import argparse
import json
import os
from datetime import datetime
from typing import Dict, Any, Optional

import requests
import google.generativeai as genai
from dotenv import load_dotenv

API_URL = "https://api.bey.dev/v1"


def create_compatibility_analysis_prompt(transcript1: Dict, transcript2: Dict) -> str:
    """
    Create a streamlined prompt for founder compatibility analysis using Gemini.
    """
    return f"""
You are an expert startup advisor analyzing the compatibility between two potential co-founders. 

FOUNDER 1 CONVERSATION TRANSCRIPT:
{json.dumps(transcript1, indent=2)}

FOUNDER 2 CONVERSATION TRANSCRIPT:
{json.dumps(transcript2, indent=2)}

Analyze their compatibility and return ONLY valid JSON (no markdown formatting, no extra text):

{{
    "overall_compatibility_score": <integer 1-100>,
    "detailed_scores": {{
        "vision_alignment": {{"score": <integer 1-100>, "analysis": "<brief explanation>"}},
        "complementary_skills": {{"score": <integer 1-100>, "analysis": "<brief explanation>"}},
        "communication_style": {{"score": <integer 1-100>, "analysis": "<brief explanation>"}},
        "work_style_compatibility": {{"score": <integer 1-100>, "analysis": "<brief explanation>"}},
        "leadership_dynamics": {{"score": <integer 1-100>, "analysis": "<brief explanation>"}}
    }},
    "strengths": ["<strength 1>", "<strength 2>", "<strength 3>"],
    "challenges": ["<challenge 1>", "<challenge 2>", "<challenge 3>"],
    "recommendations": {{
        "partnership_viability": "<HIGH|MEDIUM|LOW>",
        "key_actions": ["<action 1>", "<action 2>", "<action 3>"],
        "red_flags": ["<red flag 1>", "<red flag 2>"]
    }},
    "executive_summary": "<2-3 sentence summary of compatibility and recommendation>"
}}

Focus on startup founder dynamics. Score 1-100 where 100 is perfect compatibility. Be objective and evidence-based.
"""


def analyze_founder_compatibility(transcript1: Dict, transcript2: Dict, google_api_key: str) -> Dict[str, Any]:
    """
    Analyze compatibility between two founders using Google Gemini API.
    
    Args:
        transcript1: First founder's transcript data
        transcript2: Second founder's transcript data  
        google_api_key: Google API key for Gemini
        
    Returns:
        Dictionary containing compatibility analysis results
    """
    try:
        # Configure Gemini API
        genai.configure(api_key=google_api_key)
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        # Create analysis prompt
        prompt = create_compatibility_analysis_prompt(transcript1, transcript2)
        
        print("Analyzing founder compatibility with Google Gemini...")
        
        # Generate response with optimized config for JSON output
        generation_config = {
            "max_output_tokens": 4000,  # Sufficient for streamlined response
            "temperature": 0.1,         # Low temperature for consistent JSON
        }
        response = model.generate_content(prompt, generation_config=generation_config)
        
        # Clean the response text to extract JSON (remove code blocks if present)
        response_text = response.text.strip()
        if response_text.startswith('```json'):
            response_text = response_text[7:]  # Remove ```json
        if response_text.endswith('```'):
            response_text = response_text[:-3]  # Remove ```
        response_text = response_text.strip()
        
        # Parse JSON response
        analysis_result = json.loads(response_text)
        
        # Add metadata
        analysis_result["metadata"] = {
            "model_used": "gemini-1.5-flash",
            "analysis_timestamp": datetime.now().isoformat(),
            "founder1_id": transcript1.get("actor", "unknown"),
            "founder2_id": transcript2.get("actor", "unknown")
        }
        
        return {
            "success": True,
            "compatibility_analysis": analysis_result
        }
        
    except json.JSONDecodeError as e:
        return {
            "success": False,
            "error": "json_decode_error",
            "message": f"Failed to parse Gemini response as JSON: {str(e)}",
            "raw_response": response_text if 'response_text' in locals() else (response.text if 'response' in locals() else None)
        }
    except Exception as e:
        return {
            "success": False,
            "error": "analysis_error", 
            "message": f"Error during compatibility analysis: {str(e)}"
        }


def get_last_call_for_agent(api_key: str, agent_id: str, actor_name: str) -> Optional[Dict[str, Any]]:
    """
    Get the last call data for a specific agent.
    
    Returns:
        Dictionary with call data if successful, None if error
    """
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
        return None

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
        return None

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
        return None

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
    
    return result


def main() -> None:
    load_dotenv()
    
    # Load API keys from environment
    bey_api_key = os.getenv("BEY_API_KEY")
    google_api_key = os.getenv("GOOGLE_API_KEY")
    
    if bey_api_key is None:
        raise ValueError("Please set the BEY_API_KEY environment variable in .env")
    
    if google_api_key is None:
        raise ValueError("Please set the GOOGLE_API_KEY environment variable in .env")

    # Define the two agents with their IDs
    agents = [
        {
            "agent_id": "96a7d634-d54c-4804-9a66-a9b9b639f77a",  # Replace with actual agent 1 ID
            "actor_name": "Founder 1"
        },
        {
            "agent_id": "e2851df0-b25a-4b68-9a73-d619533e4d09",  # Replace with actual agent 2 ID
            "actor_name": "Founder 2"
        }
    ]
    
    print("="*80)
    print("STARTUP FOUNDER COMPATIBILITY ANALYSIS")
    print("="*80)
    print("Fetching transcripts for both founders...")
    
    # Collect transcripts from both agents
    transcripts = []
    
    for agent in agents:
        print(f"\nProcessing {agent['actor_name']}...")
        result = get_last_call_for_agent(
            api_key=bey_api_key,
            agent_id=agent["agent_id"],
            actor_name=agent["actor_name"]
        )
        
        if result and result.get("success"):
            transcripts.append(result)
        else:
            print(f"Failed to get transcript for {agent['actor_name']}")
    
    # Check if we have both transcripts
    if len(transcripts) != 2:
        print(f"\nError: Need exactly 2 transcripts, got {len(transcripts)}")
        print("Cannot perform compatibility analysis without both founder transcripts.")
        return
    
    print(f"\n{'='*80}")
    print("ANALYZING FOUNDER COMPATIBILITY WITH GOOGLE GEMINI")
    print("="*80)
    
    # Perform compatibility analysis using Google Gemini
    compatibility_result = analyze_founder_compatibility(
        transcript1=transcripts[0],
        transcript2=transcripts[1], 
        google_api_key=google_api_key
    )
    
    if compatibility_result.get("success"):
        analysis = compatibility_result["compatibility_analysis"]
        
        # Display results in a formatted way
        print(f"\n🎯 OVERALL COMPATIBILITY SCORE: {analysis.get('overall_compatibility_score', 'N/A')}/100")
        print(f"🤝 PARTNERSHIP VIABILITY: {analysis.get('recommendations', {}).get('partnership_viability', 'N/A')}")
        
        print(f"\n📋 EXECUTIVE SUMMARY:")
        print(f"{analysis.get('executive_summary', 'N/A')}")
        
        # Detailed scores
        detailed_scores = analysis.get('detailed_scores', {})
        if detailed_scores:
            print(f"\n📊 DETAILED COMPATIBILITY SCORES:")
            print("-" * 50)
            for dimension, data in detailed_scores.items():
                score = data.get('score', 'N/A')
                print(f"• {dimension.replace('_', ' ').title()}: {score}/100")
        
        # Synergy analysis
        strengths = analysis.get('strengths', [])
        challenges = analysis.get('challenges', [])
        if strengths or challenges:
            print(f"\n⚡ SYNERGY ANALYSIS:")
            print("-" * 50)
            
            if strengths:
                print("💪 Potential Strengths:")
                for strength in strengths[:3]:  # Show top 3
                    print(f"  • {strength}")
            
            if challenges:
                print("\n⚠️ Potential Challenges:")
                for challenge in challenges[:3]:  # Show top 3
                    print(f"  • {challenge}")
        
        # Recommendations
        recommendations = analysis.get('recommendations', {})
        if recommendations:
            print(f"\n🎯 RECOMMENDATIONS:")
            print("-" * 50)
            
            actions = recommendations.get('key_actions', [])
            if actions:
                print("📝 Key Actions:")
                for action in actions[:3]:  # Show top 3
                    print(f"  • {action}")
            
            red_flags = recommendations.get('red_flags', [])
            if red_flags:
                print("\n🚩 Red Flags:")
                for flag in red_flags:
                    print(f"  • {flag}")
        
        # Save full analysis results
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        analysis_filename = f"founder_compatibility_analysis_{timestamp}.json"
        
        with open(analysis_filename, 'w', encoding='utf-8') as f:
            json.dump(compatibility_result, f, indent=2, ensure_ascii=False)
        
        print(f"\n💾 Full analysis saved to: {analysis_filename}")
        print(f"\n{'='*80}")
        print("COMPATIBILITY ANALYSIS COMPLETED")
        print("="*80)
        
    else:
        print(f"\n❌ Compatibility analysis failed:")
        print(f"Error: {compatibility_result.get('message', 'Unknown error')}")
        if compatibility_result.get('raw_response'):
            print(f"Raw response: {compatibility_result['raw_response'][:500]}...")


if __name__ == "__main__":
    main()
