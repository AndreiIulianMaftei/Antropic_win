# agentic_workflow_main.py
import os
import json
import asyncio
from dotenv import load_dotenv

# Imports from other files in the project
from app.core.workflow import FounderAnalysisOrchestrator
from app.agents.analysis_report_agent import create_analysis_agent, run_analysis_agent

async def run_founder_analysis(prospect_data: dict, interview_file: str = "output_samples/sample_interview_analysis_input.json"):
    """
    Run the founder analysis workflow with provided prospect data.
    
    Args:
        prospect_data: The data from the frontend POST request
        interview_file: Path to the interview data file (optional)
    
    Returns:
        dict: Complete analysis results including the analysis report
    """
    # Load environment variables
    load_dotenv()
    openrouter_api_key = os.getenv("API_KEY")
    tavily_api_key = os.getenv("TAVILY_API_KEY")
    linkedin_cookie = os.getenv("LINKEDIN_COOKIE")

    if not all([openrouter_api_key, tavily_api_key, linkedin_cookie]):
        raise ValueError("One or more required environment variables (API_KEY, TAVILY_API_KEY, LINKEDIN_COOKIE) are missing from your .env file.")

    # Initialize and run the orchestrator with the provided data
    orchestrator = FounderAnalysisOrchestrator(
        openrouter_api_key=openrouter_api_key,
        tavily_api_key=tavily_api_key
    )
    
    # Run the workflow with the prospect data from the POST request
    final_output = await orchestrator.run(prospect_data)

    # Load interview data if file exists
    if os.path.exists(interview_file):
        with open(interview_file, "r") as f:
            interview_data = json.load(f)
        inter_dict = {item["id"]: item for item in interview_data}

        # Add interview analysis to each founder
        for founder in final_output["data"]["teamList"]:
            if founder["id"] in inter_dict:
                founder["interview_analysis"] = inter_dict[founder["id"]]
    else:
        print(f"Interview file '{interview_file}' not found. Skipping interview analysis.")

    # Generate analysis report
    try:
        a_agent = create_analysis_agent()
        report = await run_analysis_agent(a_agent, json.dumps(final_output["data"]["teamList"]))
        report_json = report.dict()
        
        # Add the analysis report to the final output
        final_output["analysis_report"] = report_json
        
    except Exception as e:
        print(f"Error generating analysis report: {e}")
        final_output["analysis_report"] = {"error": f"Failed to generate report: {str(e)}"}

    return final_output

async def main(input_file="output_samples/sample_frontend_input.json", interview_file="output_samples/sample_interview_analysis_input.json"):
    """
    Main execution function for standalone testing.
    This is kept for backward compatibility and testing purposes.
    """
    # Load the input JSON from file (for testing)
    if not os.path.exists(input_file):
        print(f"Input file '{input_file}' not found. Please create it.")
        return
        
    with open(input_file, "r") as f:
        prospect_data = json.load(f)

    # Run the analysis
    final_output = await run_founder_analysis(prospect_data, interview_file)

    # Print and save results (for testing)
    print("\n\n--- FINAL ENRICHED OUTPUT FOR FRONTEND ---")
    print(json.dumps(final_output, indent=2))

    # Save outputs
    output_file = "output_samples/final_analysis_output.json"
    with open(output_file, "w") as f:
        json.dump(final_output, f, indent=2)
    print(f"\nOutput saved to {output_file}")

    if "analysis_report" in final_output and "error" not in final_output["analysis_report"]:
        print("\n\n--- ANALYSIS REPORT ---")
        print(json.dumps(final_output["analysis_report"], indent=2))
        report_file = "output_samples/analysis_report.json"
        with open(report_file, "w") as f:
            json.dump(final_output["analysis_report"], f, indent=2)
        print(f"\nReport saved to {report_file}")

if __name__ == "__main__":
    # Create a sample input file for testing if it doesn't exist
    input_filename = "output_samples/sample_frontend_input.json"
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
                "github": "https://github.com/karpathy",
                "linkedin": "https://www.linkedin.com/in/yann-lecun/",
                "university": "New York University"
              },
              {
                "id": "2",
                "name": "Sheryl Sandberg",
                "github": "",
                "linkedin": "https://www.linkedin.com/in/sherylsandberg/",
                "university": "Harvard University"
              }
            ]
          },
          "received_at": "2025-09-25T14:48:08.884723"
        }
        with open(input_filename, "w") as f:
            json.dump(sample_data, f, indent=2)
            
    # Run the main asynchronous event loop for testing
    asyncio.run(main())