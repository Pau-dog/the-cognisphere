# Dashboard Visualization Customizations

This guide shows how to customize the React dashboard visualizations for The Cognisphere.

## 1. Network Visualization Customizations

### File: `frontend/src/pages/Network.tsx`

#### Custom Node Colors by Agent Type

```typescript
// Add this function to customize node colors
const getNodeColor = (agent: any) => {
  const personality = agent.personality
  
  // Color based on dominant personality trait
  if (personality.extraversion > 0.7) return '#ff6b6b' // Red for extroverts
  if (personality.openness > 0.7) return '#4ecdc4'    // Teal for creative
  if (personality.agreeableness > 0.7) return '#45b7d1' // Blue for cooperative
  if (personality.conscientiousness > 0.7) return '#96ceb4' // Green for organized
  if (personality.neuroticism > 0.7) return '#feca57' // Yellow for anxious
  return '#a4b0be' // Default gray
}

// Custom node sizes based on influence
const getNodeSize = (agent: any) => {
  const baseSize = 20
  const influenceMultiplier = agent.influence / 100
  return baseSize + (influenceMultiplier * 30)
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
    // Add custom properties
    color: getNodeColor(node),
    size: getNodeSize(node)
  },
  classes: node.faction_id ? 'faction-member' : 'independent',
  position: {
    x: Math.random() * 800,
    y: Math.random() * 600
  }
}))
```

#### Custom Edge Styling

```typescript
// Customize edge colors and thickness
const getEdgeColor = (edge: any) => {
  const relationship = edge.relationship_type
  
  switch (relationship) {
    case 'alliance': return '#2ecc71'      // Green for alliances
    case 'trade': return '#3498db'         // Blue for trade
    case 'hostile': return '#e74c3c'       // Red for hostility
    case 'neutral': return '#95a5a6'       // Gray for neutral
    default: return '#bdc3c7'
  }
}

const getEdgeWidth = (edge: any) => {
  return Math.max(1, Math.min(10, edge.strength * 5))
}

// Apply in the edges mapping
const edges = networkData.edges.map((edge) => ({
  data: {
    id: `${edge.source}-${edge.target}`,
    source: edge.source,
    target: edge.target,
    relationship: edge.relationship_type,
    strength: edge.strength,
    // Add custom properties
    color: getEdgeColor(edge),
    width: getEdgeWidth(edge)
  }
}))
```

#### Advanced Layout Options

```typescript
// Add custom layout options
const layoutOptions = {
  name: 'cose',
  nodeRepulsion: 4000,
  idealEdgeLength: 100,
  edgeElasticity: 0.45,
  nestingFactor: 0.1,
  gravity: 0.25,
  numIter: 2500,
  tile: true,
  animate: true,
  animationDuration: 1000,
  tilingPaddingVertical: 10,
  tilingPaddingHorizontal: 10,
  gravityRangeCompound: 1.5,
  gravityCompound: 1.0,
  gravityRange: 3.8,
  initialEnergyOnIncremental: 0.3
}

// Use in CytoscapeComponent
<CytoscapeComponent
  elements={elements}
  layout={layoutOptions}
  style={{ width: '100%', height: '600px' }}
  stylesheet={stylesheet}
  cy={(cy) => {
    cy.on('tap', 'node', (evt) => {
      setSelectedNode(evt.target.data())
    })
  }}
/>
```

## 2. Culture Timeline Customizations

### File: `frontend/src/pages/Culture.tsx`

#### Custom Myth Display Cards

```typescript
// Add custom theme colors
const getThemeColor = (theme: string) => {
  const themeColors: { [key: string]: string } = {
    'creation': '#9b59b6',
    'heroism': '#e74c3c',
    'wisdom': '#3498db',
    'transformation': '#f39c12',
    'sacrifice': '#e67e22',
    'exploration': '#1abc9c',
    'order': '#34495e',
    'chaos': '#e74c3c',
    'mystery': '#8e44ad',
    'celebration': '#f1c40f'
  }
  return themeColors[theme] || '#95a5a6'
}

// Custom myth card component
const MythCard = ({ myth }: { myth: any }) => (
  <motion.div
    className="myth-card"
    style={{
      borderLeft: `4px solid ${getThemeColor(myth.theme)}`,
      background: `linear-gradient(135deg, ${getThemeColor(myth.theme)}20, transparent)`,
      boxShadow: `0 4px 8px ${getThemeColor(myth.theme)}30`
    }}
    whileHover={{ scale: 1.02 }}
    initial={{ opacity: 0, y: 20 }}
    animate={{ opacity: 1, y: 0 }}
    transition={{ duration: 0.3 }}
  >
    <div className="myth-header">
      <h3 className="myth-title">{myth.title}</h3>
      <span 
        className="theme-badge"
        style={{ backgroundColor: getThemeColor(myth.theme) }}
      >
        {myth.theme}
      </span>
    </div>
    
    <div className="myth-stats">
      <div className="stat">
        <span className="stat-label">Popularity</span>
        <div className="stat-bar">
          <div 
            className="stat-fill"
            style={{ 
              width: `${myth.popularity * 100}%`,
              backgroundColor: getThemeColor(myth.theme)
            }}
          />
        </div>
        <span className="stat-value">{myth.popularity.toFixed(2)}</span>
      </div>
      
      <div className="stat">
        <span className="stat-label">Influence</span>
        <span className="stat-value">{myth.influence.toFixed(1)}</span>
      </div>
    </div>
    
    <p className="myth-content">{myth.content}</p>
    
    {myth.characters && myth.characters.length > 0 && (
      <div className="myth-characters">
        <span className="characters-label">Characters:</span>
        {myth.characters.map((char: string, index: number) => (
          <span key={index} className="character-tag">{char}</span>
        ))}
      </div>
    )}
  </motion.div>
)
```

#### Interactive Slang Evolution Chart

```typescript
// Add real-time slang evolution visualization
const SlangEvolutionChart = ({ slangData }: { slangData: any[] }) => {
  const [selectedTimeframe, setSelectedTimeframe] = useState('30')
  
  const filteredData = slangData.filter(slang => 
    slang.tick_created >= (currentTick - parseInt(selectedTimeframe))
  )
  
  return (
    <div className="slang-evolution">
      <div className="chart-header">
        <h3>Language Evolution</h3>
        <select 
          value={selectedTimeframe} 
          onChange={(e) => setSelectedTimeframe(e.target.value)}
        >
          <option value="10">Last 10 ticks</option>
          <option value="30">Last 30 ticks</option>
          <option value="100">Last 100 ticks</option>
        </select>
      </div>
      
      <div className="slang-timeline">
        {filteredData.map((slang, index) => (
          <motion.div
            key={slang.id}
            className="slang-item"
            initial={{ opacity: 0, x: -20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ delay: index * 0.1 }}
          >
            <div className="slang-word">{slang.word}</div>
            <div className="slang-meaning">{slang.meaning}</div>
            <div className="slang-stats">
              <span>Popularity: {slang.popularity.toFixed(2)}</span>
              <span>Adoption: {(slang.adoption_rate * 100).toFixed(1)}%</span>
            </div>
          </motion.div>
        ))}
      </div>
    </div>
  )
}
```

## 3. Economy Dashboard Customizations

### File: `frontend/src/pages/Economy.tsx`

#### Real-time Price Charts

```typescript
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts'

// Custom price chart component
const PriceChart = ({ priceData }: { priceData: any[] }) => {
  const [selectedResources, setSelectedResources] = useState(['food', 'energy', 'artifacts'])
  
  return (
    <div className="price-chart-container">
      <div className="chart-controls">
        <h3>Resource Prices</h3>
        <div className="resource-selector">
          {['food', 'energy', 'artifacts', 'influence'].map(resource => (
            <label key={resource} className="resource-checkbox">
              <input
                type="checkbox"
                checked={selectedResources.includes(resource)}
                onChange={(e) => {
                  if (e.target.checked) {
                    setSelectedResources([...selectedResources, resource])
                  } else {
                    setSelectedResources(selectedResources.filter(r => r !== resource))
                  }
                }}
              />
              <span className="resource-name">{resource}</span>
            </label>
          ))}
        </div>
      </div>
      
      <ResponsiveContainer width="100%" height={400}>
        <LineChart data={priceData}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="tick" />
          <YAxis />
          <Tooltip />
          <Legend />
          {selectedResources.map((resource, index) => (
            <Line
              key={resource}
              type="monotone"
              dataKey={resource}
              stroke={`hsl(${index * 90}, 70%, 50%)`}
              strokeWidth={2}
              dot={false}
            />
          ))}
        </LineChart>
      </ResponsiveContainer>
    </div>
  )
}
```

#### Trade Volume Heatmap

```typescript
// Trade volume heatmap component
const TradeHeatmap = ({ tradeData }: { tradeData: any[] }) => {
  const [timeframe, setTimeframe] = useState('24')
  
  // Process trade data into heatmap format
  const heatmapData = useMemo(() => {
    const hours = Array.from({ length: parseInt(timeframe) }, (_, i) => i)
    const resources = ['food', 'energy', 'artifacts', 'influence']
    
    return hours.map(hour => {
      const hourData: any = { hour }
      resources.forEach(resource => {
        const resourceTrades = tradeData.filter(trade => 
          trade.tick >= (currentTick - parseInt(timeframe)) + hour &&
          (trade.resources_offered[resource] > 0 || trade.resources_requested[resource] > 0)
        )
        hourData[resource] = resourceTrades.length
      })
      return hourData
    })
  }, [tradeData, timeframe, currentTick])
  
  return (
    <div className="trade-heatmap">
      <div className="heatmap-header">
        <h3>Trade Volume Heatmap</h3>
        <select value={timeframe} onChange={(e) => setTimeframe(e.target.value)}>
          <option value="12">Last 12 ticks</option>
          <option value="24">Last 24 ticks</option>
          <option value="48">Last 48 ticks</option>
        </select>
      </div>
      
      <div className="heatmap-grid">
        {heatmapData.map((hourData, hourIndex) => (
          <div key={hourIndex} className="heatmap-hour">
            <div className="hour-label">T{hourData.hour}</div>
            {['food', 'energy', 'artifacts', 'influence'].map(resource => (
              <div
                key={resource}
                className={`heatmap-cell ${resource}`}
                style={{
                  backgroundColor: `rgba(52, 152, 219, ${Math.min(1, hourData[resource] / 10)})`
                }}
                title={`${resource}: ${hourData[resource]} trades`}
              />
            ))}
          </div>
        ))}
      </div>
    </div>
  )
}
```

## 4. Custom CSS Styles

### File: `frontend/src/index.css`

```css
/* Custom dashboard styles */

.myth-card {
  @apply bg-white rounded-lg p-4 shadow-md mb-4 transition-all duration-300;
}

.myth-card:hover {
  @apply shadow-lg transform scale-105;
}

.theme-badge {
  @apply text-white px-2 py-1 rounded-full text-xs font-semibold;
}

.stat-bar {
  @apply w-full h-2 bg-gray-200 rounded-full overflow-hidden;
}

.stat-fill {
  @apply h-full transition-all duration-500;
}

.character-tag {
  @apply bg-blue-100 text-blue-800 px-2 py-1 rounded-full text-xs mr-1;
}

.slang-item {
  @apply bg-white rounded-lg p-3 mb-2 shadow-sm border-l-4 border-blue-500;
}

.slang-word {
  @apply font-bold text-lg text-blue-700;
}

.slang-meaning {
  @apply text-gray-600 text-sm;
}

.slang-stats {
  @apply flex justify-between text-xs text-gray-500 mt-2;
}

.heatmap-grid {
  @apply grid grid-cols-12 gap-1;
}

.heatmap-cell {
  @apply w-4 h-4 rounded-sm border border-gray-200;
}

.heatmap-cell.food { border-color: #e74c3c; }
.heatmap-cell.energy { border-color: #f39c12; }
.heatmap-cell.artifacts { border-color: #9b59b6; }
.heatmap-cell.influence { border-color: #2ecc71; }

.resource-checkbox {
  @apply flex items-center mr-4 cursor-pointer;
}

.resource-checkbox input {
  @apply mr-2;
}

/* Animation classes */
.fade-in {
  animation: fadeIn 0.5s ease-in;
}

@keyframes fadeIn {
  from { opacity: 0; transform: translateY(20px); }
  to { opacity: 1; transform: translateY(0); }
}

.slide-in-left {
  animation: slideInLeft 0.3s ease-out;
}

@keyframes slideInLeft {
  from { opacity: 0; transform: translateX(-20px); }
  to { opacity: 1; transform: translateX(0); }
}
```

## 5. Real-time Updates

### File: `frontend/src/hooks/useRealTimeData.ts`

```typescript
import { useEffect, useState } from 'react'
import { useSimulation } from '../state/SimulationContext'

export const useRealTimeData = (endpoint: string, interval: number = 1000) => {
  const [data, setData] = useState(null)
  const [isLoading, setIsLoading] = useState(true)
  const { state } = useSimulation()
  
  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await fetch(`/api/${endpoint}`)
        const newData = await response.json()
        setData(newData)
        setIsLoading(false)
      } catch (error) {
        console.error(`Error fetching ${endpoint}:`, error)
      }
    }
    
    fetchData()
    const intervalId = setInterval(fetchData, interval)
    
    return () => clearInterval(intervalId)
  }, [endpoint, interval])
  
  return { data, isLoading }
}

// Usage in components
const NetworkPage = () => {
  const { data: networkData, isLoading } = useRealTimeData('network', 2000)
  
  if (isLoading) return <div>Loading network data...</div>
  
  return (
    <div>
      {/* Network visualization */}
    </div>
  )
}
```

## 6. Custom Themes

### File: `frontend/src/themes/darkTheme.ts`

```typescript
export const darkTheme = {
  colors: {
    primary: '#3498db',
    secondary: '#2ecc71',
    background: '#1a1a1a',
    surface: '#2d2d2d',
    text: '#ffffff',
    textSecondary: '#b0b0b0',
    border: '#404040',
    error: '#e74c3c',
    warning: '#f39c12',
    success: '#2ecc71'
  },
  
  nodeColors: {
    extrovert: '#ff6b6b',
    creative: '#4ecdc4',
    cooperative: '#45b7d1',
    organized: '#96ceb4',
    anxious: '#feca57',
    default: '#a4b0be'
  },
  
  edgeColors: {
    alliance: '#2ecc71',
    trade: '#3498db',
    hostile: '#e74c3c',
    neutral: '#95a5a6'
  }
}

// Apply theme in main component
const ThemedDashboard = () => {
  const [theme, setTheme] = useState(darkTheme)
  
  return (
    <div style={{ 
      backgroundColor: theme.colors.background,
      color: theme.colors.text 
    }}>
      {/* Dashboard content */}
    </div>
  )
}
```

These customizations will give you complete control over the dashboard appearance and functionality, allowing you to create a unique visualization experience for The Cognisphere!
