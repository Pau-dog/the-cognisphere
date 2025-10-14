import React from 'react'
import { motion } from 'framer-motion'
import { 
  Brain, 
  Users, 
  Activity, 
  TrendingUp, 
  Globe, 
  Network,
  BarChart3,
  Clock,
  Zap
} from 'lucide-react'
import { useSimulation } from '../state/SimulationContext'

const Dashboard: React.FC = () => {
  const { state } = useSimulation()

  const stats = [
    {
      name: 'Agents',
      value: state.agents.length,
      icon: Users,
      color: 'text-blue-400',
      bgColor: 'bg-blue-500/10',
      change: '+12%',
      changeType: 'positive'
    },
    {
      name: 'Factions',
      value: state.status?.realtime?.faction_count || 0,
      icon: Network,
      color: 'text-purple-400',
      bgColor: 'bg-purple-500/10',
      change: '+3',
      changeType: 'positive'
    },
    {
      name: 'Active Myths',
      value: state.status?.realtime?.myth_count || 0,
      icon: Globe,
      color: 'text-green-400',
      bgColor: 'bg-green-500/10',
      change: '+1',
      changeType: 'positive'
    },
    {
      name: 'Total Trades',
      value: state.status?.realtime?.trade_count || 0,
      icon: TrendingUp,
      color: 'text-yellow-400',
      bgColor: 'bg-yellow-500/10',
      change: '+45',
      changeType: 'positive'
    },
    {
      name: 'Active Events',
      value: state.status?.realtime?.active_events || 0,
      icon: Zap,
      color: 'text-red-400',
      bgColor: 'bg-red-500/10',
      change: '2',
      changeType: 'neutral'
    },
    {
      name: 'Gini Coefficient',
      value: state.economicData?.gini_coefficient?.toFixed(3) || '0.000',
      icon: BarChart3,
      color: 'text-indigo-400',
      bgColor: 'bg-indigo-500/10',
      change: '-0.02',
      changeType: 'positive'
    }
  ]

  const recentMyths = state.culturalData?.myths.slice(0, 3) || []
  const recentNorms = state.culturalData?.norms.slice(0, 3) || []

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold text-white">Dashboard</h1>
          <p className="text-secondary-400 mt-2">
            Real-time overview of your emergent civilization
          </p>
        </div>
        
        <div className="flex items-center space-x-3">
          <div className={`px-3 py-1 rounded-full text-sm font-medium ${
            state.status?.state === 'running' 
              ? 'bg-green-500/20 text-green-400' 
              : state.status?.state === 'paused'
              ? 'bg-yellow-500/20 text-yellow-400'
              : 'bg-gray-500/20 text-gray-400'
          }`}>
            {state.status?.state === 'running' && <Activity className="w-4 h-4 inline mr-1" />}
            {state.status?.state || 'Stopped'}
          </div>
          
          <div className="flex items-center space-x-2 text-sm text-secondary-400">
            <Clock className="w-4 h-4" />
            <span>Tick {state.status?.current_tick || 0}</span>
          </div>
        </div>
      </div>

      {/* Stats Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {stats.map((stat, index) => (
          <motion.div
            key={stat.name}
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: index * 0.1 }}
            className="card p-6"
          >
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm font-medium text-secondary-400">{stat.name}</p>
                <p className="text-2xl font-bold text-white mt-1">{stat.value}</p>
                <p className={`text-xs mt-1 ${
                  stat.changeType === 'positive' ? 'text-green-400' : 
                  stat.changeType === 'negative' ? 'text-red-400' : 
                  'text-secondary-400'
                }`}>
                  {stat.change} from last update
                </p>
              </div>
              <div className={`p-3 rounded-lg ${stat.bgColor}`}>
                <stat.icon className={`w-6 h-6 ${stat.color}`} />
              </div>
            </div>
          </motion.div>
        ))}
      </div>

      {/* Main Content Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Recent Cultural Developments */}
        <motion.div
          initial={{ opacity: 0, x: -20 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ delay: 0.3 }}
          className="card p-6"
        >
          <div className="flex items-center space-x-2 mb-4">
            <Globe className="w-5 h-5 text-green-400" />
            <h2 className="text-lg font-semibold text-white">Recent Cultural Developments</h2>
          </div>
          
          <div className="space-y-4">
            {/* Myths */}
            <div>
              <h3 className="text-sm font-medium text-secondary-300 mb-2">New Myths</h3>
              <div className="space-y-2">
                {recentMyths.length > 0 ? (
                  recentMyths.map((myth) => (
                    <div key={myth.id} className="p-3 bg-secondary-800 rounded-lg">
                      <div className="flex items-start justify-between">
                        <div className="flex-1">
                          <p className="text-sm font-medium text-white">{myth.title}</p>
                          <p className="text-xs text-secondary-400 mt-1">{myth.theme}</p>
                        </div>
                        <div className="text-xs text-secondary-500">
                          {myth.popularity.toFixed(2)}
                        </div>
                      </div>
                    </div>
                  ))
                ) : (
                  <p className="text-sm text-secondary-500">No recent myths</p>
                )}
              </div>
            </div>

            {/* Norms */}
            <div>
              <h3 className="text-sm font-medium text-secondary-300 mb-2">Active Norms</h3>
              <div className="space-y-2">
                {recentNorms.length > 0 ? (
                  recentNorms.map((norm) => (
                    <div key={norm.id} className="p-3 bg-secondary-800 rounded-lg">
                      <div className="flex items-start justify-between">
                        <div className="flex-1">
                          <p className="text-sm font-medium text-white">{norm.title}</p>
                          <p className="text-xs text-secondary-400 mt-1">{norm.norm_type}</p>
                        </div>
                        <div className="text-xs text-secondary-500">
                          {(norm.compliance_rate * 100).toFixed(0)}%
                        </div>
                      </div>
                    </div>
                  ))
                ) : (
                  <p className="text-sm text-secondary-500">No active norms</p>
                )}
              </div>
            </div>
          </div>
        </motion.div>

        {/* Economic Overview */}
        <motion.div
          initial={{ opacity: 0, x: 20 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ delay: 0.4 }}
          className="card p-6"
        >
          <div className="flex items-center space-x-2 mb-4">
            <BarChart3 className="w-5 h-5 text-blue-400" />
            <h2 className="text-lg font-semibold text-white">Economic Overview</h2>
          </div>
          
          <div className="space-y-4">
            {/* Market Prices */}
            {state.economicData?.market_summary?.current_prices && (
              <div>
                <h3 className="text-sm font-medium text-secondary-300 mb-2">Market Prices</h3>
                <div className="grid grid-cols-2 gap-2">
                  {Object.entries(state.economicData.market_summary.current_prices).map(([resource, price]) => (
                    <div key={resource} className="p-2 bg-secondary-800 rounded">
                      <div className="text-xs text-secondary-400 capitalize">{resource}</div>
                      <div className="text-sm font-medium text-white">{price.toFixed(2)}</div>
                    </div>
                  ))}
                </div>
              </div>
            )}

            {/* Trade Activity */}
            <div>
              <h3 className="text-sm font-medium text-secondary-300 mb-2">Trade Activity</h3>
              <div className="space-y-2">
                <div className="flex justify-between text-sm">
                  <span className="text-secondary-400">Active Trades</span>
                  <span className="text-white">{state.economicData?.market_summary?.active_trades || 0}</span>
                </div>
                <div className="flex justify-between text-sm">
                  <span className="text-secondary-400">Completed Trades</span>
                  <span className="text-white">{state.economicData?.market_summary?.completed_trades || 0}</span>
                </div>
                <div className="flex justify-between text-sm">
                  <span className="text-secondary-400">Gini Coefficient</span>
                  <span className="text-white">{state.economicData?.gini_coefficient?.toFixed(3) || 'N/A'}</span>
                </div>
              </div>
            </div>
          </div>
        </motion.div>
      </div>

      {/* Network Overview */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.5 }}
        className="card p-6"
      >
        <div className="flex items-center space-x-2 mb-4">
          <Network className="w-5 h-5 text-purple-400" />
          <h2 className="text-lg font-semibold text-white">Network Overview</h2>
        </div>
        
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          <div className="text-center">
            <div className="text-2xl font-bold text-white">{state.networkData?.nodes.length || 0}</div>
            <div className="text-sm text-secondary-400">Total Agents</div>
          </div>
          <div className="text-center">
            <div className="text-2xl font-bold text-white">{state.networkData?.edges.length || 0}</div>
            <div className="text-sm text-secondary-400">Connections</div>
          </div>
          <div className="text-center">
            <div className="text-2xl font-bold text-white">
              {state.networkData?.nodes.length ? 
                (state.networkData.edges.length / state.networkData.nodes.length).toFixed(2) : 
                '0.00'
              }
            </div>
            <div className="text-sm text-secondary-400">Avg Connections</div>
          </div>
        </div>
      </motion.div>
    </div>
  )
}

export default Dashboard
