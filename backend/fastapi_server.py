from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Dict, Any
import os
from dotenv import load_dotenv
import json
from datetime import datetime

# Load environment variables
load_dotenv()

# Initialize FastAPI app
app = FastAPI(
    title="Antropic API Server",
    description="A FastAPI server for the Antropic project",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure this appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic models for request/response
class HealthResponse(BaseModel):
    status: str
    timestamp: str
    message: str

class AgentRequest(BaseModel):
    agent_id: str
    actor_name: str

class ApiResponse(BaseModel):
    success: bool
    data: Dict[Any, Any] = None
    message: str = None
    error: str = None

class SetupInfo(BaseModel):
    data: Dict[Any, Any]  # Accept any JSON structure

class Prospects(BaseModel):
    data: Dict[Any, Any]  # Accept any JSON structure

class DataResponse(BaseModel):
    success: bool
    id: str = None
    message: str = None
    data: Dict[Any, Any] = None
    error: str = None

# MAIN FULLSTACK FLOW DATATYPES
# INPUT MODELS
class StartupInfo(BaseModel):
    name: str
    product: str
    founded: str
    mission: str
    businessModel: str
    pitchDeck: str = None
    isManual: bool

class Prospect(BaseModel):
    id: str
    name: str
    email: str
    github: str = None
    linkedin: str
    university: str = None
    notes: str = None

class RequestData(BaseModel):
    startupInfo: StartupInfo
    teamList: list[Prospect]

class ProspectsRequest(BaseModel):
    data: RequestData

# OUTPUT MODELS
class ResearchDepth(BaseModel):
    hIndex: int

class FounderHighlight(BaseModel):
    name: str
    highlights: list[str]
    comments: str

class InterviewHighlight(BaseModel):
    question: str
    summary: str
    keyInsights: list[str]
    score: float
    person: str

class AnalysisResponse(BaseModel):
    overallScore: float
    disruptionProbability: float
    teamSynergy: float
    complementaryScore: float
    researchDepth: ResearchDepth
    founderHighlights: list[FounderHighlight]
    interviewHighlights: list[InterviewHighlight]

# Root endpoint
@app.get("/")
async def root():
    """Root endpoint - health check"""
    return {
        "message": "Antropic FastAPI Server is running!",
        "status": "healthy",
        "timestamp": datetime.now().isoformat()
    }

# Health check endpoint
@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint"""
    return HealthResponse(
        status="healthy",
        timestamp=datetime.now().isoformat(),
        message="Server is running properly"
    )

# API info endpoint
@app.get("/api/info")
async def api_info():
    """Get API information"""
    return {
        "name": "Antropic API",
        "version": "1.0.0",
        "endpoints": [
            {"path": "/", "method": "GET", "description": "Root endpoint"},
            {"path": "/health", "method": "GET", "description": "Health check"},
            {"path": "/api/info", "method": "GET", "description": "API information"},
            {"path": "/api/agent/{agent_id}", "method": "GET", "description": "Get agent information"},
            {"path": "/api/calls", "method": "POST", "description": "Get last call for agent"},
            {"path": "/api/setupinfo", "method": "POST", "description": "Receive setupinfo JSON data"},
            {"path": "/api/prospects", "method": "POST", "description": "Receive prospects JSON data"},
            {"path": "/api/setupinfo/{data_id}", "method": "GET", "description": "Get setupinfo by ID"},
            {"path": "/api/prospects/{data_id}", "method": "GET", "description": "Get prospects by ID"},
            {"path": "/api/data", "method": "GET", "description": "List all stored data"}
        ]
    }

# Agent endpoint
@app.get("/api/agent/{agent_id}")
async def get_agent(agent_id: str):
    """Get agent information by ID"""
    # This is a placeholder - you can implement your agent logic here
    return {
        "agent_id": agent_id,
        "status": "active",
        "timestamp": datetime.now().isoformat(),
        "message": f"Agent {agent_id} information retrieved"
    }

# Calls endpoint - similar to your existing functionality
@app.post("/api/calls", response_model=ApiResponse)
async def get_agent_calls(request: AgentRequest):
    """Get last call for a specific agent"""
    try:
        api_key = os.getenv("BEY_API_KEY")
        if not api_key:
            raise HTTPException(
                status_code=500, 
                detail="BEY_API_KEY not found in environment variables"
            )
        
        # Here you can integrate your existing beyond_presance.py logic
        # For now, returning a placeholder response
        return ApiResponse(
            success=True,
            data={
                "agent_id": request.agent_id,
                "actor_name": request.actor_name,
                "last_call": "placeholder_call_id",
                "timestamp": datetime.now().isoformat()
            },
            message="Agent calls retrieved successfully"
        )
    
    except Exception as e:
        return ApiResponse(
            success=False,
            error=str(e),
            message="Failed to retrieve agent calls"
        )

# Helper function to get next data number
def get_next_data_number(data_type: str):
    """Get the next incremental data number for setupinfo or prospects"""
    os.makedirs("data_storage", exist_ok=True)
    
    # Find existing files of this type
    existing_files = []
    for filename in os.listdir("data_storage"):
        if filename.startswith(f"{data_type}_") and filename.endswith(".json"):
            try:
                number = int(filename.replace(f"{data_type}_", "").replace(".json", ""))
                existing_files.append(number)
            except ValueError:
                continue
    
    # Return next number (starting from 1)
    return max(existing_files) + 1 if existing_files else 1

# SetupInfo endpoint
@app.post("/api/setupinfo", response_model=DataResponse)
async def receive_setupinfo(setupinfo: SetupInfo):
    """Receive and store setupinfo JSON data"""
    try:
        # Generate incremental ID
        data_number = get_next_data_number("setupinfo")
        data_id = str(data_number)
        
        # Prepare data for storage
        storage_data = {
            "id": data_id,
            "type": "setupinfo",
            "data": setupinfo.data,
            "received_at": datetime.now().isoformat()
        }
        
        # Save to incremental JSON file
        try:
            filename = f"data_storage/setupinfo_{data_id}.json"
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(storage_data, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Warning: Could not save setupinfo to file: {e}")
        
        return DataResponse(
            success=True,
            id=data_id,
            message="SetupInfo data received successfully",
            data=setupinfo.data
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to process setupinfo: {str(e)}")

# Get setupinfo by ID
@app.get("/api/setupinfo/{data_id}", response_model=DataResponse)
async def get_setupinfo(data_id: str):
    """Retrieve setupinfo data by ID"""
    try:
        filename = f"data_storage/setupinfo_{data_id}.json"
        
        if not os.path.exists(filename):
            raise HTTPException(status_code=404, detail="SetupInfo data not found")
        
        with open(filename, 'r', encoding='utf-8') as f:
            stored_data = json.load(f)
        
        return DataResponse(
            success=True,
            id=data_id,
            message="SetupInfo data retrieved successfully",
            data=stored_data["data"]
        )
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to retrieve setupinfo: {str(e)}")

# Get prospects by ID
@app.get("/api/prospects/{data_id}", response_model=DataResponse)
async def get_prospects(data_id: str):
    """Retrieve prospects data by ID"""
    try:
        filename = f"data_storage/prospects_{data_id}.json"
        
        if not os.path.exists(filename):
            raise HTTPException(status_code=404, detail="Prospects data not found")
        
        with open(filename, 'r', encoding='utf-8') as f:
            stored_data = json.load(f)
        
        return DataResponse(
            success=True,
            id=data_id,
            message="Prospects data retrieved successfully",
            data=stored_data["data"]
        )
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to retrieve prospects: {str(e)}")

# List all stored data
@app.get("/api/data")
async def list_all_data():
    """List all stored setupinfo and prospects data"""
    try:
        data_dir = "data_storage"
        if not os.path.exists(data_dir):
            return {"success": True, "data": [], "message": "No data found"}
        
        all_data = []
        for filename in os.listdir(data_dir):
            if filename.endswith('.json'):
                try:
                    with open(os.path.join(data_dir, filename), 'r', encoding='utf-8') as f:
                        stored_data = json.load(f)
                        all_data.append({
                            "id": stored_data["id"],
                            "type": stored_data["type"],
                            "received_at": stored_data["received_at"],
                            "filename": filename
                        })
                except Exception as e:
                    print(f"Error reading data {filename}: {e}")
                    continue
        
        return {
            "success": True,
            "data": sorted(all_data, key=lambda x: x["received_at"], reverse=True),
            "count": len(all_data),
            "message": f"Found {len(all_data)} data entries"
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to list data: {str(e)}")

# Generic data endpoint (fallback)
@app.post("/api/data")
async def post_generic_data(data: Dict[Any, Any]):
    """Accept and process generic POST data"""
    return {
        "message": "Generic data received successfully",
        "received_data": data,
        "timestamp": datetime.now().isoformat(),
        "note": "Use /api/setupinfo or /api/prospects for structured data"
    }

# Custom 404 handler
@app.exception_handler(404)
async def custom_404_handler(request: Request, exc):
    return JSONResponse(
        status_code=404,
        content={
            "error": "Not Found",
            "message": f"The endpoint {request.url.path} was not found",
            "status_code": 404
        }
    )

# Prospects endpoint
@app.post("/api/prospects", response_model=DataResponse)
async def receive_prospects(prospects: Prospects):
    """Receive and store prospects JSON data"""
    try:
        # Generate incremental ID
        data_number = get_next_data_number("prospects")
        data_id = str(data_number)
        
        # Prepare data for storage
        storage_data = {
            "id": data_id,
            "type": "prospects",
            "data": prospects.data,
            "received_at": datetime.now().isoformat()
        }
        
        # Save to incremental JSON file
        try:
            filename = f"data_storage/prospects_{data_id}.json"
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(storage_data, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Warning: Could not save prospects to file: {e}")
        
        return DataResponse(
            success=True,
            id=data_id,
            message="Prospects data received successfully",
            data=prospects.data
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to process prospects: {str(e)}")

# Sample response data
SAMPLE_RESPONSE = {
    "overallScore": 8.5,
    "disruptionProbability": 7.2,
    "teamSynergy": 9.1,
    "complementaryScore": 8.8,
    "researchDepth": {
        "hIndex": 15
    },
    "founderHighlights": [
        {
            "name": "John Doe",
            "highlights": [
                "Former VP at Google with 10+ years experience",
                "Published 25+ papers in AI/ML",
                "Led teams of 50+ engineers"
            ],
            "comments": "Strong technical leadership background with proven track record in scaling AI products."
        },
        {
            "name": "Jane Smith",
            "highlights": [
                "Stanford PhD in Computer Science",
                "3 successful exits as CTO",
                "Expert in distributed systems"
            ],
            "comments": "Exceptional technical depth with entrepreneurial experience."
        }
    ],
    "interviewHighlights": [
        {
            "question": "What is your biggest challenge in scaling AI products?",
            "summary": "Candidate demonstrated deep understanding of AI scalability challenges",
            "keyInsights": [
                "Identified data quality as primary bottleneck",
                "Proposed innovative MLOps solutions",
                "Showed experience with large-scale deployments"
            ],
            "score": 9.2,
            "person": "John Doe"
        },
        {
            "question": "How do you handle technical debt in fast-growing startups?",
            "summary": "Strong pragmatic approach to balancing speed vs. technical excellence",
            "keyInsights": [
                "Advocated for gradual refactoring strategies",
                "Emphasized importance of automated testing",
                "Demonstrated experience managing technical trade-offs"
            ],
            "score": 8.8,
            "person": "Jane Smith"
        },
        {
            "question": "Describe your leadership philosophy for technical teams",
            "summary": "Excellent people management skills with focus on team growth",
            "keyInsights": [
                "Promotes psychological safety in engineering teams",
                "Uses data-driven approaches for team optimization",
                "Strong track record of developing junior engineers"
            ],
            "score": 9.5,
            "person": "John Doe"
        }
    ]
}

# MAIN FASTAPI FLOW
@app.post("/api/analyse", response_model=AnalysisResponse)
async def analyze_prospects(request: ProspectsRequest):
    try:
        # DESTRUCTURE INPUT DATA FOR EASY ACCESS
        
        # Startup Information - All Properties Accessible
        startup_name = request.data.startupInfo.name
        startup_product = request.data.startupInfo.product
        startup_founded = request.data.startupInfo.founded
        startup_mission = request.data.startupInfo.mission
        startup_business_model = request.data.startupInfo.businessModel
        startup_pitch_deck = request.data.startupInfo.pitchDeck
        startup_is_manual = request.data.startupInfo.isManual
        
        # Team List - All Individual Prospects
        team_prospects = request.data.teamList
        team_size = len(team_prospects)
        
        # Individual Prospect Properties (easily accessible)
        prospect_details = []
        for prospect in team_prospects:
            prospect_info = {
                'id': prospect.id,
                'name': prospect.name,
                'email': prospect.email,
                'github': prospect.github,
                'linkedin': prospect.linkedin,
                'university': prospect.university,
                'notes': prospect.notes
            }
            prospect_details.append(prospect_info)
        
        # LOG RECEIVED DATA FOR DEBUGGING
        print("=" * 50)
        print("STARTUP INFORMATION:")
        print(f"  Name: {startup_name}")
        print(f"  Product: {startup_product}")
        print(f"  Founded: {startup_founded}")
        print(f"  Mission: {startup_mission}")
        print(f"  Business Model: {startup_business_model}")
        print(f"  Pitch Deck: {startup_pitch_deck}")
        print(f"  Is Manual: {startup_is_manual}")
        
        print("\nTEAM INFORMATION:")
        print(f"  Team Size: {team_size}")
        for i, prospect in enumerate(prospect_details, 1):
            print(f"  Prospect {i}:")
            print(f"    ID: {prospect['id']}")
            print(f"    Name: {prospect['name']}")
            print(f"    Email: {prospect['email']}")
            print(f"    GitHub: {prospect['github']}")
            print(f"    LinkedIn: {prospect['linkedin']}")
            print(f"    University: {prospect['university']}")
            print(f"    Notes: {prospect['notes']}")
        print("=" * 50)
        
        # PROCESSING SECTION
        # TODO: Replace this section with your actual analysis logic
        
        # Example processing using the destructured data:
        overall_score = analyze_overall_score(startup_business_model, team_size, prospect_details)
        disruption_prob = calculate_disruption_probability(startup_product, startup_mission)
        team_synergy = evaluate_team_synergy(prospect_details)
        complementary_score = calculate_complementary_skills(prospect_details)
        research_depth = assess_research_depth(prospect_details)
        founder_highlights = generate_founder_highlights(prospect_details)
        interview_highlights = process_interview_data(prospect_details)
        
        # STRUCTURED RESPONSE
        response = AnalysisResponse(
            overallScore=overall_score,
            disruptionProbability=disruption_prob,
            teamSynergy=team_synergy,
            complementaryScore=complementary_score,
            researchDepth=ResearchDepth(hIndex=research_depth),
            founderHighlights=founder_highlights,
            interviewHighlights=interview_highlights
        )
        
        return response
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to process request: {str(e)}")

# Replace these with your actual business logic

def analyze_overall_score(business_model: str, team_size: int, prospects: list[dict]) -> float:
    """
    Analyze overall score based on business model and team composition
    """
    # TODO: Implement your scoring logic here
    return 10.0

def calculate_disruption_probability(product: str, mission: str) -> float:
    """
    Calculate disruption probability based on product and mission
    """
    # TODO: Implement your disruption analysis logic
    keywords = ["ai", "ml", "blockchain", "automation", "revolutionize"]
    score = 6.0
    for keyword in keywords:
        if keyword in (product + " " + mission).lower():
            score += 0.5
    return min(score, 10.0)

def evaluate_team_synergy(prospects: list[dict]) -> float:
    """
    Evaluate how well the team works together
    """
    # TODO: Implement team synergy analysis
    # Consider universities, previous experience, skill complementarity
    return 8.5

def calculate_complementary_skills(prospects: list[dict]) -> float:
    """
    Calculate how complementary the team skills are
    """
    # TODO: Analyze skills from LinkedIn profiles, GitHub, etc.
    return 8.8

def assess_research_depth(prospects: list[dict]) -> int:
    """
    Assess the research depth of the team (h-index equivalent)
    """
    # TODO: Analyze academic background, publications, etc.
    return 15

def generate_founder_highlights(prospects: list[dict]) -> list[FounderHighlight]:
    """
    Generate highlights for each founder based on their data
    """
    # TODO: Process LinkedIn, GitHub, university data to generate highlights
    highlights = []
    for prospect in prospects:
        highlight = FounderHighlight(
            name=prospect['name'],
            highlights=[
                f"Profile analysis based on {prospect['linkedin']}",
                f"Technical skills inferred from {prospect['github'] or 'available data'}",
                f"Educational background: {prospect['university'] or 'Not specified'}"
            ],
            comments=f"Analysis pending for {prospect['name']} - implement detailed profiling logic."
        )
        highlights.append(highlight)
    return highlights

def process_interview_data(prospects: list[dict]) -> list[InterviewHighlight]:
    """
    Process interview data and generate insights
    """
    # TODO: Implement interview processing logic
    # This would typically involve AI analysis of interview responses
    sample_highlights = []
    for i, prospect in enumerate(prospects):
        highlight = InterviewHighlight(
            question=f"Sample question for {prospect['name']}",
            summary=f"Analysis summary for {prospect['name']}",
            keyInsights=[
                "Insight 1 based on responses",
                "Insight 2 from technical evaluation",
                "Insight 3 regarding leadership potential"
            ],
            score=8.0 + i * 0.3,
            person=prospect['name']
        )
        sample_highlights.append(highlight)
    return sample_highlights

if __name__ == "__main__":
    import uvicorn
    
    # Configuration
    host = "127.0.0.1"
    port = 8000
    
    print(f"Starting FastAPI server on http://{host}:{port}")
    print(f"API documentation available at http://{host}:{port}/docs")
    print(f"Alternative docs at http://{host}:{port}/redoc")
    
    # Run the server
    uvicorn.run(
        "fastapi_server:app",
        host=host,
        port=port,
        reload=True,  # Enable auto-reload during development
        log_level="info"
    )