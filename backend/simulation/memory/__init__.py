"""
Memory systems for agents including graph-based memory and vector storage.

This module provides both graph-based memory (using Neo4j or NetworkX)
and vector-based semantic memory for agent reasoning and retrieval.
"""

from .graph import MemoryGraph, MemoryNode, MemoryEdge
from .vector import VectorMemory, FAISSVectorStore, VectorMemorySystem
from .schemas import MemoryEvent, MemoryConcept, MemoryRelationship

# Create a simple AgentMemory class for compatibility
class AgentMemory:
    """Simple agent memory for compatibility."""
    def __init__(self, agent_id: str):
        self.agent_id = agent_id
        self.graph_memory = MemoryGraph()
        self.vector_memory = FAISSVectorStore()

__all__ = [
    "MemoryGraph",
    "MemoryNode", 
    "MemoryEdge",
    "VectorMemory",
    "FAISSVectorStore",
    "VectorMemorySystem",
    "MemoryEvent",
    "MemoryConcept",
    "MemoryRelationship",
    "AgentMemory"
]
