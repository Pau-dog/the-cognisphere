"""
FastAPI application for The Cognisphere simulation engine.

Provides REST API endpoints for controlling simulations, accessing data,
and real-time visualization of emergent civilization dynamics.
"""

import asyncio
from typing import Optional
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import uvicorn

from simulation.engine import SimulationEngine, SimulationConfig, SimulationState
from simulation.environmental_stimuli import EnvironmentalStimuliManager, StimulusType
from adapters import LLMMode


# Request/Response models
class SimulationConfigRequest(BaseModel):
    num_agents: int = 300
    seed: Optional[int] = 42
    max_ticks: int = 10000
    llm_mode: str = "mock"
    llm_model: str = "gpt-3.5-turbo"
    llm_temperature: float = 0.3
    tick_duration_ms: int = 100
    agents_per_tick: int = 50
    interactions_per_tick: int = 100
    memory_backend: str = "networkx"
    vector_backend: str = "faiss"
    snapshot_frequency: int = 20
    snapshot_directory: str = "snapshots"
    stimuli_file: Optional[str] = None


class SimulationControlRequest(BaseModel):
    action: str  # "start", "pause", "resume", "stop", "step"


class SnapshotRequest(BaseModel):
    name: Optional[str] = None


# Global simulation engine instance
simulation_engine: Optional[SimulationEngine] = None

# Create FastAPI app
app = FastAPI(
    title="The Cognisphere API",
    description="API for emergent intelligence civilization simulation",
    version="0.1.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup_event():
    """Initialize the simulation engine on startup."""
    global simulation_engine
    try:
        config = SimulationConfig()
        simulation_engine = SimulationEngine(config)
        print("Simulation engine initialized on startup")
    except Exception as e:
        print(f"Failed to initialize simulation engine: {e}")


@app.on_event("shutdown")
async def shutdown_event():
    """Clean up resources on shutdown."""
    global simulation_engine
    if simulation_engine:
        simulation_engine.cleanup()
        print("Simulation engine cleaned up")


# Health check endpoints
@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "timestamp": "2024-01-01T00:00:00Z"}

@app.get("/healthz")
async def healthz():
    """Kubernetes-style health check endpoint."""
    return {"ok": True}

@app.get("/")
async def root():
    """Root endpoint with basic information."""
    return {
        "name": "The Cognisphere API",
        "version": "0.1.0",
        "description": "Emergent Intelligence Civilization Engine API",
        "status": "running",
        "endpoints": {
            "docs": "/docs",
            "health": "/health",
            "healthz": "/healthz",
            "simulation": "/simulation",
            "agents": "/agents",
            "culture": "/culture",
            "economy": "/economy"
        }
    }


# Simulation control endpoints
@app.post("/simulation/initialize")
async def initialize_simulation(config: SimulationConfigRequest):
    """Initialize a new simulation with the given configuration."""
    global simulation_engine
    
    try:
        # Convert request to config
        sim_config = SimulationConfig(
            num_agents=config.num_agents,
            seed=config.seed,
            max_ticks=config.max_ticks,
            llm_mode=LLMMode(config.llm_mode),
            llm_model=config.llm_model,
            llm_temperature=config.llm_temperature,
            tick_duration_ms=config.tick_duration_ms,
            agents_per_tick=config.agents_per_tick,
            interactions_per_tick=config.interactions_per_tick,
            memory_backend=config.memory_backend,
            vector_backend=config.vector_backend,
            snapshot_frequency=config.snapshot_frequency,
            snapshot_directory=config.snapshot_directory,
            stimuli_file=config.stimuli_file
        )
        
        # Create new simulation engine
        simulation_engine = SimulationEngine(sim_config)
        success = await simulation_engine.initialize()
        
        if success:
            return {"status": "initialized", "config": sim_config.to_dict()}
        else:
            raise HTTPException(status_code=500, detail="Failed to initialize simulation")
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/simulation/control")
async def control_simulation(request: SimulationControlRequest):
    """Control simulation execution (start, pause, resume, stop, step)."""
    global simulation_engine
    
    if not simulation_engine:
        raise HTTPException(status_code=400, detail="Simulation not initialized")
    
    try:
        action = request.action.lower()
        
        if action == "start":
            if simulation_engine.state == SimulationState.READY:
                # Start simulation in background
                asyncio.create_task(simulation_engine.run_simulation())
                return {"status": "started"}
            else:
                raise HTTPException(status_code=400, detail="Simulation not ready")
        
        elif action == "pause":
            await simulation_engine.pause_simulation()
            return {"status": "paused"}
        
        elif action == "resume":
            await simulation_engine.resume_simulation()
            return {"status": "resumed"}
        
        elif action == "stop":
            await simulation_engine.stop_simulation()
            return {"status": "stopped"}
        
        elif action == "step":
            await simulation_engine.step_simulation()
            return {"status": "stepped"}
        
        else:
            raise HTTPException(status_code=400, detail=f"Unknown action: {action}")
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/simulation/status")
async def get_simulation_status():
    """Get current simulation status."""
    global simulation_engine
    
    if not simulation_engine:
        return {"status": "not_initialized"}
    
    try:
        status = await simulation_engine.get_simulation_status()
        return status
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Data access endpoints
@app.get("/agents")
async def get_agents(agent_id: Optional[str] = None):
    """Get agent data."""
    global simulation_engine
    
    if not simulation_engine:
        raise HTTPException(status_code=400, detail="Simulation not initialized")
    
    try:
        data = await simulation_engine.get_agent_data(agent_id)
        return data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/agents/{agent_id}")
async def get_agent(agent_id: str):
    """Get specific agent data."""
    global simulation_engine
    
    if not simulation_engine:
        raise HTTPException(status_code=400, detail="Simulation not initialized")
    
    try:
        data = await simulation_engine.get_agent_data(agent_id)
        if not data:
            raise HTTPException(status_code=404, detail="Agent not found")
        return data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/culture")
async def get_cultural_data():
    """Get cultural data (myths, norms, slang)."""
    global simulation_engine
    
    if not simulation_engine:
        raise HTTPException(status_code=400, detail="Simulation not initialized")
    
    try:
        data = await simulation_engine.get_cultural_data()
        return data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/economy")
async def get_economic_data():
    """Get economic data."""
    global simulation_engine
    
    if not simulation_engine:
        raise HTTPException(status_code=400, detail="Simulation not initialized")
    
    try:
        data = await simulation_engine.get_economic_data()
        return data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/network")
async def get_network_data():
    """Get agent network data for visualization."""
    global simulation_engine
    
    if not simulation_engine:
        raise HTTPException(status_code=400, detail="Simulation not initialized")
    
    try:
        data = await simulation_engine.get_network_data()
        return data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/world")
async def get_world_summary():
    """Get comprehensive world summary."""
    global simulation_engine
    
    if not simulation_engine:
        raise HTTPException(status_code=400, detail="Simulation not initialized")
    
    try:
        if simulation_engine.world:
            summary = simulation_engine.world.get_world_summary()
            return summary
        else:
            return {"error": "World not initialized"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Snapshot endpoints
@app.post("/snapshots")
async def take_snapshot(request: SnapshotRequest):
    """Take a snapshot of the current simulation state."""
    global simulation_engine
    
    if not simulation_engine:
        raise HTTPException(status_code=400, detail="Simulation not initialized")
    
    try:
        snapshot_file = await simulation_engine.take_snapshot(request.name)
        return {"status": "snapshot_created", "file": snapshot_file}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/snapshots")
async def list_snapshots():
    """List available snapshots."""
    global simulation_engine
    
    if not simulation_engine:
        raise HTTPException(status_code=400, detail="Simulation not initialized")
    
    try:
        snapshots = simulation_engine.snapshots
        return {"snapshots": [{"name": s["name"], "tick": s["tick"], "timestamp": s["timestamp"]} for s in snapshots]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/snapshots/load")
async def load_snapshot(snapshot_file: str):
    """Load a snapshot and restore simulation state."""
    global simulation_engine
    
    if not simulation_engine:
        raise HTTPException(status_code=400, detail="Simulation not initialized")
    
    try:
        success = await simulation_engine.load_snapshot(snapshot_file)
        if success:
            return {"status": "snapshot_loaded", "file": snapshot_file}
        else:
            raise HTTPException(status_code=500, detail="Failed to load snapshot")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Real-time data endpoints for dashboard
@app.get("/realtime/status")
async def get_realtime_status():
    """Get real-time simulation status for dashboard."""
    global simulation_engine
    
    if not simulation_engine:
        return {"status": "not_initialized", "data": None}
    
    try:
        status = await simulation_engine.get_simulation_status()
        
        # Add real-time metrics
        if simulation_engine.world:
            status["realtime"] = {
                "current_tick": simulation_engine.world.current_tick,
                "agent_count": len(simulation_engine.world.agents),
                "faction_count": len(simulation_engine.world.factions),
                "active_events": len(simulation_engine.world.event_system.active_events),
                "myth_count": len(simulation_engine.world.culture.myths),
                "norm_count": len(simulation_engine.world.culture.active_norms),
                "trade_count": len(simulation_engine.world.economy.trade_history)
            }
        
        return status
    except Exception as e:
        return {"status": "error", "error": str(e)}


@app.get("/realtime/network")
async def get_realtime_network():
    """Get real-time network data for visualization."""
    global simulation_engine
    
    if not simulation_engine:
        return {"nodes": [], "edges": []}
    
    try:
        data = await simulation_engine.get_network_data()
        return data
    except Exception as e:
        return {"nodes": [], "edges": [], "error": str(e)}


@app.get("/realtime/culture")
async def get_realtime_culture():
    """Get real-time cultural data."""
    global simulation_engine
    
    if not simulation_engine:
        return {"myths": [], "norms": [], "slang": []}
    
    try:
        data = await simulation_engine.get_cultural_data()
        return data
    except Exception as e:
        return {"myths": [], "norms": [], "slang": [], "error": str(e)}


@app.get("/realtime/economy")
async def get_realtime_economy():
    """Get real-time economic data."""
    global simulation_engine
    
    if not simulation_engine:
        return {"market": {}, "gini_coefficient": 0.0}
    
    try:
        data = await simulation_engine.get_economic_data()
        return data
    except Exception as e:
        return {"market": {}, "gini_coefficient": 0.0, "error": str(e)}


# Statistics and analytics endpoints
@app.get("/stats/performance")
async def get_performance_stats():
    """Get simulation performance statistics."""
    global simulation_engine
    
    if not simulation_engine:
        raise HTTPException(status_code=400, detail="Simulation not initialized")
    
    try:
        if simulation_engine.scheduler:
            stats = simulation_engine.scheduler.get_performance_stats()
            return stats
        else:
            return {"error": "Scheduler not initialized"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/stats/history")
async def get_simulation_history():
    """Get simulation tick history."""
    global simulation_engine
    
    if not simulation_engine:
        raise HTTPException(status_code=400, detail="Simulation not initialized")
    
    try:
        if simulation_engine.world and simulation_engine.world.tick_history:
            return {"history": simulation_engine.world.tick_history}
        else:
            return {"history": []}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Utility endpoints
@app.get("/config")
async def get_config():
    """Get current simulation configuration."""
    global simulation_engine
    
    if not simulation_engine:
        raise HTTPException(status_code=400, detail="Simulation not initialized")
    
    try:
        return {"config": simulation_engine.config.to_dict()}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/reset")
async def reset_simulation():
    """Reset the simulation to initial state."""
    global simulation_engine
    
    if not simulation_engine:
        raise HTTPException(status_code=400, detail="Simulation not initialized")
    
    try:
        # Stop current simulation
        await simulation_engine.stop_simulation()
        
        # Reinitialize
        success = await simulation_engine.initialize()
        
        if success:
            return {"status": "reset_complete"}
        else:
            raise HTTPException(status_code=500, detail="Failed to reset simulation")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Environmental Stimuli endpoints
@app.get("/stimuli/status")
async def get_stimuli_status():
    """Get environmental stimuli system status."""
    try:
        if not simulation_engine:
            raise HTTPException(status_code=404, detail="No active simulation")
        
        status = simulation_engine.get_environmental_stimuli_status()
        return status
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/stimuli/active")
async def get_active_stimuli():
    """Get currently active environmental stimuli."""
    try:
        if not simulation_engine or not simulation_engine.stimuli_manager:
            raise HTTPException(status_code=404, detail="No active simulation or stimuli manager")
        
        stimuli = simulation_engine.stimuli_manager.get_active_stimuli()
        
        # Convert to JSON-serializable format
        stimuli_data = []
        for stimulus in stimuli:
            stimuli_data.append({
                "id": stimulus.id,
                "type": stimulus.stimulus_type.value,
                "title": stimulus.title,
                "content": stimulus.content[:200] + "..." if len(stimulus.content) > 200 else stimulus.content,
                "source": stimulus.source,
                "timestamp": stimulus.timestamp.isoformat(),
                "intensity": stimulus.intensity.value,
                "sentiment": stimulus.sentiment,
                "keywords": stimulus.keywords,
                "cultural_impact": stimulus.cultural_impact,
                "economic_impact": stimulus.economic_impact,
                "social_impact": stimulus.social_impact
            })
        
        return {
            "count": len(stimuli_data),
            "stimuli": stimuli_data
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/stimuli/by-type/{stimulus_type}")
async def get_stimuli_by_type(stimulus_type: str):
    """Get stimuli filtered by type."""
    try:
        if not simulation_engine or not simulation_engine.stimuli_manager:
            raise HTTPException(status_code=404, detail="No active simulation or stimuli manager")
        
        # Validate stimulus type
        try:
            stimulus_type_enum = StimulusType(stimulus_type)
        except ValueError:
            raise HTTPException(status_code=400, detail=f"Invalid stimulus type: {stimulus_type}")
        
        stimuli = simulation_engine.stimuli_manager.get_stimuli_by_type(stimulus_type_enum)
        
        # Convert to JSON-serializable format
        stimuli_data = []
        for stimulus in stimuli:
            stimuli_data.append({
                "id": stimulus.id,
                "type": stimulus.stimulus_type.value,
                "title": stimulus.title,
                "content": stimulus.content[:200] + "..." if len(stimulus.content) > 200 else stimulus.content,
                "source": stimulus.source,
                "timestamp": stimulus.timestamp.isoformat(),
                "intensity": stimulus.intensity.value,
                "sentiment": stimulus.sentiment,
                "keywords": stimulus.keywords,
                "cultural_impact": stimulus.cultural_impact,
                "economic_impact": stimulus.economic_impact,
                "social_impact": stimulus.social_impact
            })
        
        return {
            "type": stimulus_type,
            "count": len(stimuli_data),
            "stimuli": stimuli_data
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/stimuli/fetch")
async def fetch_stimuli():
    """Manually trigger fetching of environmental stimuli."""
    try:
        if not simulation_engine or not simulation_engine.stimuli_manager:
            raise HTTPException(status_code=404, detail="No active simulation or stimuli manager")
        
        # Fetch stimuli
        stimuli = await simulation_engine.stimuli_manager.fetch_all_stimuli()
        
        return {
            "status": "success",
            "fetched_count": len(stimuli),
            "message": f"Fetched {len(stimuli)} environmental stimuli"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/stimuli/divergence")
async def get_cultural_divergence():
    """Get cultural divergence analysis from reality."""
    try:
        if not simulation_engine or not simulation_engine.stimuli_manager:
            raise HTTPException(status_code=404, detail="No active simulation or stimuli manager")
        
        divergence_summary = simulation_engine.stimuli_manager.get_cultural_divergence_summary()
        
        return {
            "cultural_divergence": divergence_summary,
            "interpretation": {
                "mirroring_factor": f"{divergence_summary['mirroring_factor']:.1%} of culture mirrors reality",
                "divergence_rate": f"{divergence_summary['divergence_rate']:.1%} divergence rate per stimulus",
                "reality_baseline": "Baseline patterns from real-world data",
                "future_projection": "Culture evolving toward future version of reality"
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Error handlers
@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """Global exception handler."""
    return JSONResponse(
        status_code=500,
        content={"detail": f"Internal server error: {str(exc)}"}
    )


if __name__ == "__main__":
    uvicorn.run(
        "app:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
