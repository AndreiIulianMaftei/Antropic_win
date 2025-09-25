# /Complete workflow/main.py
import os
import json
import asyncio
from dotenv import load_dotenv

# Imports from other files in the project
from core.workflow import FounderAnalysisOrchestrator
from agents.analysis_report_agent import create_analysis_agent, run_analysis_agent

async def main(input_file = "sample_frontend_input.json", interview_file = "sample_interview_analysis_input.json"):
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

    with open(interview_file, "r") as f:
        interview_data = json.load(f)
    inter_dict = {item["id"]: item for item in interview_data}



    for founder in final_output["data"]["teamList"]:
        founder["interview_analysis"] = inter_dict[founder["id"]]
    # Print the final, enriched JSON to the console
    print("\n\n--- FINAL ENRICHED OUTPUT FOR FRONTEND ---")
    print(json.dumps(final_output, indent=2))

    # Save the final output to a file
    output_file = "final_analysis_output.json"
    with open(output_file, "w") as f:
        json.dump(final_output, f, indent=2)
    print(f"\nOutput saved to {output_file}")
    a_agent = create_analysis_agent()
    report = await run_analysis_agent(a_agent, json.dumps(final_output["data"]["teamList"]))
    print("\n\n--- ANALYSIS REPORT ---")
    report_json = report.dict()
    print(json.dumps(report_json, indent=2))
    report_file = "analysis_report.json"
    with open(report_file, "w") as f:
        json.dump(report_json, f, indent=2)
    print(f"\nReport saved to {report_file}")

if __name__ == "__main__":
    # Create a sample input file for testing if it doesn't exist
    input_filename = "sample_frontend_input.json"
    interview_input_filename = "sample_interview_input.json"
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


