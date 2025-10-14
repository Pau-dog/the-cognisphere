# The Cognisphere Customization Guide

## Agent Personality Customization

### File: `backend/simulation/agents.py`

#### 1. Modify Default Personality Ranges

```python
@classmethod
def generate_random(cls, seed: Optional[int] = None) -> "AgentPersonality":
    """Generate random personality with custom biases."""
    if seed:
        random.seed(seed)
    
    # Customize these ranges to create different agent types
    return AgentPersonality(
        openness=random.uniform(0.3, 0.9),      # Higher = more creative/curious
        conscientiousness=random.uniform(0.2, 0.8), # Higher = more organized/diligent
        extraversion=random.uniform(0.1, 0.9),      # Higher = more social/outgoing
        agreeableness=random.uniform(0.2, 0.8),     # Higher = more cooperative/trusting
        neuroticism=random.uniform(0.1, 0.7)        # Higher = more anxious/emotional
    )
```

#### 2. Create Specialized Agent Types

```python
@classmethod
def create_entrepreneur(cls) -> "AgentPersonality":
    """High openness, conscientiousness, extraversion."""
    return AgentPersonality(
        openness=0.8,
        conscientiousness=0.7,
        extraversion=0.9,
        agreeableness=0.4,
        neuroticism=0.3
    )

@classmethod
def create_philosopher(cls) -> "AgentPersonality":
    """High openness, low extraversion."""
    return AgentPersonality(
        openness=0.9,
        conscientiousness=0.6,
        extraversion=0.2,
        agreeableness=0.7,
        neuroticism=0.4
    )

@classmethod
def create_leader(cls) -> "AgentPersonality":
    """High extraversion, conscientiousness, agreeableness."""
    return AgentPersonality(
        openness=0.6,
        conscientiousness=0.8,
        extraversion=0.9,
        agreeableness=0.8,
        neuroticism=0.2
    )
```

## Cultural Evolution Customization

### File: `backend/simulation/culture.py`

#### 1. Adjust Language Drift Frequency

```python
# In Culture class __init__
self.language_drift_frequency = 3  # Every 3 ticks (was 5)
self.slang_mutation_rate = 0.15    # 15% chance (was 10%)
self.myth_canonization_threshold = 0.6  # Lower threshold (was 0.7)
```

#### 2. Customize Myth Themes

```python
def generate_myth_templates(self) -> List[Dict[str, Any]]:
    """Add your own myth templates."""
    templates = [
        # Add new themes
        {
            "theme": "technology",
            "title_template": "The {invention} of {creator}",
            "content_template": "When {creator} built the first {invention}, it changed everything...",
            "inventions": ["machine", "device", "system", "tool"],
            "creators": ["the Engineer", "the Inventor", "the Builder"]
        },
        {
            "theme": "mystery",
            "title_template": "The {mystery} of {place}",
            "content_template": "In the depths of {place}, something {mystery} awaits...",
            "mysteries": ["secret", "enigma", "puzzle", "riddle"],
            "places": ["the Ancient Ruins", "the Lost City", "the Hidden Temple"]
        }
    ]
    return templates
```

#### 3. Adjust Norm Voting Thresholds

```python
def vote_on_norm(self, norm_id: str, agent_id: str, vote: bool):
    """Customize voting requirements."""
    if norm_id in self.proposed_norms:
        norm = self.proposed_norms[norm_id]
        if vote:
            norm.votes_for += 1
        else:
            norm.votes_against += 1

        total_votes = norm.votes_for + norm.votes_against
        # Customize these thresholds
        if total_votes >= 5:  # Lower minimum votes (was 10)
            approval_rate = norm.votes_for / total_votes
            if approval_rate >= 0.5:  # Lower approval threshold (was 0.6)
                norm.status = "active"
                self.active_norms[norm_id] = norm
```

## Economic System Customization

### File: `backend/simulation/economy.py`

#### 1. Add New Resource Types

```python
class ResourceType(Enum):
    """Add new resource types."""
    FOOD = "food"
    ENERGY = "energy"
    ARTIFACTS = "artifacts"
    INFLUENCE = "influence"
    KNOWLEDGE = "knowledge"      # New resource
    REPUTATION = "reputation"    # New resource
    TIME = "time"               # New resource
```

#### 2. Customize Trade Mechanics

```python
def calculate_utility(self, agent_resources: Dict[str, float],
                     resource_values: Dict[str, float]) -> float:
    """Customize utility calculation."""
    # Add personality-based modifiers
    personality_modifiers = {
        "food": 1.0 + (agent.personality.conscientiousness * 0.2),
        "energy": 1.0 + (agent.personality.extraversion * 0.3),
        "artifacts": 1.0 + (agent.personality.openness * 0.4),
        "influence": 1.0 + (agent.personality.extraversion * 0.5),
    }
    
    # Apply modifiers to utility calculation
    utility = 1.0
    for resource, change in net_change.items():
        if change != 0:
            new_amount = agent_resources.get(resource, 0) + change
            if new_amount > 0:
                weight = resource_values.get(resource, 1.0)
                modifier = personality_modifiers.get(resource, 1.0)
                utility *= (new_amount ** (weight * 0.3 * modifier))
    
    return utility
```

#### 3. Adjust Market Dynamics

```python
def update_prices(self, tick: int, supply_demand: Dict[str, Tuple[float, float]]):
    """Customize price volatility."""
    for resource_name, (supply, demand) in supply_demand.items():
        if resource_name in self.resources:
            resource = self.resources[resource_name]

            # Customize volatility
            if supply > 0:
                scarcity = demand / supply
                # More volatile pricing (was 0.5 + scarcity * 2.0)
                resource.scarcity_modifier = 0.3 + (scarcity * 3.0)
            else:
                resource.scarcity_modifier = 15.0  # Higher extreme scarcity (was 10.0)
```

## Dashboard Visualization Customization

### File: `frontend/src/pages/Network.tsx`

#### 1. Customize Node Colors by Agent Type

```typescript
const getNodeColor = (agent: Agent) => {
  // Color based on personality
  if (agent.personality.extraversion > 0.7) return '#ff6b6b'; // Red for extroverts
  if (agent.personality.openness > 0.7) return '#4ecdc4';    // Teal for creative
  if (agent.personality.agreeableness > 0.7) return '#45b7d1'; // Blue for cooperative
  return '#96ceb4'; // Default green
};
```

#### 2. Add Custom Metrics

```typescript
const getNodeSize = (agent: Agent) => {
  // Size based on influence
  const baseSize = 20;
  const influenceMultiplier = agent.influence / 100;
  return baseSize + (influenceMultiplier * 30);
};
```

### File: `frontend/src/pages/Culture.tsx`

#### 1. Customize Myth Display

```typescript
const renderMythCard = (myth: Myth) => (
  <div className="myth-card" style={{
    borderLeft: `4px solid ${getThemeColor(myth.theme)}`,
    background: `linear-gradient(135deg, ${getThemeColor(myth.theme)}20, transparent)`
  }}>
    <h3>{myth.title}</h3>
    <p className="theme-badge">{myth.theme}</p>
    <p className="popularity">Popularity: {myth.popularity.toFixed(2)}</p>
  </div>
);
```

## Quick Customization Examples

### 1. Make Agents More Creative

```python
# In agents.py, modify generate_random()
openness=random.uniform(0.6, 1.0),  # Higher creativity range
```

### 2. Make Trade More Volatile

```python
# In economy.py, modify update_prices()
resource.scarcity_modifier = 0.2 + (scarcity * 4.0)  # More extreme pricing
```

### 3. Faster Cultural Evolution

```python
# In culture.py, modify Culture.__init__()
self.language_drift_frequency = 2  # Every 2 ticks
self.slang_mutation_rate = 0.2     # 20% mutation rate
```

### 4. More Cooperative Agents

```python
# In agents.py, modify generate_random()
agreeableness=random.uniform(0.6, 1.0),  # Higher cooperation
```

## Testing Your Customizations

```bash
# Run with custom parameters
python3 scripts/seed_and_run.py --agents 50 --ticks 100 --seed 42

# Watch the dashboard at http://localhost:5173
# Observe how your changes affect agent behavior
```

## Advanced Customizations

### 1. Add New Agent Capabilities

```python
# In agents.py, add new methods to Agent class
def create_institution(self, tick: int) -> Optional[Institution]:
    """Agents can now create institutions."""
    if self.personality.extraversion > 0.8 and self.influence > 50:
        return Institution(
            name=f"{self.name}'s Council",
            founder_id=self.agent_id,
            tick_founded=tick
        )
    return None
```

### 2. Custom Event Systems

```python
# Create new event types
class CustomEvent(SimulationEvent):
    """Add your own event types."""
    def __init__(self, event_type: str, description: str, **kwargs):
        super().__init__(event_type, description, **kwargs)
        self.custom_data = kwargs.get('custom_data', {})
```

This guide gives you complete control over every aspect of The Cognisphere's behavior!
