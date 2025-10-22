import React, { useRef, useEffect, useState } from 'react'
import { motion } from 'framer-motion'
import { Network as NetworkIcon, Users, Link, Eye, EyeOff } from 'lucide-react'
import { useSimulation } from '../state/SimulationContext'
import CytoscapeComponent from 'react-cytoscapejs'
import mockData from '../data/mockData'

const Network: React.FC = () => {
  const { state } = useSimulation()
  const [showLabels, setShowLabels] = useState(true)
  const [showFactions, setShowFactions] = useState(true)
  const [selectedNode, setSelectedNode] = useState<any>(null)
  
  // Use mock data for screenshots
  const useMockData = false
  const data = useMockData ? mockData : state

  const networkData = useMockData ? {
    nodes: data.agents.map(agent => ({
      id: agent.id,
      name: agent.name,
      faction_id: agent.faction,
      influence: agent.influence,
      satisfaction: agent.satisfaction,
      personality: { openness: 0.7, conscientiousness: 0.6, extraversion: 0.5, agreeableness: 0.8, neuroticism: 0.3 }
    })),
    edges: data.network.connections.map(conn => ({
      source: conn.from,
      target: conn.to,
      trust_level: conn.trust,
      interaction_count: Math.floor(conn.trust * 100)
    }))
  } : state.networkData

  // Convert network data to Cytoscape format
  const elements = React.useMemo(() => {
    if (!networkData) return []

    const nodes = networkData.nodes.map((node) => ({
      data: {
        id: node.id,
        label: showLabels ? node.name : '',
        faction: node.faction_id,
        influence: node.influence,
        satisfaction: node.satisfaction,
        personality: node.personality
      },
      classes: node.faction_id ? 'faction-member' : 'independent',
      position: {
        x: Math.random() * 800,
        y: Math.random() * 600
      }
    }))

    const edges = networkData.edges.map((edge) => ({
      data: {
        id: `${edge.source}-${edge.target}`,
        source: edge.source,
        target: edge.target,
        trust: edge.trust_level,
        interactions: edge.interaction_count
      },
      classes: edge.trust_level > 0 ? 'positive-trust' : 'negative-trust'
    }))

    return [...nodes, ...edges]
  }, [networkData, showLabels, showFactions])

  const layout = {
    name: 'random',
    fit: true,
    padding: 30,
    nodeDimensionsIncludeLabels: true,
    animate: true,
    animationDuration: 1000,
    randomize: true
  }

  const stylesheet = [
    {
      selector: 'node',
      style: {
        'background-color': '#3B82F6',
        'label': 'data(label)',
        'text-valign': 'center',
        'text-halign': 'center',
        'color': '#FFFFFF',
        'font-size': '12px',
        'font-weight': 'bold',
        'width': '40px',
        'height': '40px',
        'border-width': '2px',
        'border-color': '#1E40AF'
      }
    },
    {
      selector: 'node.faction-member',
      style: {
        'background-color': '#8B5CF6',
        'border-color': '#7C3AED'
      }
    },
    {
      selector: 'node.independent',
      style: {
        'background-color': '#6B7280',
        'border-color': '#4B5563'
      }
    },
    {
      selector: 'edge',
      style: {
        'width': '2px',
        'line-color': '#9CA3AF',
        'target-arrow-color': '#9CA3AF',
        'target-arrow-shape': 'triangle',
        'curve-style': 'bezier'
      }
    },
    {
      selector: 'edge.positive-trust',
      style: {
        'line-color': '#10B981',
        'target-arrow-color': '#10B981'
      }
    },
    {
      selector: 'edge.negative-trust',
      style: {
        'line-color': '#EF4444',
        'target-arrow-color': '#EF4444'
      }
    }
  ]

  const handleNodeClick = (event: any) => {
    const node = event.target
    setSelectedNode({
      id: node.id(),
      data: node.data()
    })
  }

  const networkStats = {
    totalAgents: networkData?.nodes.length || 0,
    totalConnections: networkData?.edges.length || 0,
    avgConnections: networkData?.nodes.length ? (networkData.edges.length / networkData.nodes.length).toFixed(2) : '0.00',
    factions: useMockData ? data.status.factions_count : 0
  }

  const connectionTypes = {
    positiveTrust: networkData?.edges.filter(e => e.trust_level > 0).length || 0,
    negativeTrust: networkData?.edges.filter(e => e.trust_level < 0).length || 0,
    neutral: networkData?.edges.filter(e => e.trust_level === 0).length || 0
  }

  const factionDistribution = useMockData ? {
    factionMembers: data.network.factions.reduce((sum, faction) => sum + faction.members, 0),
    independentAgents: data.status.agents_count - data.network.factions.reduce((sum, faction) => sum + faction.members, 0),
    totalFactions: data.status.factions_count
  } : {
    factionMembers: 0,
    independentAgents: 0,
    totalFactions: 0
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold text-white">Agent Network</h1>
          <p className="text-secondary-400 mt-2">
            Visualize agent relationships and social connections
          </p>
        </div>
        
        <div className="flex items-center space-x-4">
          <button
            onClick={() => setShowLabels(!showLabels)}
            className={`flex items-center space-x-2 px-3 py-2 rounded-lg transition-colors ${
              showLabels 
                ? 'bg-primary-600 text-white' 
                : 'bg-secondary-700 text-secondary-300 hover:bg-secondary-600'
            }`}
          >
            {showLabels ? <Eye className="w-4 h-4" /> : <EyeOff className="w-4 h-4" />}
            <span>Labels</span>
          </button>
          
          <button
            onClick={() => setShowFactions(!showFactions)}
            className={`flex items-center space-x-2 px-3 py-2 rounded-lg transition-colors ${
              showFactions 
                ? 'bg-primary-600 text-white' 
                : 'bg-secondary-700 text-secondary-300 hover:bg-secondary-600'
            }`}
          >
            <Users className="w-4 h-4" />
            <span>Factions</span>
          </button>
        </div>
      </div>

      {/* Network Stats */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="card p-6"
        >
          <div className="flex items-center space-x-3">
            <div className="p-3 bg-blue-500/10 rounded-lg">
              <Users className="w-6 h-6 text-blue-400" />
            </div>
            <div>
              <p className="text-sm text-secondary-400">Total Agents</p>
              <p className="text-2xl font-bold text-white">{networkStats.totalAgents}</p>
            </div>
          </div>
        </motion.div>

        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.1 }}
          className="card p-6"
        >
          <div className="flex items-center space-x-3">
            <div className="p-3 bg-green-500/10 rounded-lg">
              <Link className="w-6 h-6 text-green-400" />
            </div>
            <div>
              <p className="text-sm text-secondary-400">Connections</p>
              <p className="text-2xl font-bold text-white">{networkStats.totalConnections}</p>
            </div>
          </div>
        </motion.div>

        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.2 }}
          className="card p-6"
        >
          <div className="flex items-center space-x-3">
            <div className="p-3 bg-purple-500/10 rounded-lg">
              <NetworkIcon className="w-6 h-6 text-purple-400" />
            </div>
            <div>
              <p className="text-sm text-secondary-400">Avg Connections</p>
              <p className="text-2xl font-bold text-white">{networkStats.avgConnections}</p>
            </div>
          </div>
        </motion.div>

        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.3 }}
          className="card p-6"
        >
          <div className="flex items-center space-x-3">
            <div className="p-3 bg-yellow-500/10 rounded-lg">
              <Users className="w-6 h-6 text-yellow-400" />
            </div>
            <div>
              <p className="text-sm text-secondary-400">Factions</p>
              <p className="text-2xl font-bold text-white">{networkStats.factions}</p>
            </div>
          </div>
        </motion.div>
      </div>

      {/* Network Visualization */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <motion.div
          initial={{ opacity: 0, x: -20 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ delay: 0.4 }}
          className="lg:col-span-2 card p-6"
        >
          <div className="flex items-center space-x-3 mb-6">
            <NetworkIcon className="w-6 h-6 text-primary-400" />
            <h2 className="text-lg font-semibold">Network Graph</h2>
          </div>
          
          <div className="h-96 bg-secondary-800 rounded-lg border border-secondary-700">
            {networkData && networkData.nodes.length > 0 ? (
              <CytoscapeComponent
                elements={elements}
                layout={layout}
                stylesheet={stylesheet}
                style={{ width: '100%', height: '100%' }}
                cy={(cy) => {
                  cy.on('tap', 'node', handleNodeClick)
                }}
              />
            ) : (
              <div className="flex items-center justify-center h-full">
                <div className="text-center">
                  <NetworkIcon className="w-12 h-12 text-secondary-500 mx-auto mb-4" />
                  <p className="text-secondary-400 mb-2">No network data available</p>
                  <p className="text-sm text-secondary-500">Start a simulation to see agent connections</p>
                </div>
              </div>
            )}
          </div>
        </motion.div>

        <motion.div
          initial={{ opacity: 0, x: 20 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ delay: 0.5 }}
          className="card p-6"
        >
          <div className="flex items-center space-x-3 mb-6">
            <Users className="w-6 h-6 text-primary-400" />
            <h2 className="text-lg font-semibold">Agent Details</h2>
          </div>
          
          {selectedNode ? (
            <div className="space-y-4">
              <div>
                <h3 className="font-medium text-white">{selectedNode.data.label}</h3>
                <p className="text-sm text-secondary-400">ID: {selectedNode.id}</p>
              </div>
              
              <div className="space-y-2">
                <div className="flex justify-between">
                  <span className="text-sm text-secondary-400">Influence:</span>
                  <span className="text-sm text-white">{(selectedNode.data.influence * 100).toFixed(1)}%</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-sm text-secondary-400">Satisfaction:</span>
                  <span className="text-sm text-white">{(selectedNode.data.satisfaction * 100).toFixed(1)}%</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-sm text-secondary-400">Faction:</span>
                  <span className="text-sm text-white">{selectedNode.data.faction || 'Independent'}</span>
                </div>
              </div>
            </div>
          ) : (
            <div className="text-center">
              <Users className="w-12 h-12 text-secondary-500 mx-auto mb-4" />
              <p className="text-secondary-400 mb-2">Click on an agent to see details</p>
            </div>
          )}
        </motion.div>
      </div>

      {/* Network Analysis */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.6 }}
        className="card p-6"
      >
        <h2 className="text-lg font-semibold mb-6">Network Analysis</h2>
        
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          <div>
            <h3 className="font-medium text-white mb-3">Connection Types</h3>
            <div className="space-y-2">
              <div className="flex items-center justify-between">
                <div className="flex items-center space-x-2">
                  <div className="w-3 h-3 bg-green-500 rounded-full"></div>
                  <span className="text-sm text-secondary-400">Positive Trust</span>
                </div>
                <span className="text-sm text-white">{connectionTypes.positiveTrust}</span>
              </div>
              <div className="flex items-center justify-between">
                <div className="flex items-center space-x-2">
                  <div className="w-3 h-3 bg-red-500 rounded-full"></div>
                  <span className="text-sm text-secondary-400">Negative Trust</span>
                </div>
                <span className="text-sm text-white">{connectionTypes.negativeTrust}</span>
              </div>
              <div className="flex items-center justify-between">
                <div className="flex items-center space-x-2">
                  <div className="w-3 h-3 bg-gray-500 rounded-full"></div>
                  <span className="text-sm text-secondary-400">Neutral</span>
                </div>
                <span className="text-sm text-white">{connectionTypes.neutral}</span>
              </div>
            </div>
          </div>

          <div>
            <h3 className="font-medium text-white mb-3">Faction Distribution</h3>
            <div className="space-y-2">
              <div className="flex justify-between">
                <span className="text-sm text-secondary-400">Faction Members</span>
                <span className="text-sm text-white">{factionDistribution.factionMembers}</span>
              </div>
              <div className="flex justify-between">
                <span className="text-sm text-secondary-400">Independent Agents</span>
                <span className="text-sm text-white">{factionDistribution.independentAgents}</span>
              </div>
              <div className="flex justify-between">
                <span className="text-sm text-secondary-400">Total Factions</span>
                <span className="text-sm text-white">{factionDistribution.totalFactions}</span>
              </div>
            </div>
          </div>

          <div>
            <h3 className="font-medium text-white mb-3">Network Metrics</h3>
            <div className="space-y-2">
              <div className="flex justify-between">
                <span className="text-sm text-secondary-400">Density</span>
                <span className="text-sm text-white">{networkStats.totalAgents > 0 ? (networkStats.totalConnections / (networkStats.totalAgents * (networkStats.totalAgents - 1))).toFixed(4) : '0.0000'}</span>
              </div>
              <div className="flex justify-between">
                <span className="text-sm text-secondary-400">Avg Trust</span>
                <span className="text-sm text-white">{networkData?.edges.length ? (networkData.edges.reduce((sum, edge) => sum + edge.trust_level, 0) / networkData.edges.length).toFixed(3) : '0.000'}</span>
              </div>
              <div className="flex justify-between">
                <span className="text-sm text-secondary-400">Avg Interactions</span>
                <span className="text-sm text-white">{networkData?.edges.length ? (networkData.edges.reduce((sum, edge) => sum + edge.interaction_count, 0) / networkData.edges.length).toFixed(1) : '0.0'}</span>
              </div>
            </div>
          </div>
        </div>
      </motion.div>
    </div>
  )
}

export default Network