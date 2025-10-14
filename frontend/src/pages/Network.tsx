import React, { useRef, useEffect, useState } from 'react'
import { motion } from 'framer-motion'
import { Network as NetworkIcon, Users, Link, Eye, EyeOff } from 'lucide-react'
import { useSimulation } from '../state/SimulationContext'
import CytoscapeComponent from 'react-cytoscapejs'

const Network: React.FC = () => {
  const { state } = useSimulation()
  const [showLabels, setShowLabels] = useState(true)
  const [showFactions, setShowFactions] = useState(true)
  const [selectedNode, setSelectedNode] = useState<any>(null)

  const networkData = state.networkData

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
    name: 'force',
    fit: true,
    padding: 30,
    animate: true,
    animationDuration: 1000,
    nodeRepulsion: 4000,
    edgeLength: 100,
    randomize: false
  }

  const stylesheet = [
    {
      selector: 'node',
      style: {
        'background-color': '#3b82f6',
        'label': 'data(label)',
        'width': 20,
        'height': 20,
        'font-size': '12px',
        'color': '#f8fafc',
        'text-outline-width': 2,
        'text-outline-color': '#1e293b'
      }
    },
    {
      selector: 'node.faction-member',
      style: {
        'background-color': '#8b5cf6',
        'border-width': 2,
        'border-color': '#a855f7'
      }
    },
    {
      selector: 'node:selected',
      style: {
        'background-color': '#f59e0b',
        'border-width': 3,
        'border-color': '#fbbf24'
      }
    },
    {
      selector: 'edge',
      style: {
        'width': 2,
        'line-color': '#64748b',
        'opacity': 0.6,
        'curve-style': 'bezier'
      }
    },
    {
      selector: 'edge.positive-trust',
      style: {
        'line-color': '#10b981',
        'opacity': 0.8
      }
    },
    {
      selector: 'edge.negative-trust',
      style: {
        'line-color': '#ef4444',
        'opacity': 0.6
      }
    }
  ]

  const handleNodeTap = (event: any) => {
    const node = event.target
    if (node.isNode()) {
      setSelectedNode(node.data())
    }
  }

  const handleBackgroundTap = () => {
    setSelectedNode(null)
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
          <div className="flex items-center space-x-2">
            <button
              onClick={() => setShowLabels(!showLabels)}
              className={`btn ${showLabels ? 'btn-primary' : 'btn-ghost'}`}
            >
              {showLabels ? <Eye className="w-4 h-4" /> : <EyeOff className="w-4 h-4" />}
              <span className="ml-2">Labels</span>
            </button>
            
            <button
              onClick={() => setShowFactions(!showFactions)}
              className={`btn ${showFactions ? 'btn-primary' : 'btn-ghost'}`}
            >
              <Users className="w-4 h-4" />
              <span className="ml-2">Factions</span>
            </button>
          </div>
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
              <p className="text-2xl font-bold text-white">{networkData?.nodes.length || 0}</p>
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
              <p className="text-2xl font-bold text-white">{networkData?.edges.length || 0}</p>
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
              <p className="text-2xl font-bold text-white">
                {networkData?.nodes.length ? 
                  (networkData.edges.length / networkData.nodes.length).toFixed(2) : 
                  '0.00'
                }
              </p>
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
              <p className="text-2xl font-bold text-white">
                {new Set(networkData?.nodes.filter(n => n.faction_id).map(n => n.faction_id)).size || 0}
              </p>
            </div>
          </div>
        </motion.div>
      </div>

      {/* Network Visualization */}
      <div className="grid grid-cols-1 lg:grid-cols-4 gap-6">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.4 }}
          className="lg:col-span-3"
        >
          <div className="card p-6">
            <h2 className="text-lg font-semibold text-white mb-4">Network Graph</h2>
            
            {networkData && networkData.nodes.length > 0 ? (
              <div className="h-96 border border-secondary-700 rounded-lg overflow-hidden">
                <CytoscapeComponent
                  elements={elements}
                  style={{ width: '100%', height: '100%' }}
                  layout={layout}
                  stylesheet={stylesheet}
                  cy={(cy) => {
                    cy.on('tap', 'node', handleNodeTap)
                    cy.on('tap', handleBackgroundTap)
                  }}
                />
              </div>
            ) : (
              <div className="h-96 border border-secondary-700 rounded-lg flex items-center justify-center">
                <div className="text-center">
                  <NetworkIcon className="w-12 h-12 text-secondary-600 mx-auto mb-4" />
                  <p className="text-secondary-400">No network data available</p>
                  <p className="text-sm text-secondary-500 mt-1">Start a simulation to see agent connections</p>
                </div>
              </div>
            )}
          </div>
        </motion.div>

        {/* Node Details */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.5 }}
          className="lg:col-span-1"
        >
          <div className="card p-6">
            <h2 className="text-lg font-semibold text-white mb-4">Agent Details</h2>
            
            {selectedNode ? (
              <div className="space-y-4">
                <div>
                  <h3 className="font-medium text-white">{selectedNode.label || selectedNode.id}</h3>
                  <p className="text-sm text-secondary-400">Agent ID: {selectedNode.id}</p>
                </div>

                {selectedNode.faction && (
                  <div>
                    <h4 className="text-sm font-medium text-secondary-300">Faction</h4>
                    <p className="text-sm text-white">{selectedNode.faction}</p>
                  </div>
                )}

                <div>
                  <h4 className="text-sm font-medium text-secondary-300">Influence</h4>
                  <p className="text-sm text-white">{selectedNode.influence?.toFixed(3) || 'N/A'}</p>
                </div>

                <div>
                  <h4 className="text-sm font-medium text-secondary-300">Satisfaction</h4>
                  <p className="text-sm text-white">{selectedNode.satisfaction?.toFixed(3) || 'N/A'}</p>
                </div>

                {selectedNode.personality && (
                  <div>
                    <h4 className="text-sm font-medium text-secondary-300">Personality</h4>
                    <div className="space-y-1 text-xs">
                      <div className="flex justify-between">
                        <span className="text-secondary-400">Openness</span>
                        <span className="text-white">{selectedNode.personality.openness?.toFixed(2) || 'N/A'}</span>
                      </div>
                      <div className="flex justify-between">
                        <span className="text-secondary-400">Conscientiousness</span>
                        <span className="text-white">{selectedNode.personality.conscientiousness?.toFixed(2) || 'N/A'}</span>
                      </div>
                      <div className="flex justify-between">
                        <span className="text-secondary-400">Extraversion</span>
                        <span className="text-white">{selectedNode.personality.extraversion?.toFixed(2) || 'N/A'}</span>
                      </div>
                      <div className="flex justify-between">
                        <span className="text-secondary-400">Agreeableness</span>
                        <span className="text-white">{selectedNode.personality.agreeableness?.toFixed(2) || 'N/A'}</span>
                      </div>
                      <div className="flex justify-between">
                        <span className="text-secondary-400">Neuroticism</span>
                        <span className="text-white">{selectedNode.personality.neuroticism?.toFixed(2) || 'N/A'}</span>
                      </div>
                    </div>
                  </div>
                )}
              </div>
            ) : (
              <div className="text-center py-8">
                <Users className="w-8 h-8 text-secondary-600 mx-auto mb-2" />
                <p className="text-sm text-secondary-400">Click on an agent to see details</p>
              </div>
            )}
          </div>
        </motion.div>
      </div>

      {/* Network Analysis */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.6 }}
        className="card p-6"
      >
        <h2 className="text-lg font-semibold text-white mb-4">Network Analysis</h2>
        
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          <div>
            <h3 className="text-sm font-medium text-secondary-300 mb-2">Connection Types</h3>
            <div className="space-y-2">
              <div className="flex items-center justify-between">
                <div className="flex items-center space-x-2">
                  <div className="w-3 h-3 bg-green-500 rounded-full" />
                  <span className="text-sm text-secondary-400">Positive Trust</span>
                </div>
                <span className="text-sm text-white">
                  {networkData?.edges.filter(e => e.trust_level > 0).length || 0}
                </span>
              </div>
              <div className="flex items-center justify-between">
                <div className="flex items-center space-x-2">
                  <div className="w-3 h-3 bg-red-500 rounded-full" />
                  <span className="text-sm text-secondary-400">Negative Trust</span>
                </div>
                <span className="text-sm text-white">
                  {networkData?.edges.filter(e => e.trust_level < 0).length || 0}
                </span>
              </div>
              <div className="flex items-center justify-between">
                <div className="flex items-center space-x-2">
                  <div className="w-3 h-3 bg-gray-500 rounded-full" />
                  <span className="text-sm text-secondary-400">Neutral</span>
                </div>
                <span className="text-sm text-white">
                  {networkData?.edges.filter(e => e.trust_level === 0).length || 0}
                </span>
              </div>
            </div>
          </div>

          <div>
            <h3 className="text-sm font-medium text-secondary-300 mb-2">Faction Distribution</h3>
            <div className="space-y-2">
              <div className="flex justify-between text-sm">
                <span className="text-secondary-400">Faction Members</span>
                <span className="text-white">
                  {networkData?.nodes.filter(n => n.faction_id).length || 0}
                </span>
              </div>
              <div className="flex justify-between text-sm">
                <span className="text-secondary-400">Independent Agents</span>
                <span className="text-white">
                  {networkData?.nodes.filter(n => !n.faction_id).length || 0}
                </span>
              </div>
              <div className="flex justify-between text-sm">
                <span className="text-secondary-400">Total Factions</span>
                <span className="text-white">
                  {new Set(networkData?.nodes.filter(n => n.faction_id).map(n => n.faction_id)).size || 0}
                </span>
              </div>
            </div>
          </div>

          <div>
            <h3 className="text-sm font-medium text-secondary-300 mb-2">Network Metrics</h3>
            <div className="space-y-2">
              <div className="flex justify-between text-sm">
                <span className="text-secondary-400">Density</span>
                <span className="text-white">
                  {networkData?.nodes.length ? 
                    (networkData.edges.length / (networkData.nodes.length * (networkData.nodes.length - 1))).toFixed(4) : 
                    '0.0000'
                  }
                </span>
              </div>
              <div className="flex justify-between text-sm">
                <span className="text-secondary-400">Avg Trust</span>
                <span className="text-white">
                  {networkData?.edges.length ? 
                    (networkData.edges.reduce((sum, e) => sum + e.trust_level, 0) / networkData.edges.length).toFixed(3) : 
                    '0.000'
                  }
                </span>
              </div>
              <div className="flex justify-between text-sm">
                <span className="text-secondary-400">Avg Interactions</span>
                <span className="text-white">
                  {networkData?.edges.length ? 
                    (networkData.edges.reduce((sum, e) => sum + e.interaction_count, 0) / networkData.edges.length).toFixed(1) : 
                    '0.0'
                  }
                </span>
              </div>
            </div>
          </div>
        </div>
      </motion.div>
    </div>
  )
}

export default Network
