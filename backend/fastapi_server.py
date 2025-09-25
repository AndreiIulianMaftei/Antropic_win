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