# Environmental Stimuli System

The Environmental Stimuli System is a groundbreaking feature that connects The Cognisphere to real-world data, allowing the digital civilization to evolve based on actual events, trends, and patterns from our reality.

## Overview

This system creates a living bridge between reality and simulation, where:

1. **Real-world data** is continuously ingested from multiple sources
2. **Environmental stimuli** are processed and analyzed for cultural impact
3. **Cultural mirroring** makes the civilization initially reflect reality (70% mirroring factor)
4. **Divergence mechanics** gradually evolve the culture into a "future version" (1% divergence rate per stimulus)

## How It Works

### Data Ingestion

The system fetches real-world data from multiple sources:

- **RSS Feeds**: BBC Technology, Science, Business, Entertainment, CNN Technology
- **News APIs**: Technology, science, business, entertainment, health news
- **Weather Data**: Current weather conditions affecting social behavior
- **Social Media**: Trends and cultural movements (extensible)

### Stimulus Processing

Each piece of real-world data becomes an `EnvironmentalStimulus` with:

- **Sentiment Analysis**: Positive/negative emotional impact (-1.0 to 1.0)
- **Intensity Levels**: Low, Medium, High, Critical based on content analysis
- **Impact Scores**: Cultural, Economic, and Social impact calculations
- **Keywords**: Extracted meaningful terms that influence agent vocabulary

### Cultural Evolution

The system implements sophisticated cultural evolution mechanics:

#### Mirroring Phase
- **70% Mirroring Factor**: Culture initially mirrors real-world patterns
- Agents adopt vocabulary, behaviors, and preferences from reality
- Social norms and economic patterns reflect current world trends

#### Divergence Phase
- **1% Divergence Rate**: Each stimulus introduces small variations
- Culture gradually evolves beyond current reality
- Creates a "future version" of human civilization
- Agents develop novel concepts, behaviors, and social structures

## API Endpoints

### Get Stimuli Status
```http
GET /stimuli/status
```
Returns the current status of the environmental stimuli system, including:
- Active stimuli count
- Cultural mirroring factor
- Divergence rate
- Historical data summary

### Get Active Stimuli
```http
GET /stimuli/active
```
Returns all currently active environmental stimuli with:
- Stimulus details (title, content, source)
- Sentiment and intensity scores
- Impact measurements
- Keywords and timestamps

### Filter by Type
```http
GET /stimuli/by-type/{stimulus_type}
```
Filter stimuli by type:
- `news` - General news articles
- `technological` - Technology-related content
- `scientific` - Science and research
- `economic` - Business and economy
- `cultural` - Arts, entertainment, culture
- `weather` - Weather conditions
- `social_media` - Social media trends

### Manual Fetch
```http
POST /stimuli/fetch
```
Manually trigger fetching of new environmental stimuli from all sources.

### Cultural Divergence Analysis
```http
GET /stimuli/divergence
```
Get detailed analysis of cultural divergence from reality, including:
- Mirroring factor percentage
- Divergence rate
- Reality baseline patterns
- Future projection insights

## Frontend Dashboard

The Environmental Stimuli Dashboard provides:

### Real-time Monitoring
- Live feed of incoming stimuli
- Sentiment analysis visualization
- Impact score tracking
- Cultural evolution metrics

### Filtering and Analysis
- Filter by stimulus type
- Sort by intensity, sentiment, or timestamp
- Keyword analysis
- Historical trends

### Cultural Divergence Visualization
- Mirroring factor display
- Divergence rate tracking
- Reality baseline comparison
- Future projection insights

## Configuration

### Data Sources

Add new data sources by extending the `DataSource` class:

```python
class CustomSource(DataSource):
    def __init__(self, name: str, enabled: bool = True):
        super().__init__(name, enabled)
    
    async def fetch_data(self) -> List[EnvironmentalStimulus]:
        # Implement data fetching logic
        pass
```

### Stimulus Types

Add new stimulus types by extending `StimulusType` enum:

```python
class StimulusType(Enum):
    NEWS = "news"
    CUSTOM_TYPE = "custom_type"
```

### Cultural Parameters

Adjust cultural evolution parameters:

```python
manager = EnvironmentalStimuliManager()
manager.cultural_mirroring_factor = 0.8  # 80% mirroring
manager.divergence_rate = 0.02  # 2% divergence rate
```

## Impact on Simulation

### Agent Behavior
- **Personality Evolution**: Agents' personalities shift based on stimuli
- **Vocabulary Growth**: New words and concepts enter agent language
- **Social Dynamics**: Cooperation and trading behaviors adapt to real-world patterns
- **Cultural Preferences**: Agents develop preferences based on environmental influences

### Economic Systems
- **Market Sentiment**: Economic stimuli affect trading willingness
- **Resource Preferences**: Agents adapt resource priorities based on real-world trends
- **Innovation Patterns**: Technology stimuli drive innovation in the simulation

### Social Structures
- **Alliance Formation**: Social stimuli influence cooperation patterns
- **Cultural Norms**: Real-world events shape emerging social norms
- **Institution Development**: Agents create institutions reflecting real-world patterns

## Future Enhancements

### Planned Features
- **Machine Learning Integration**: AI-powered sentiment analysis and trend prediction
- **Social Media APIs**: Direct integration with Twitter, Reddit, and other platforms
- **Economic Data**: Real-time stock market and economic indicator integration
- **Scientific Papers**: Integration with arXiv and other research databases
- **Cultural Events**: Calendar integration for festivals, holidays, and cultural events

### Advanced Analytics
- **Predictive Modeling**: Forecast cultural evolution trends
- **Reality Comparison**: Compare simulation outcomes with real-world predictions
- **Anomaly Detection**: Identify when simulation diverges significantly from reality
- **Cultural Mapping**: Visualize the evolution from reality to future civilization

## Usage Examples

### Basic Setup
```python
from simulation.environmental_stimuli import create_default_stimuli_manager

# Create stimuli manager with default sources
manager = create_default_stimuli_manager()

# Fetch stimuli
stimuli = await manager.fetch_all_stimuli()
```

### Custom Configuration
```python
from simulation.environmental_stimuli import EnvironmentalStimuliManager, NewsAPISource

# Create custom manager
manager = EnvironmentalStimuliManager()

# Add custom news source
news_source = NewsAPISource(api_key="your_api_key")
manager.add_source(news_source)

# Adjust cultural parameters
manager.cultural_mirroring_factor = 0.6  # 60% mirroring
manager.divergence_rate = 0.015  # 1.5% divergence rate
```

### Integration with Simulation
```python
# Environmental stimuli are automatically applied every 10 ticks
# Access stimuli status through the simulation engine
status = simulation_engine.get_environmental_stimuli_status()
```

## Monitoring and Debugging

### Logging
The system provides comprehensive logging for:
- Data source fetch operations
- Stimulus processing and analysis
- Cultural impact calculations
- Divergence measurements

### Metrics
Track key metrics:
- Stimuli fetch rate and success rate
- Cultural mirroring accuracy
- Divergence progression
- Agent behavior changes

### Health Checks
Monitor system health:
- Data source availability
- Processing performance
- Memory usage
- Error rates

## Conclusion

The Environmental Stimuli System transforms The Cognisphere from a closed simulation into a living, breathing digital civilization that:

1. **Starts grounded in reality** through cultural mirroring
2. **Evolves organically** through environmental influences
3. **Develops unique characteristics** through divergence mechanics
4. **Creates a future version** of human civilization

This creates an unprecedented opportunity to study how real-world events shape cultural evolution and to explore what human civilization might become in the future.

The system is designed to be extensible, allowing researchers and developers to add new data sources, adjust cultural parameters, and explore different scenarios of civilizational evolution.
