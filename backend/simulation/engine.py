"""
Main simulation engine that coordinates all systems.

The SimulationEngine is the central coordinator that manages the world state,
scheduler, and all simulation systems to create emergent civilization dynamics.
"""

import asyncio
import time
from typing import Dict, List, Optional, Any, Callable
from dataclasses import dataclass
from enum import Enum
import json
import os
from pathlib import Path

from .world import World, WorldState
from .scheduler import SimulationScheduler, SchedulerConfig, SchedulerState
from .agents import Agent, AgentPersonality
from .adapters import LLMAdapter, LLMAdapterFactory, LLMConfig, LLMMode


class SimulationState(Enum):
    """Overall simulation states."""
    UNINITIALIZED = "uninitialized"
    INITIALIZING = "initializing"
    READY = "ready"
    RUNNING = "running"
    PAUSED = "paused"
    STOPPED = "stopped"
    ERROR = "error"


@dataclass
class SimulationConfig:
    """Configuration for the simulation engine."""
    # World settings
    num_agents: int = 300
    seed: Optional[int] = 42
    max_ticks: int = 10000
    
    # LLM settings
    llm_mode: LLMMode = LLMMode.MOCK
    llm_model: str = "gpt-3.5-turbo"
    llm_temperature: float = 0.3
    llm_api_key: Optional[str] = None
    
    # Scheduler settings
    tick_duration_ms: int = 100
    agents_per_tick: int = 50
    interactions_per_tick: int = 100
    
    # Memory settings
    memory_backend: str = "networkx"  # "neo4j" or "networkx"
    vector_backend: str = "faiss"     # "faiss" or "chroma"
    
    # Snapshot settings
    snapshot_frequency: int = 20
    snapshot_directory: str = "snapshots"
    
    # Stimuli settings
    stimuli_file: Optional[str] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert config to dictionary."""
        return {
            "num_agents": self.num_agents,
            "seed": self.seed,
            "max_ticks": self.max_ticks,
            "llm_mode": self.llm_mode.value,
            "llm_model": self.llm_model,
            "llm_temperature": self.llm_temperature,
            "tick_duration_ms": self.tick_duration_ms,
            "agents_per_tick": self.agents_per_tick,
            "interactions_per_tick": self.interactions_per_tick,
            "memory_backend": self.memory_backend,
            "vector_backend": self.vector_backend,
            "snapshot_frequency": self.snapshot_frequency,
            "snapshot_directory": self.snapshot_directory,
            "stimuli_file": self.stimuli_file
        }


class SimulationEngine:
    """Main simulation engine coordinating all systems."""
    
    def __init__(self, config: SimulationConfig):
        self.config = config
        self.state = SimulationState.UNINITIALIZED
        
        # Core systems
        self.world: Optional[World] = None
        self.scheduler: Optional[SimulationScheduler] = None
        self.llm_adapter: Optional[LLMAdapter] = None
        
        # State tracking
        self.start_time: Optional[float] = None
        self.end_time: Optional[float] = None
        self.snapshots: List[Dict[str, Any]] = []
        
        # Callbacks
        self.tick_callbacks: List[Callable[[int], None]] = []
        self.completion_callbacks: List[Callable[[], None]] = []
        self.error_callbacks: List[Callable[[str], None]] = []
    
    async def initialize(self) -> bool:
        """Initialize the simulation engine."""
        try:
            self.state = SimulationState.INITIALIZING
            print("Initializing simulation engine...")
            
            # Initialize LLM adapter
            llm_config = LLMConfig(
                mode=self.config.llm_mode,
                model=self.config.llm_model,
                temperature=self.config.llm_temperature,
                api_key=self.config.llm_api_key
            )
            self.llm_adapter = LLMAdapterFactory.create_adapter(
                llm_config, seed=self.config.seed
            )
            print(f"Initialized LLM adapter: {self.config.llm_mode.value}")
            
            # Initialize world
            self.world = World(seed=self.config.seed)
            self.world.initialize_world(
                num_agents=self.config.num_agents,
                seed=self.config.seed
            )
            print(f"Initialized world with {len(self.world.agents)} agents")
            
            # Initialize scheduler
            scheduler_config = SchedulerConfig(
                tick_duration_ms=self.config.tick_duration_ms,
                max_ticks=self.config.max_ticks,
                agents_per_tick=self.config.agents_per_tick,
                interactions_per_tick=self.config.interactions_per_tick
            )
            self.scheduler = SimulationScheduler(self.world, scheduler_config)
            
            # Set up callbacks
            self.scheduler.add_tick_callback(self._on_tick)
            self.scheduler.add_completion_callback(self._on_completion)
            
            # Create snapshot directory
            os.makedirs(self.config.snapshot_directory, exist_ok=True)
            
            # Load external stimuli if provided
            if self.config.stimuli_file and os.path.exists(self.config.stimuli_file):
                await self._load_stimuli()
            
            self.state = SimulationState.READY
            print("Simulation engine initialized successfully")
            return True
            
        except Exception as e:
            self.state = SimulationState.ERROR
            print(f"Failed to initialize simulation engine: {e}")
            await self._handle_error(str(e))
            return False
    
    async def run_simulation(self, max_ticks: Optional[int] = None) -> bool:
        """Run the complete simulation."""
        if self.state != SimulationState.READY:
            print("Simulation not ready. Call initialize() first.")
            return False
        
        try:
            self.state = SimulationState.RUNNING
            self.start_time = time.time()
            
            print(f"Starting simulation with {len(self.world.agents)} agents...")
            print(f"Target ticks: {max_ticks or self.config.max_ticks}")
            
            # Run simulation
            tick_results = await self.scheduler.run_simulation(max_ticks)
            
            self.end_time = time.time()
            duration = self.end_time - self.start_time
            
            print(f"Simulation completed in {duration:.2f} seconds")
            print(f"Processed {len(tick_results)} ticks")
            print(f"Average tick duration: {sum(r.duration_ms for r in tick_results) / len(tick_results):.2f}ms")
            
            # Generate final summary
            await self._generate_final_summary()
            
            self.state = SimulationState.STOPPED
            return True
            
        except Exception as e:
            self.state = SimulationState.ERROR
            print(f"Simulation failed: {e}")
            await self._handle_error(str(e))
            return False
    
    async def pause_simulation(self):
        """Pause the running simulation."""
        if self.scheduler and self.state == SimulationState.RUNNING:
            self.scheduler.pause()
            self.state = SimulationState.PAUSED
            print("Simulation paused")
    
    async def resume_simulation(self):
        """Resume the paused simulation."""
        if self.scheduler and self.state == SimulationState.PAUSED:
            self.scheduler.resume()
            self.state = SimulationState.RUNNING
            print("Simulation resumed")
    
    async def step_simulation(self):
        """Step the simulation forward one tick."""
        if self.scheduler and self.state == SimulationState.PAUSED:
            self.scheduler.step()
            self.state = SimulationState.RUNNING
            print("Simulation stepping forward one tick")
    
    async def stop_simulation(self):
        """Stop the simulation."""
        if self.scheduler:
            self.scheduler.stop()
            self.state = SimulationState.STOPPED
            print("Simulation stopped")
    
    async def take_snapshot(self, name: Optional[str] = None) -> str:
        """Take a snapshot of the current simulation state."""
        if not self.world:
            raise RuntimeError("World not initialized")
        
        timestamp = int(time.time())
        if not name:
            name = f"snapshot_{timestamp}"
        
        snapshot = {
            "name": name,
            "timestamp": timestamp,
            "tick": self.world.current_tick,
            "config": self.config.to_dict(),
            "world_summary": self.world.get_world_summary(),
            "performance_stats": self.scheduler.get_performance_stats() if self.scheduler else {},
            "agent_network": self.world.get_agent_network_data(),
            "cultural_timeline": self.world.get_cultural_timeline()
        }
        
        # Save to file
        snapshot_file = os.path.join(self.config.snapshot_directory, f"{name}.json")
        with open(snapshot_file, 'w') as f:
            json.dump(snapshot, f, indent=2)
        
        self.snapshots.append(snapshot)
        print(f"Snapshot saved: {snapshot_file}")
        
        return snapshot_file
    
    async def load_snapshot(self, snapshot_file: str) -> bool:
        """Load a snapshot and restore simulation state."""
        try:
            with open(snapshot_file, 'r') as f:
                snapshot = json.load(f)
            
            # Restore configuration
            config_dict = snapshot.get("config", {})
            self.config = SimulationConfig(**config_dict)
            
            # Reinitialize systems
            await self.initialize()
            
            # Restore world state
            world_summary = snapshot.get("world_summary", {})
            if world_summary:
                self.world.current_tick = world_summary.get("current_tick", 0)
                self.world.state = WorldState.RUNNING
            
            print(f"Snapshot loaded: {snapshot_file}")
            return True
            
        except Exception as e:
            print(f"Failed to load snapshot: {e}")
            return False
    
    async def get_simulation_status(self) -> Dict[str, Any]:
        """Get current simulation status."""
        status = {
            "state": self.state.value,
            "current_tick": self.world.current_tick if self.world else 0,
            "start_time": self.start_time,
            "end_time": self.end_time,
            "duration": (self.end_time - self.start_time) if self.start_time and self.end_time else None
        }
        
        if self.world:
            status["world_summary"] = self.world.get_world_summary()
        
        if self.scheduler:
            status["scheduler_stats"] = self.scheduler.get_performance_stats()
        
        return status
    
    async def get_agent_data(self, agent_id: Optional[str] = None) -> Dict[str, Any]:
        """Get agent data for visualization."""
        if not self.world:
            return {}
        
        if agent_id:
            agent = self.world.agents.get(agent_id)
            return agent.to_dict() if agent else {}
        else:
            return {
                "agents": [agent.to_dict() for agent in self.world.agents.values()],
                "total_count": len(self.world.agents)
            }
    
    async def get_cultural_data(self) -> Dict[str, Any]:
        """Get cultural data for visualization."""
        if not self.world:
            return {}
        
        return {
            "myths": [myth.to_dict() for myth in self.world.culture.myths.values()],
            "norms": [norm.to_dict() for norm in self.world.culture.active_norms.values()],
            "slang": [slang.to_dict() for slang in self.world.culture.slang_registry.values()],
            "timeline": self.world.get_cultural_timeline()
        }
    
    async def get_economic_data(self) -> Dict[str, Any]:
        """Get economic data for visualization."""
        if not self.world:
            return {}
        
        return self.world.economy.get_economy_summary()
    
    async def get_network_data(self) -> Dict[str, Any]:
        """Get network data for visualization."""
        if not self.world:
            return {}
        
        return self.world.get_agent_network_data()
    
    def add_tick_callback(self, callback: Callable[[int], None]):
        """Add callback to be called after each tick."""
        self.tick_callbacks.append(callback)
    
    def add_completion_callback(self, callback: Callable[[], None]):
        """Add callback to be called when simulation completes."""
        self.completion_callbacks.append(callback)
    
    def add_error_callback(self, callback: Callable[[str], None]):
        """Add callback to be called when an error occurs."""
        self.error_callbacks.append(callback)
    
    async def _on_tick(self, tick: int):
        """Handle tick callback."""
        # Call registered callbacks
        for callback in self.tick_callbacks:
            try:
                callback(tick)
            except Exception as e:
                print(f"Error in tick callback: {e}")
        
        # Take snapshots at configured intervals
        if (self.config.snapshot_frequency > 0 and 
            tick % self.config.snapshot_frequency == 0 and 
            tick > 0):
            await self.take_snapshot(f"auto_snapshot_tick_{tick}")
    
    async def _on_completion(self):
        """Handle completion callback."""
        # Take final snapshot
        await self.take_snapshot("final_snapshot")
        
        # Call registered callbacks
        for callback in self.completion_callbacks:
            try:
                callback()
            except Exception as e:
                print(f"Error in completion callback: {e}")
    
    async def _handle_error(self, error: str):
        """Handle simulation error."""
        print(f"Simulation error: {error}")
        
        # Call registered error callbacks
        for callback in self.error_callbacks:
            try:
                callback(error)
            except Exception as e:
                print(f"Error in error callback: {e}")
        
        self.state = SimulationState.ERROR
    
    async def _load_stimuli(self):
        """Load external stimuli from file."""
        try:
            with open(self.config.stimuli_file, 'r') as f:
                stimuli_data = json.load(f)
            
            if isinstance(stimuli_data, list):
                # Add stimuli as events
                events = self.world.event_system.add_external_stimuli(
                    stimuli_data, self.world.current_tick
                )
                print(f"Loaded {len(events)} external stimuli events")
            else:
                print("Invalid stimuli file format")
                
        except Exception as e:
            print(f"Failed to load stimuli: {e}")
    
    async def _generate_final_summary(self):
        """Generate final simulation summary."""
        if not self.world:
            return
        
        summary = {
            "simulation_config": self.config.to_dict(),
            "final_stats": self.world.stats,
            "performance": self.scheduler.get_performance_stats() if self.scheduler else {},
            "duration": self.end_time - self.start_time if self.start_time and self.end_time else 0,
            "total_ticks": self.world.current_tick,
            "snapshots_taken": len(self.snapshots)
        }
        
        # Save summary
        summary_file = os.path.join(self.config.snapshot_directory, "final_summary.json")
        with open(summary_file, 'w') as f:
            json.dump(summary, f, indent=2)
        
        print(f"Final summary saved: {summary_file}")
        
        # Print key statistics
        print("\n=== SIMULATION SUMMARY ===")
        print(f"Total ticks: {self.world.current_tick}")
        print(f"Duration: {summary['duration']:.2f} seconds")
        print(f"Final agents: {len(self.world.agents)}")
        print(f"Final factions: {len(self.world.factions)}")
        print(f"Total myths: {len(self.world.culture.myths)}")
        print(f"Active norms: {len(self.world.culture.active_norms)}")
        print(f"Total trades: {len(self.world.economy.trade_history)}")
        print(f"Gini coefficient: {self.world.economy.gini_coefficient:.3f}")
        print("========================\n")
    
    def cleanup(self):
        """Clean up simulation resources."""
        if self.world:
            self.world.cleanup()
        
        self.state = SimulationState.STOPPED
        print("Simulation engine cleaned up")
