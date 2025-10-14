# The Cognisphere Implementation Guide

## Quick Start Implementation

### 1. Apply Agent Customizations

```bash
# Copy the custom agent personalities to your agents.py
cp AGENT_CUSTOMIZATIONS.py backend/simulation/agent_customizations.py

# Edit backend/simulation/agents.py to use custom personalities
```

**Add to `backend/simulation/agents.py`:**

```python
# At the top, import your customizations
from .agent_customizations import SpecializedPersonalities, generate_biased_personality

# Modify the Agent class initialization
class Agent:
    def __init__(self, agent_id: str, personality_type: str = "balanced"):
        # ... existing code ...
        
        # Use custom personality generation
        if personality_type == "entrepreneur":
            self.personality = SpecializedPersonalities.create_entrepreneur()
        elif personality_type == "philosopher":
            self.personality = SpecializedPersonalities.create_philosopher()
        elif personality_type == "leader":
            self.personality = SpecializedPersonalities.create_leader()
        else:
            self.personality = generate_biased_personality(personality_type)
```

### 2. Apply Culture Customizations

```bash
# Copy culture customizations
cp CULTURE_CUSTOMIZATIONS.py backend/simulation/culture_customizations.py
```

**Add to `backend/simulation/culture.py`:**

```python
# Import customizations
from .culture_customizations import FastCulture, CreativeCulture, CustomMythThemes

# Modify the Culture class
class Culture:
    def __init__(self, culture_type: str = "standard"):
        if culture_type == "fast":
            # Use FastCulture parameters
            self.language_drift_frequency = 2
            self.slang_mutation_rate = 0.25
            self.myth_canonization_threshold = 0.5
        elif culture_type == "creative":
            # Use CreativeCulture parameters
            self.language_drift_frequency = 3
            self.slang_mutation_rate = 0.2
            self.myth_canonization_threshold = 0.6
        else:
            # Default parameters
            self.language_drift_frequency = 5
            self.slang_mutation_rate = 0.1
            self.myth_canonization_threshold = 0.7
```

### 3. Apply Economy Customizations

```bash
# Copy economy customizations
cp ECONOMY_CUSTOMIZATIONS.py backend/simulation/economy_customizations.py
```

**Add to `backend/simulation/economy.py`:**

```python
# Import customizations
from .economy_customizations import FreeMarketEconomy, PlannedEconomy, AdvancedResourceTypes

# Modify the Economy class
class Economy:
    def __init__(self, economy_type: str = "mixed"):
        if economy_type == "free_market":
            # Use FreeMarketEconomy parameters
            self.price_volatility = 0.3
            self.competition_factor = 0.8
            self.government_intervention = 0.0
        elif economy_type == "planned":
            # Use PlannedEconomy parameters
            self.price_volatility = 0.05
            self.competition_factor = 0.2
            self.government_intervention = 0.9
        else:
            # Default mixed economy
            self.price_volatility = 0.15
            self.competition_factor = 0.5
            self.government_intervention = 0.4
```

### 4. Apply Dashboard Customizations

```bash
# Copy dashboard customizations
cp DASHBOARD_CUSTOMIZATIONS.md frontend/src/customizations/
```

**Add to `frontend/src/pages/Network.tsx`:**

```typescript
// Add custom node coloring function
const getNodeColor = (agent: any) => {
  const personality = agent.personality
  if (personality.extraversion > 0.7) return '#ff6b6b'
  if (personality.openness > 0.7) return '#4ecdc4'
  if (personality.agreeableness > 0.7) return '#45b7d1'
  return '#a4b0be'
}

// Apply in the elements mapping
const nodes = networkData.nodes.map((node) => ({
  data: {
    id: node.id,
    label: showLabels ? node.name : '',
    faction: node.faction_id,
    influence: node.influence,
    satisfaction: node.satisfaction,
    personality: node.personality,
    color: getNodeColor(node) // Add custom color
  },
  // ... rest of node configuration
}))
```

## Configuration Files

### 1. Create Simulation Configuration

**Create `config/simulation.yaml`:**

```yaml
simulation:
  agents:
    count: 100
    personality_types:
      - "entrepreneur"
      - "philosopher" 
      - "leader"
      - "merchant"
      - "artist"
    personality_distribution: [0.2, 0.2, 0.2, 0.2, 0.2]
  
  culture:
    type: "creative"  # fast, creative, conservative, tech
    myth_themes:
      - "technology"
      - "fantasy"
      - "science_fiction"
    norm_types:
      - "tech_norms"
      - "creative_norms"
  
  economy:
    type: "mixed"  # free_market, planned, mixed
    resource_types:
      - "knowledge_economy"
      - "creative_economy"
    trade_mechanics: "negotiation_based"
    market_dynamics: "stable"
  
  dashboard:
    theme: "dark"
    update_interval: 1000  # milliseconds
    visualization_types:
      - "network"
      - "culture_timeline"
      - "economy_charts"
```

### 2. Environment Configuration

**Create `.env.example`:**

```bash
# Simulation Settings
SIMULATION_AGENTS=100
SIMULATION_TICKS=1000
SIMULATION_SEED=42

# Agent Settings
AGENT_PERSONALITY_TYPES=entrepreneur,philosopher,leader,merchant,artist
AGENT_PERSONALITY_DISTRIBUTION=0.2,0.2,0.2,0.2,0.2

# Culture Settings
CULTURE_TYPE=creative
CULTURE_DRIFT_FREQUENCY=3
CULTURE_MYTH_THRESHOLD=0.6

# Economy Settings
ECONOMY_TYPE=mixed
ECONOMY_VOLATILITY=0.15
ECONOMY_COMPETITION=0.5

# Dashboard Settings
DASHBOARD_THEME=dark
DASHBOARD_UPDATE_INTERVAL=1000
```

## Testing Your Customizations

### 1. Run Customized Simulation

```bash
# Test with custom agent types
python3 scripts/seed_and_run.py --agents 50 --personality-types entrepreneur,philosopher,leader

# Test with custom culture
python3 scripts/seed_and_run.py --culture-type creative --ticks 100

# Test with custom economy
python3 scripts/seed_and_run.py --economy-type free_market --ticks 100
```

### 2. Verify Dashboard Changes

```bash
# Start the development servers
cd backend && python3 -m uvicorn app:app --reload &
cd frontend && npm run dev &

# Open dashboard at http://localhost:5173
# Check that:
# - Node colors reflect personality types
# - Cultural evolution is faster/slower as configured
# - Economic indicators show expected behavior
```

### 3. Performance Testing

```bash
# Test with larger populations
python3 scripts/seed_and_run.py --agents 500 --ticks 200

# Monitor performance
python3 scripts/benchmark.py --agents 1000 --ticks 100
```

## Deployment with Customizations

### 1. Update Docker Configuration

**Update `docker/docker-compose.yml`:**

```yaml
services:
  backend:
    environment:
      - SIMULATION_AGENTS=100
      - CULTURE_TYPE=creative
      - ECONOMY_TYPE=mixed
      - AGENT_PERSONALITY_TYPES=entrepreneur,philosopher,leader
```

### 2. Update Render Configuration

**Update `render.yaml`:**

```yaml
services:
  - type: web
    name: cognisphere-backend
    envVars:
      - key: CULTURE_TYPE
        value: creative
      - key: ECONOMY_TYPE
        value: mixed
      - key: AGENT_PERSONALITY_TYPES
        value: entrepreneur,philosopher,leader,merchant,artist
```

## Monitoring and Analytics

### 1. Add Custom Metrics

**Create `backend/monitoring/custom_metrics.py`:**

```python
from prometheus_client import Counter, Histogram, Gauge

# Custom metrics for your customizations
entrepreneur_trades = Counter('entrepreneur_trades_total', 'Total trades by entrepreneurs')
philosopher_myths = Counter('philosopher_myths_total', 'Total myths created by philosophers')
culture_evolution_rate = Gauge('culture_evolution_rate', 'Current culture evolution rate')
economy_volatility = Gauge('economy_volatility', 'Current economic volatility')

# Use in your simulation
def record_agent_action(agent, action):
    if agent.personality_type == "entrepreneur" and action == "trade":
        entrepreneur_trades.inc()
    elif agent.personality_type == "philosopher" and action == "create_myth":
        philosopher_myths.inc()
```

### 2. Custom Dashboard Widgets

**Create `frontend/src/components/CustomWidgets.tsx`:**

```typescript
// Custom widgets for your specific customizations
export const PersonalityDistributionWidget = () => {
  const { state } = useSimulation()
  
  const personalityCounts = useMemo(() => {
    const counts = { entrepreneur: 0, philosopher: 0, leader: 0, merchant: 0, artist: 0 }
    state.agents.forEach(agent => {
      counts[agent.personality_type]++
    })
    return counts
  }, [state.agents])
  
  return (
    <div className="personality-widget">
      <h3>Personality Distribution</h3>
      {Object.entries(personalityCounts).map(([type, count]) => (
        <div key={type} className="personality-bar">
          <span>{type}</span>
          <div className="bar">
            <div 
              className="bar-fill" 
              style={{ width: `${(count / state.agents.length) * 100}%` }}
            />
          </div>
          <span>{count}</span>
        </div>
      ))}
    </div>
  )
}
```

## Troubleshooting

### Common Issues

1. **Import Errors**: Make sure all custom files are in the correct directories
2. **Performance Issues**: Reduce agent count or tick frequency for testing
3. **Dashboard Not Updating**: Check WebSocket connections and API endpoints
4. **Custom Styles Not Applied**: Verify CSS imports and class names

### Debug Mode

```bash
# Enable debug logging
export DEBUG=1
export LOG_LEVEL=DEBUG

# Run with debug output
python3 scripts/seed_and_run.py --debug --agents 10 --ticks 50
```

This implementation guide will help you quickly apply all the customizations and get The Cognisphere running with your specific requirements!
