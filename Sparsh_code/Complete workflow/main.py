# /Complete workflow/main.py
import os
import json
import asyncio
from dotenv import load_dotenv

# Imports from other files in the project
from founder_analysis_orchestrator import FounderAnalysisOrchestrator

async def main():
    """
    Main execution function to run the founder analysis workflow.
    """
    # Load environment variables from a .env file
    load_dotenv()
    openrouter_api_key = os.getenv("API_KEY")
    tavily_api_key = os.getenv("TAVILY_API_KEY")
    linkedin_cookie = os.getenv("LINKEDIN_COOKIE")

    # Corrected: Check only for API keys that are actively used in the provided code.
    if not all([openrouter_api_key, tavily_api_key, linkedin_cookie]):
        raise ValueError("One or more required environment variables (API_KEY, TAVILY_API_KEY, LINKEDIN_COOKIE) are missing from your .env file.")

    # Define the input file path
    input_file = "sample_frontend_input.json"

    # Load the input JSON from the frontend
    if not os.path.exists(input_file):
        print(f"Input file '{input_file}' not found. Please create it.")
        return
        
    with open(input_file, "r") as f:
        prospect_data = json.load(f)

    # Initialize and run the orchestrator
    orchestrator = FounderAnalysisOrchestrator(
        openrouter_api_key=openrouter_api_key,
        tavily_api_key=tavily_api_key
    )
    
    final_output = await orchestrator.run(prospect_data)

    # Print the final, enriched JSON to the console
    print("\n\n--- FINAL ENRICHED OUTPUT FOR FRONTEND ---")
    print(json.dumps(final_output, indent=2))

    # Save the final output to a file
    output_file = "final_analysis_output.json"
    with open(output_file, "w") as f:
        json.dump(final_output, f, indent=2)
    print(f"\nOutput saved to {output_file}")

if __name__ == "__main__":
    # Create a sample input file for testing if it doesn't exist
    input_filename = "sample_frontend_input.json"
    if not os.path.exists(input_filename):
        print(f"Creating sample input file: {input_filename}")
        sample_data = {
          "id": "2",
          "type": "prospects",
          "data": {
            "startupInfo": { "name": "DeepResearch AI" },
            "teamList": [
              {
                "id": "1",
                "name": "Yann LeCun",
                "github": "https://github.com/karpathy", # Using a known active profile for better testing
                "linkedin": "https://www.linkedin.com/in/yann-lecun/",
                "university": "New York University"
              },
              {
                "id": "2",
                "name": "Sheryl Sandberg",
                "github": "", # No GitHub
                "linkedin": "https://www.linkedin.com/in/sherylsandberg/",
                "university": "Harvard University"
              }
            ]
          },
          "received_at": "2025-09-25T14:48:08.884723"
        }
        with open(input_filename, "w") as f:
            json.dump(sample_data, f, indent=2)
            
    # Run the main asynchronous event loop
    asyncio.run(main())