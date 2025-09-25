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

class UserProfile(BaseModel):
    name: str
    linkedin_url: str = None
    github_url: str = None
    university: str = None
    email: str = None  # Optional additional field
    bio: str = None    # Optional additional field

class UserProfileResponse(BaseModel):
    success: bool
    profile_id: str = None
    message: str = None
    data: UserProfile = None
    error: str = None

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
            {"path": "/api/profile", "method": "POST", "description": "Create user profile with name, LinkedIn, GitHub, university"},
            {"path": "/api/profile/{profile_id}", "method": "GET", "description": "Get user profile by ID"},
            {"path": "/api/profiles", "method": "GET", "description": "List all user profiles"},
            {"path": "/api/profile/{profile_id}", "method": "DELETE", "description": "Delete user profile"}
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

# Helper function to get next profile number
def get_next_profile_number():
    """Get the next incremental profile number"""
    os.makedirs("user_profiles", exist_ok=True)
    
    # Find existing profile files
    existing_files = []
    for filename in os.listdir("user_profiles"):
        if filename.endswith(".json") and filename[:-5].isdigit():
            existing_files.append(int(filename[:-5]))
    
    # Return next number (starting from 1)
    return max(existing_files) + 1 if existing_files else 1

# User profile endpoints
@app.post("/api/profile", response_model=UserProfileResponse)
async def create_user_profile(profile: UserProfile):
    """Create or update a user profile with name, LinkedIn, GitHub, and university info"""
    try:
        # Generate incremental profile ID
        profile_number = get_next_profile_number()
        profile_id = str(profile_number)
        
        # Here you can add validation logic
        if not profile.name or len(profile.name.strip()) == 0:
            raise HTTPException(status_code=400, detail="Name is required")
        
        # Validate URLs if provided
        if profile.linkedin_url and not (profile.linkedin_url.startswith('http://') or profile.linkedin_url.startswith('https://')):
            raise HTTPException(status_code=400, detail="LinkedIn URL must start with http:// or https://")
        
        if profile.github_url and not (profile.github_url.startswith('http://') or profile.github_url.startswith('https://')):
            raise HTTPException(status_code=400, detail="GitHub URL must start with http:// or https://")
        
        # Save profile data (you can implement database storage here)
        profile_data = {
            "profile_id": profile_id,
            "name": profile.name.strip(),
            "linkedin_url": profile.linkedin_url,
            "github_url": profile.github_url,
            "university": profile.university,
            "email": profile.email,
            "bio": profile.bio,
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat()
        }
        
        # Save to incremental JSON file
        try:
            filename = f"user_profiles/{profile_id}.json"
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(profile_data, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Warning: Could not save profile to file: {e}")
        
        return UserProfileResponse(
            success=True,
            profile_id=profile_id,
            message="User profile created successfully",
            data=profile
        )
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create user profile: {str(e)}")

@app.get("/api/profile/{profile_id}", response_model=UserProfileResponse)
async def get_user_profile(profile_id: str):
    """Retrieve a user profile by ID"""
    try:
        filename = f"user_profiles/{profile_id}.json"
        
        if not os.path.exists(filename):
            raise HTTPException(status_code=404, detail="Profile not found")
        
        with open(filename, 'r', encoding='utf-8') as f:
            profile_data = json.load(f)
        
        # Convert back to UserProfile model
        user_profile = UserProfile(
            name=profile_data["name"],
            linkedin_url=profile_data.get("linkedin_url"),
            github_url=profile_data.get("github_url"),
            university=profile_data.get("university"),
            email=profile_data.get("email"),
            bio=profile_data.get("bio")
        )
        
        return UserProfileResponse(
            success=True,
            profile_id=profile_id,
            message="Profile retrieved successfully",
            data=user_profile
        )
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to retrieve profile: {str(e)}")

@app.get("/api/profiles")
async def list_user_profiles():
    """List all user profiles"""
    try:
        profiles_dir = "user_profiles"
        if not os.path.exists(profiles_dir):
            return {"success": True, "profiles": [], "message": "No profiles found"}
        
        profiles = []
        for filename in os.listdir(profiles_dir):
            if filename.endswith('.json'):
                try:
                    with open(os.path.join(profiles_dir, filename), 'r', encoding='utf-8') as f:
                        profile_data = json.load(f)
                        profiles.append({
                            "profile_id": profile_data["profile_id"],
                            "name": profile_data["name"],
                            "university": profile_data.get("university"),
                            "created_at": profile_data["created_at"]
                        })
                except Exception as e:
                    print(f"Error reading profile {filename}: {e}")
                    continue
        
        return {
            "success": True,
            "profiles": sorted(profiles, key=lambda x: int(x["profile_id"]), reverse=True),
            "count": len(profiles),
            "message": f"Found {len(profiles)} profiles"
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to list profiles: {str(e)}")

@app.delete("/api/profile/{profile_id}")
async def delete_user_profile(profile_id: str):
    """Delete a user profile by ID"""
    try:
        filename = f"user_profiles/{profile_id}.json"
        
        if not os.path.exists(filename):
            raise HTTPException(status_code=404, detail="Profile not found")
        
        os.remove(filename)
        
        return {
            "success": True,
            "message": f"Profile {profile_id} deleted successfully"
        }
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to delete profile: {str(e)}")

# Example POST endpoint
@app.post("/api/data")
async def post_data(data: Dict[Any, Any]):
    """Accept and process POST data"""
    return {
        "message": "Data received successfully",
        "received_data": data,
        "timestamp": datetime.now().isoformat()
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