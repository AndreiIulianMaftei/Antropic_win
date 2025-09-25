import argparse
import json
import os
from datetime import datetime
from typing import Dict, Any, List, Optional
import glob

import google.generativeai as genai
from dotenv import load_dotenv


def create_group_analysis_prompt(transcripts: List[Dict]) -> str:
    """
    Create a comprehensive prompt for group analysis using Gemini.
    """
    transcript_data = ""
    for i, transcript in enumerate(transcripts, 1):
        transcript_data += f"\n\nPARTICIPANT {i} TRANSCRIPT:\n"
        transcript_data += f"Agent ID: {transcript.get('agent_id', 'unknown')}\n"
        transcript_data += f"Conversation ID: {transcript.get('conversation_id', 'unknown')}\n"
        transcript_data += json.dumps(transcript, indent=2)
        transcript_data += "\n" + "="*50

    return f"""
You are an expert group dynamics and organizational psychology analyst. Analyze the following group conversation transcripts and provide comprehensive insights.

GROUP CONVERSATION TRANSCRIPTS:
{transcript_data}

Analyze the group dynamics and return ONLY valid JSON (no markdown formatting, no extra text):

{{
    "group_analysis": {{
        "overall_group_cohesion_score": <integer 1-100>,
        "group_size": <integer>,
        "analysis_timestamp": "<ISO timestamp>",
        "group_dynamics": {{
            "communication_patterns": {{"score": <integer 1-100>, "analysis": "<detailed explanation>"}},
            "collaboration_effectiveness": {{"score": <integer 1-100>, "analysis": "<detailed explanation>"}},
            "leadership_emergence": {{"score": <integer 1-100>, "analysis": "<detailed explanation>"}},
            "conflict_resolution": {{"score": <integer 1-100>, "analysis": "<detailed explanation>"}},
            "decision_making_process": {{"score": <integer 1-100>, "analysis": "<detailed explanation>"}},
            "trust_and_psychological_safety": {{"score": <integer 1-100>, "analysis": "<detailed explanation>"}}
        }},
        "individual_profiles": [
            {{
                "participant_id": "<participant identifier>",
                "communication_style": "<description>",
                "leadership_traits": "<description>",
                "collaboration_approach": "<description>",
                "key_contributions": ["<contribution 1>", "<contribution 2>"],
                "potential_challenges": ["<challenge 1>", "<challenge 2>"]
            }}
        ],
        "group_strengths": ["<strength 1>", "<strength 2>", "<strength 3>", "<strength 4>"],
        "group_challenges": ["<challenge 1>", "<challenge 2>", "<challenge 3>", "<challenge 4>"],
        "interaction_patterns": {{
            "dominant_speakers": ["<participant id>"],
            "quiet_participants": ["<participant id>"],
            "collaboration_pairs": ["<participant 1> & <participant 2>"],
            "potential_conflicts": ["<description of potential conflict areas>"]
        }},
        "recommendations": {{
            "group_effectiveness": "<HIGH|MEDIUM|LOW>",
            "improvement_actions": ["<action 1>", "<action 2>", "<action 3>", "<action 4>"],
            "team_building_focus": ["<focus area 1>", "<focus area 2>"],
            "leadership_recommendations": ["<recommendation 1>", "<recommendation 2>"],
            "communication_improvements": ["<improvement 1>", "<improvement 2>"]
        }},
        "executive_summary": "<3-4 sentence comprehensive summary of group dynamics and recommendations>",
        "risk_assessment": {{
            "high_risk_areas": ["<risk 1>", "<risk 2>"],
            "medium_risk_areas": ["<risk 1>", "<risk 2>"],
            "mitigation_strategies": ["<strategy 1>", "<strategy 2>"]
        }}
    }}
}}

Focus on team dynamics, communication effectiveness, leadership patterns, and organizational behavior. Score 1-100 where 100 is optimal group performance. Be objective and evidence-based in your analysis.
"""


def analyze_group_dynamics(transcripts: List[Dict], google_api_key: str) -> Dict[str, Any]:
    """
    Analyze group dynamics using Google Gemini API.
    
    Args:
        transcripts: List of transcript data dictionaries
        google_api_key: Google API key for Gemini
        
    Returns:
        Dictionary containing group analysis results
    """
    try:
        # Configure Gemini API
        genai.configure(api_key=google_api_key)
        model = genai.GenerativeModel('gemini-1.5-pro')  # Using pro for more complex analysis
        
        # Create analysis prompt
        prompt = create_group_analysis_prompt(transcripts)
        
        print("Analyzing group dynamics with Google Gemini...")
        print(f"Processing {len(transcripts)} transcripts...")
        
        # Generate response with optimized config for JSON output
        generation_config = {
            "max_output_tokens": 8000,  # Larger for comprehensive group analysis
            "temperature": 0.2,         # Low temperature for consistent JSON
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
            "model_used": "gemini-1.5-pro",
            "analysis_timestamp": datetime.now().isoformat(),
            "transcript_count": len(transcripts),
            "transcript_sources": [t.get("conversation_id", "unknown") for t in transcripts]
        }
        
        return {
            "success": True,
            "group_analysis": analysis_result
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
            "message": f"Error during group analysis: {str(e)}"
        }


def load_transcripts_from_folder(folder_path: str) -> List[Dict[str, Any]]:
    """
    Load all transcript JSON files from the specified folder.
    
    Args:
        folder_path: Path to the transcripts folder
        
    Returns:
        List of transcript dictionaries
    """
    transcripts = []
    
    # Get all JSON files in the transcripts folder
    json_files = glob.glob(os.path.join(folder_path, "*.json"))
    
    if not json_files:
        print(f"No JSON files found in {folder_path}")
        return transcripts
    
    print(f"Found {len(json_files)} transcript files:")
    
    for json_file in json_files:
        try:
            print(f"  - Loading: {os.path.basename(json_file)}")
            with open(json_file, 'r', encoding='utf-8') as f:
                transcript_data = json.load(f)
                transcripts.append(transcript_data)
        except Exception as e:
            print(f"  ❌ Error loading {json_file}: {str(e)}")
    
    print(f"Successfully loaded {len(transcripts)} transcripts")
    return transcripts


def display_group_analysis_results(analysis: Dict[str, Any]) -> None:
    """
    Display the group analysis results in a formatted way.
    """
    group_data = analysis.get("group_analysis", {})
    
    print(f"\n🎯 OVERALL GROUP COHESION SCORE: {group_data.get('overall_group_cohesion_score', 'N/A')}/100")
    print(f"👥 GROUP SIZE: {group_data.get('group_size', 'N/A')} participants")
    print(f"🏆 GROUP EFFECTIVENESS: {group_data.get('recommendations', {}).get('group_effectiveness', 'N/A')}")
    
    print(f"\n📋 EXECUTIVE SUMMARY:")
    print(f"{group_data.get('executive_summary', 'N/A')}")
    
    # Group dynamics scores
    dynamics = group_data.get('group_dynamics', {})
    if dynamics:
        print(f"\n📊 GROUP DYNAMICS SCORES:")
        print("-" * 60)
        for dimension, data in dynamics.items():
            score = data.get('score', 'N/A')
            print(f"• {dimension.replace('_', ' ').title()}: {score}/100")
    
    # Individual profiles
    profiles = group_data.get('individual_profiles', [])
    if profiles:
        print(f"\n👤 INDIVIDUAL PARTICIPANT PROFILES:")
        print("-" * 60)
        for i, profile in enumerate(profiles, 1):
            print(f"\n📋 Participant {i} ({profile.get('participant_id', 'Unknown')}):")
            print(f"  🗣️  Communication Style: {profile.get('communication_style', 'N/A')}")
            print(f"  👑 Leadership Traits: {profile.get('leadership_traits', 'N/A')}")
            print(f"  🤝 Collaboration Approach: {profile.get('collaboration_approach', 'N/A')}")
            
            contributions = profile.get('key_contributions', [])
            if contributions:
                print(f"  💡 Key Contributions:")
                for contrib in contributions[:2]:  # Show top 2
                    print(f"    • {contrib}")
    
    # Group strengths and challenges
    strengths = group_data.get('group_strengths', [])
    challenges = group_data.get('group_challenges', [])
    
    if strengths or challenges:
        print(f"\n⚡ GROUP DYNAMICS ANALYSIS:")
        print("-" * 60)
        
        if strengths:
            print("💪 Group Strengths:")
            for strength in strengths[:4]:  # Show top 4
                print(f"  • {strength}")
        
        if challenges:
            print("\n⚠️ Group Challenges:")
            for challenge in challenges[:4]:  # Show top 4
                print(f"  • {challenge}")
    
    # Interaction patterns
    patterns = group_data.get('interaction_patterns', {})
    if patterns:
        print(f"\n🔄 INTERACTION PATTERNS:")
        print("-" * 60)
        
        dominant = patterns.get('dominant_speakers', [])
        if dominant:
            print(f"🎤 Dominant Speakers: {', '.join(dominant)}")
        
        quiet = patterns.get('quiet_participants', [])
        if quiet:
            print(f"🤐 Quiet Participants: {', '.join(quiet)}")
        
        pairs = patterns.get('collaboration_pairs', [])
        if pairs:
            print(f"🤝 Strong Collaboration Pairs: {', '.join(pairs)}")
    
    # Recommendations
    recommendations = group_data.get('recommendations', {})
    if recommendations:
        print(f"\n🎯 RECOMMENDATIONS:")
        print("-" * 60)
        
        actions = recommendations.get('improvement_actions', [])
        if actions:
            print("📝 Improvement Actions:")
            for action in actions[:4]:  # Show top 4
                print(f"  • {action}")
        
        leadership_recs = recommendations.get('leadership_recommendations', [])
        if leadership_recs:
            print("\n👑 Leadership Recommendations:")
            for rec in leadership_recs[:2]:  # Show top 2
                print(f"  • {rec}")
    
    # Risk assessment
    risk_assessment = group_data.get('risk_assessment', {})
    if risk_assessment:
        print(f"\n🚨 RISK ASSESSMENT:")
        print("-" * 60)
        
        high_risks = risk_assessment.get('high_risk_areas', [])
        if high_risks:
            print("🔴 High Risk Areas:")
            for risk in high_risks:
                print(f"  • {risk}")
        
        strategies = risk_assessment.get('mitigation_strategies', [])
        if strategies:
            print("\n🛡️ Mitigation Strategies:")
            for strategy in strategies[:2]:  # Show top 2
                print(f"  • {strategy}")


def main() -> None:
    load_dotenv()
    
    # Load Google API key from environment
    google_api_key = os.getenv("GOOGLE_API_KEY")
    
    if google_api_key is None:
        raise ValueError("Please set the GOOGLE_API_KEY environment variable in .env")
    
    # Define transcripts folder path
    transcripts_folder = "./transcripts"
    
    print("="*80)
    print("GROUP DYNAMICS ANALYSIS WITH GOOGLE GEMINI")
    print("="*80)
    print(f"Loading transcripts from: {os.path.abspath(transcripts_folder)}")
    
    # Load all transcripts from the folder
    transcripts = load_transcripts_from_folder(transcripts_folder)
    
    if not transcripts:
        print("❌ No transcripts found or loaded successfully.")
        print("Please ensure the transcripts folder contains valid JSON files.")
        return
    
    if len(transcripts) < 2:
        print(f"⚠️ Only {len(transcripts)} transcript(s) found. Group analysis works best with 2+ participants.")
    
    print(f"\n{'='*80}")
    print("ANALYZING GROUP DYNAMICS WITH GOOGLE GEMINI")
    print("="*80)
    
    # Perform group analysis using Google Gemini
    analysis_result = analyze_group_dynamics(
        transcripts=transcripts,
        google_api_key=google_api_key
    )
    
    if analysis_result.get("success"):
        # Display results in a formatted way
        display_group_analysis_results(analysis_result)
        
        # Save full analysis results to workflow/interview_analysis folder
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        analysis_filename = f"group_dynamics_analysis_{timestamp}.json"
        
        # Ensure the interview_analysis directory exists
        analysis_dir = "./"
        os.makedirs(analysis_dir, exist_ok=True)
        
        # Full path to the analysis file
        analysis_filepath = os.path.join(analysis_dir, analysis_filename)
        
        with open(analysis_filepath, 'w', encoding='utf-8') as f:
            json.dump(analysis_result, f, indent=2, ensure_ascii=False)
        
        print(f"\n💾 Full analysis saved to: {os.path.abspath(analysis_filepath)}")
        print(f"\n{'='*80}")
        print("GROUP DYNAMICS ANALYSIS COMPLETED")
        print("="*80)
        
    else:
        print(f"\n❌ Group analysis failed:")
        print(f"Error: {analysis_result.get('message', 'Unknown error')}")
        if analysis_result.get('raw_response'):
            print(f"Raw response: {analysis_result['raw_response'][:500]}...")


if __name__ == "__main__":
    main()