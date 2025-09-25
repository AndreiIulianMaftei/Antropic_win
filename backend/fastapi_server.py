from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
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
            {"path": "/api/calls", "method": "POST", "description": "Get last call for agent"}
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
async def custom_404_handler(request, exc):
    return {
        "error": "Not Found",
        "message": f"The endpoint {request.url.path} was not found",
        "status_code": 404
    }

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