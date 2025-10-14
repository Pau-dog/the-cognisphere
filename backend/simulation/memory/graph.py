"""
Graph-based memory system for The Cognisphere.

This module implements the graph database functionality for storing and retrieving
agent memories, relationships, and knowledge structures.
"""

import uuid
import json
from typing import Dict, List, Optional, Set, Tuple, Any
from dataclasses import dataclass, field
from enum import Enum
from datetime import datetime, timedelta
import networkx as nx
from collections import defaultdict
import os


class MemoryType(Enum):
    """Types of memories in the graph."""
    EPISODIC = "episodic"  # Events and experiences
    SEMANTIC = "semantic"  # Facts and knowledge
    SOCIAL = "social"      # Relationships and interactions
    CULTURAL = "cultural"  # Myths, norms, traditions
    EMOTIONAL = "emotional"  # Emotional experiences
    PROCEDURAL = "procedural"  # Skills and procedures


class RelationshipType(Enum):
    """Types of relationships in the memory graph."""
    KNOWS = "knows"
    TRUSTS = "trusts"
    LIKES = "likes"
    DISLIKES = "dislikes"
    ALLIES_WITH = "allies_with"
    ENEMIES_WITH = "enemies_with"
    TRADED_WITH = "traded_with"
    BETRAYED = "betrayed"
    CREATED = "created"
    REFERENCES = "references"
    CONTRADICTS = "contradicts"
    DERIVES_FROM = "derives_from"
    PART_OF = "part_of"
    CAUSES = "causes"
    LEADS_TO = "leads_to"


@dataclass
class MemoryNode:
    """Represents a node in the memory graph."""
    node_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    node_type: str = "memory"  # memory, agent, concept, event, myth, norm
    memory_type: MemoryType = MemoryType.EPISODIC
    content: str = ""
    metadata: Dict[str, Any] = field(default_factory=dict)
    importance: float = 0.5  # 0.0 to 1.0
    accessibility: float = 0.5  # 0.0 to 1.0 (how easily recalled)
    valence: float = 0.0  # -1.0 to 1.0 (emotional valence)
    arousal: float = 0.0  # 0.0 to 1.0 (emotional arousal)
    created_at: datetime = field(default_factory=datetime.now)
    last_accessed: datetime = field(default_factory=datetime.now)
    access_count: int = 0
    decay_rate: float = 0.01  # How fast this memory decays
    consolidation_strength: float = 0.0  # How well consolidated this memory is
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert node to dictionary for serialization."""
        return {
            "node_id": self.node_id,
            "node_type": self.node_type,
            "memory_type": self.memory_type.value,
            "content": self.content,
            "metadata": self.metadata,
            "importance": self.importance,
            "accessibility": self.accessibility,
            "valence": self.valence,
            "arousal": self.arousal,
            "created_at": self.created_at.isoformat(),
            "last_accessed": self.last_accessed.isoformat(),
            "access_count": self.access_count,
            "decay_rate": self.decay_rate,
            "consolidation_strength": self.consolidation_strength
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'MemoryNode':
        """Create node from dictionary."""
        node = cls()
        node.node_id = data["node_id"]
        node.node_type = data["node_type"]
        node.memory_type = MemoryType(data["memory_type"])
        node.content = data["content"]
        node.metadata = data["metadata"]
        node.importance = data["importance"]
        node.accessibility = data["accessibility"]
        node.valence = data["valence"]
        node.arousal = data["arousal"]
        node.created_at = datetime.fromisoformat(data["created_at"])
        node.last_accessed = datetime.fromisoformat(data["last_accessed"])
        node.access_count = data["access_count"]
        node.decay_rate = data["decay_rate"]
        node.consolidation_strength = data["consolidation_strength"]
        return node
    
    def access(self) -> None:
        """Record access to this memory."""
        self.last_accessed = datetime.now()
        self.access_count += 1
        # Strengthen memory through access (spaced repetition effect)
        self.consolidation_strength = min(1.0, self.consolidation_strength + 0.05)
    
    def decay(self, time_delta: timedelta) -> None:
        """Apply memory decay over time."""
        decay_amount = self.decay_rate * time_delta.total_seconds() / 3600  # Decay per hour
        self.accessibility = max(0.0, self.accessibility - decay_amount)
        self.consolidation_strength = max(0.0, self.consolidation_strength - decay_amount * 0.5)


@dataclass
class MemoryEdge:
    """Represents an edge in the memory graph."""
    edge_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    source_id: str = ""
    target_id: str = ""
    relationship_type: RelationshipType = RelationshipType.KNOWS
    weight: float = 1.0  # Strength of the relationship
    metadata: Dict[str, Any] = field(default_factory=dict)
    created_at: datetime = field(default_factory=datetime.now)
    last_accessed: datetime = field(default_factory=datetime.now)
    access_count: int = 0
    decay_rate: float = 0.005  # How fast this relationship decays
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert edge to dictionary for serialization."""
        return {
            "edge_id": self.edge_id,
            "source_id": self.source_id,
            "target_id": self.target_id,
            "relationship_type": self.relationship_type.value,
            "weight": self.weight,
            "metadata": self.metadata,
            "created_at": self.created_at.isoformat(),
            "last_accessed": self.last_accessed.isoformat(),
            "access_count": self.access_count,
            "decay_rate": self.decay_rate
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'MemoryEdge':
        """Create edge from dictionary."""
        edge = cls()
        edge.edge_id = data["edge_id"]
        edge.source_id = data["source_id"]
        edge.target_id = data["target_id"]
        edge.relationship_type = RelationshipType(data["relationship_type"])
        edge.weight = data["weight"]
        edge.metadata = data["metadata"]
        edge.created_at = datetime.fromisoformat(data["created_at"])
        edge.last_accessed = datetime.fromisoformat(data["last_accessed"])
        edge.access_count = data["access_count"]
        edge.decay_rate = data["decay_rate"]
        return edge
    
    def access(self) -> None:
        """Record access to this relationship."""
        self.last_accessed = datetime.now()
        self.access_count += 1
        # Strengthen relationship through access
        self.weight = min(2.0, self.weight + 0.02)
    
    def decay(self, time_delta: timedelta) -> None:
        """Apply relationship decay over time."""
        decay_amount = self.decay_rate * time_delta.total_seconds() / 3600
        self.weight = max(0.0, self.weight - decay_amount)


class MemoryGraph:
    """Graph-based memory system using NetworkX."""
    
    def __init__(self, graph_id: str = None):
        self.graph_id = graph_id or str(uuid.uuid4())
        self.graph = nx.MultiDiGraph()
        self.nodes: Dict[str, MemoryNode] = {}
        self.edges: Dict[str, MemoryEdge] = {}
        self.node_index: Dict[str, Set[str]] = defaultdict(set)  # content -> node_ids
        self.last_cleanup: datetime = datetime.now()
        
    def add_node(self, node: MemoryNode) -> str:
        """Add a memory node to the graph."""
        self.graph.add_node(node.node_id, **node.to_dict())
        self.nodes[node.node_id] = node
        
        # Index by content for search
        words = node.content.lower().split()
        for word in words:
            self.node_index[word].add(node.node_id)
        
        return node.node_id
    
    def add_edge(self, edge: MemoryEdge) -> str:
        """Add a memory edge to the graph."""
        if edge.source_id not in self.nodes or edge.target_id not in self.nodes:
            raise ValueError("Cannot create edge between non-existent nodes")
        
        self.graph.add_edge(
            edge.source_id, 
            edge.target_id, 
            key=edge.edge_id,
            **edge.to_dict()
        )
        self.edges[edge.edge_id] = edge
        return edge.edge_id
    
    def get_node(self, node_id: str) -> Optional[MemoryNode]:
        """Get a memory node by ID."""
        return self.nodes.get(node_id)
    
    def get_edge(self, edge_id: str) -> Optional[MemoryEdge]:
        """Get a memory edge by ID."""
        return self.edges.get(edge_id)
    
    def search_nodes(self, query: str, limit: int = 10) -> List[MemoryNode]:
        """Search for nodes by content."""
        query_words = set(query.lower().split())
        scored_nodes = []
        
        for node_id, node in self.nodes.items():
            node_words = set(node.content.lower().split())
            overlap = len(query_words & node_words)
            if overlap > 0:
                score = overlap / len(query_words)
                scored_nodes.append((score, node))
        
        # Sort by relevance score
        scored_nodes.sort(key=lambda x: x[0], reverse=True)
        return [node for _, node in scored_nodes[:limit]]
    
    def get_neighbors(self, node_id: str, relationship_type: RelationshipType = None) -> List[Tuple[MemoryNode, MemoryEdge]]:
        """Get neighboring nodes and edges."""
        if node_id not in self.nodes:
            return []
        
        neighbors = []
        for source, target, key, edge_data in self.graph.edges(node_id, data=True, keys=True):
            edge = self.edges.get(key)
            if edge and (relationship_type is None or edge.relationship_type == relationship_type):
                neighbor_node = self.nodes.get(target)
                if neighbor_node:
                    neighbors.append((neighbor_node, edge))
        
        return neighbors
    
    def get_shortest_path(self, source_id: str, target_id: str, 
                         relationship_types: List[RelationshipType] = None) -> List[str]:
        """Get shortest path between two nodes."""
        if source_id not in self.nodes or target_id not in self.nodes:
            return []
        
        # Create filtered graph if relationship types specified
        if relationship_types:
            filtered_graph = nx.MultiDiGraph()
            for edge_id, edge in self.edges.items():
                if edge.relationship_type in relationship_types:
                    filtered_graph.add_edge(edge.source_id, edge.target_id)
            
            try:
                path = nx.shortest_path(filtered_graph, source_id, target_id)
                return path
            except nx.NetworkXNoPath:
                return []
        else:
            try:
                path = nx.shortest_path(self.graph, source_id, target_id)
                return path
            except nx.NetworkXNoPath:
                return []
    
    def get_connected_components(self) -> List[Set[str]]:
        """Get connected components in the graph."""
        return list(nx.weakly_connected_components(self.graph))
    
    def get_node_centrality(self, node_id: str) -> float:
        """Calculate centrality score for a node."""
        if node_id not in self.nodes:
            return 0.0
        
        try:
            # Use betweenness centrality
            centrality = nx.betweenness_centrality(self.graph)
            return centrality.get(node_id, 0.0)
        except Exception:
            return 0.0
    
    def consolidate_memories(self, time_delta: timedelta) -> None:
        """Consolidate memories over time."""
        for node in self.nodes.values():
            # Apply decay
            node.decay(time_delta)
            
            # Consolidate frequently accessed memories
            if node.access_count > 5 and node.consolidation_strength < 0.8:
                node.consolidation_strength = min(1.0, node.consolidation_strength + 0.1)
        
        for edge in self.edges.values():
            # Apply decay to relationships
            edge.decay(time_delta)
    
    def cleanup_weak_memories(self, threshold: float = 0.1) -> int:
        """Remove memories below the threshold."""
        nodes_to_remove = []
        edges_to_remove = []
        
        # Find weak nodes
        for node_id, node in self.nodes.items():
            if node.accessibility < threshold:
                nodes_to_remove.append(node_id)
        
        # Find weak edges
        for edge_id, edge in self.edges.items():
            if edge.weight < threshold:
                edges_to_remove.append(edge_id)
        
        # Remove weak nodes and edges
        for node_id in nodes_to_remove:
            self.remove_node(node_id)
        
        for edge_id in edges_to_remove:
            self.remove_edge(edge_id)
        
        return len(nodes_to_remove) + len(edges_to_remove)
    
    def remove_node(self, node_id: str) -> None:
        """Remove a node and all its edges."""
        if node_id not in self.nodes:
            return
        
        # Remove all edges connected to this node
        edges_to_remove = []
        for edge_id, edge in self.edges.items():
            if edge.source_id == node_id or edge.target_id == node_id:
                edges_to_remove.append(edge_id)
        
        for edge_id in edges_to_remove:
            self.remove_edge(edge_id)
        
        # Remove node from graph
        self.graph.remove_node(node_id)
        
        # Remove from indexes
        node = self.nodes[node_id]
        words = node.content.lower().split()
        for word in words:
            self.node_index[word].discard(node_id)
        
        # Remove from nodes dict
        del self.nodes[node_id]
    
    def remove_edge(self, edge_id: str) -> None:
        """Remove an edge from the graph."""
        if edge_id not in self.edges:
            return
        
        edge = self.edges[edge_id]
        
        # Remove from graph
        if self.graph.has_edge(edge.source_id, edge.target_id, edge_id):
            self.graph.remove_edge(edge.source_id, edge.target_id, edge_id)
        
        # Remove from edges dict
        del self.edges[edge_id]
    
    def create_episodic_memory(self, content: str, importance: float = 0.5, 
                              valence: float = 0.0, arousal: float = 0.0,
                              metadata: Dict[str, Any] = None) -> str:
        """Create an episodic memory."""
        node = MemoryNode(
            memory_type=MemoryType.EPISODIC,
            content=content,
            importance=importance,
            valence=valence,
            arousal=arousal,
            metadata=metadata or {}
        )
        return self.add_node(node)
    
    def create_semantic_memory(self, content: str, importance: float = 0.7,
                              metadata: Dict[str, Any] = None) -> str:
        """Create a semantic memory."""
        node = MemoryNode(
            memory_type=MemoryType.SEMANTIC,
            content=content,
            importance=importance,
            accessibility=0.8,  # Semantic memories are more accessible
            metadata=metadata or {}
        )
        return self.add_node(node)
    
    def create_social_memory(self, content: str, other_agent_id: str,
                           relationship_type: RelationshipType,
                           valence: float = 0.0, metadata: Dict[str, Any] = None) -> str:
        """Create a social memory and relationship."""
        # Create social memory node
        node = MemoryNode(
            memory_type=MemoryType.SOCIAL,
            content=content,
            importance=0.6,
            valence=valence,
            metadata=metadata or {}
        )
        node_id = self.add_node(node)
        
        # Create relationship edge if other agent exists
        if other_agent_id in self.nodes:
            edge = MemoryEdge(
                source_id=node_id,
                target_id=other_agent_id,
                relationship_type=relationship_type,
                weight=1.0
            )
            self.add_edge(edge)
        
        return node_id
    
    def create_relationship(self, source_id: str, target_id: str,
                          relationship_type: RelationshipType,
                          weight: float = 1.0, metadata: Dict[str, Any] = None) -> str:
        """Create a relationship between two nodes."""
        edge = MemoryEdge(
            source_id=source_id,
            target_id=target_id,
            relationship_type=relationship_type,
            weight=weight,
            metadata=metadata or {}
        )
        return self.add_edge(edge)
    
    def retrieve_memories(self, query: str, memory_types: List[MemoryType] = None,
                         limit: int = 10) -> List[MemoryNode]:
        """Retrieve memories based on query and type filter."""
        candidates = self.search_nodes(query, limit * 2)
        
        # Filter by memory type if specified
        if memory_types:
            candidates = [node for node in candidates if node.memory_type in memory_types]
        
        # Sort by accessibility and importance
        candidates.sort(key=lambda x: x.accessibility * x.importance, reverse=True)
        
        # Access the retrieved memories (for spaced repetition)
        for node in candidates[:limit]:
            node.access()
        
        return candidates[:limit]
    
    def get_memory_statistics(self) -> Dict[str, Any]:
        """Get statistics about the memory graph."""
        memory_type_counts = defaultdict(int)
        for node in self.nodes.values():
            memory_type_counts[node.memory_type.value] += 1
        
        relationship_type_counts = defaultdict(int)
        for edge in self.edges.values():
            relationship_type_counts[edge.relationship_type.value] += 1
        
        return {
            "total_nodes": len(self.nodes),
            "total_edges": len(self.edges),
            "memory_type_distribution": dict(memory_type_counts),
            "relationship_type_distribution": dict(relationship_type_counts),
            "connected_components": len(self.get_connected_components()),
            "average_accessibility": sum(node.accessibility for node in self.nodes.values()) / max(1, len(self.nodes)),
            "average_importance": sum(node.importance for node in self.nodes.values()) / max(1, len(self.nodes)),
            "graph_density": nx.density(self.graph) if self.nodes else 0.0
        }
    
    def save_to_file(self, filename: str) -> None:
        """Save the memory graph to a file."""
        data = {
            "graph_id": self.graph_id,
            "nodes": {node_id: node.to_dict() for node_id, node in self.nodes.items()},
            "edges": {edge_id: edge.to_dict() for edge_id, edge in self.edges.items()},
            "last_cleanup": self.last_cleanup.isoformat()
        }
        
        with open(filename, 'w') as f:
            json.dump(data, f, indent=2)
    
    def load_from_file(self, filename: str) -> None:
        """Load the memory graph from a file."""
        if not os.path.exists(filename):
            return
        
        with open(filename, 'r') as f:
            data = json.load(f)
        
        self.graph_id = data["graph_id"]
        self.last_cleanup = datetime.fromisoformat(data["last_cleanup"])
        
        # Load nodes
        for node_id, node_data in data["nodes"].items():
            node = MemoryNode.from_dict(node_data)
            self.nodes[node_id] = node
            self.graph.add_node(node_id, **node_data)
        
        # Load edges
        for edge_id, edge_data in data["edges"].items():
            edge = MemoryEdge.from_dict(edge_data)
            self.edges[edge_id] = edge
            self.graph.add_edge(edge.source_id, edge.target_id, key=edge_id, **edge_data)
        
        # Rebuild index
        self.node_index = defaultdict(set)
        for node_id, node in self.nodes.items():
            words = node.content.lower().split()
            for word in words:
                self.node_index[word].add(node_id)
