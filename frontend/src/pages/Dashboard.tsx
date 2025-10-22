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
import mockData from '../data/mockData'

const Dashboard: React.FC = () => {
  const { state } = useSimulation()
  
  // Use mock data for screenshots
  const useMockData = false
  const data = useMockData ? mockData : state

  const stats = [
    {
      name: 'Agents',
      value: useMockData ? data.status.agents_count : state.agents.length,
      icon: Users,
      color: 'text-blue-400',
      bgColor: 'bg-blue-500/10',
      change: '+12%',
      changeType: 'positive'
    },
    {
      name: 'Factions',
      value: useMockData ? data.status.factions_count : (state.status?.realtime?.faction_count || 0),
      icon: Network,
      color: 'text-purple-400',
      bgColor: 'bg-purple-500/10',
      change: '+3',
      changeType: 'positive'
    },
    {
      name: 'Active Myths',
      value: useMockData ? data.culture.myths.length : (state.status?.realtime?.myth_count || 0),
      icon: Globe,
      color: 'text-green-400',
      bgColor: 'bg-green-500/10',
      change: '+1',
      changeType: 'positive'
    },
    {
      name: 'Total Trades',
      value: useMockData ? data.economy.trades.length : (state.status?.realtime?.trade_count || 0),
      icon: TrendingUp,
      color: 'text-yellow-400',
      bgColor: 'bg-yellow-500/10',
      change: '+45',
      changeType: 'positive'
    },
    {
      name: 'Active Events',
      value: useMockData ? data.status.active_events : (state.status?.realtime?.event_count || 0),
      icon: Activity,
      color: 'text-red-400',
      bgColor: 'bg-red-500/10',
      change: '2',
      changeType: 'neutral'
    },
    {
      name: 'Gini Coefficient',
      value: useMockData ? data.economy.gini_coefficient.toFixed(3) : (state.status?.realtime?.gini_coefficient || 0).toFixed(3),
      icon: BarChart3,
      color: 'text-indigo-400',
      bgColor: 'bg-indigo-500/10',
      change: '-0.02',
      changeType: 'positive'
    }
  ]

  return (
    <div className="min-h-screen bg-gray-900 text-white">
      {/* Header */}
      <div className="bg-gray-800 border-b border-gray-700">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex items-center justify-between h-16">
            <div className="flex items-center space-x-4">
              <Brain className="h-8 w-8 text-blue-400" />
              <div>
                <h1 className="text-xl font-bold">Dashboard</h1>
                <p className="text-sm text-gray-400">Real-time overview of your emergent civilization</p>
              </div>
            </div>
            <div className="flex items-center space-x-4">
              <div className="flex items-center space-x-2">
                <div className={`w-2 h-2 rounded-full ${useMockData ? 'bg-green-400' : 'bg-red-400'}`} />
                <span className="text-sm text-gray-300">
                  {useMockData ? 'Running' : 'Stopped'}
                </span>
              </div>
              <div className="flex items-center space-x-2 text-sm text-gray-400">
                <Clock className="h-4 w-4" />
                <span>Tick {useMockData ? data.status.current_tick : 0}</span>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Stats Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 mb-8">
          {stats.map((stat, index) => (
            <motion.div
              key={stat.name}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: index * 0.1 }}
              className={`${stat.bgColor} rounded-lg p-6 border border-gray-700`}
            >
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm font-medium text-gray-300">{stat.name}</p>
                  <p className="text-2xl font-bold text-white">{stat.value}</p>
                  <p className={`text-sm ${stat.changeType === 'positive' ? 'text-green-400' : stat.changeType === 'negative' ? 'text-red-400' : 'text-gray-400'}`}>
                    {stat.change} from last update
                  </p>
                </div>
                <stat.icon className={`h-8 w-8 ${stat.color}`} />
              </div>
            </motion.div>
          ))}
        </div>

        {/* Main Content Grid */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          {/* Cultural Developments */}
          <motion.div
            initial={{ opacity: 0, x: -20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ delay: 0.3 }}
            className="bg-gray-800 rounded-lg border border-gray-700 p-6"
          >
            <div className="flex items-center space-x-3 mb-6">
              <Globe className="h-6 w-6 text-green-400" />
              <h2 className="text-lg font-semibold">Recent Cultural Developments</h2>
            </div>
            
            <div className="space-y-6">
              <div>
                <h3 className="text-sm font-medium text-gray-300 mb-3">New Myths</h3>
                <div className="space-y-2">
                  {useMockData ? data.culture.myths.slice(0, 2).map((myth) => (
                    <div key={myth.id} className="bg-gray-700 rounded p-3">
                      <p className="text-sm font-medium">{myth.title}</p>
                      <p className="text-xs text-gray-400">by {myth.creator} • Popularity: {(myth.popularity * 100).toFixed(0)}%</p>
                    </div>
                  )) : (
                    <p className="text-gray-400 text-sm">No recent myths</p>
                  )}
                </div>
              </div>
              
              <div>
                <h3 className="text-sm font-medium text-gray-300 mb-3">Active Norms</h3>
                <div className="space-y-2">
                  {useMockData ? data.culture.norms.slice(0, 2).map((norm) => (
                    <div key={norm.id} className="bg-gray-700 rounded p-3">
                      <p className="text-sm font-medium">{norm.description}</p>
                      <p className="text-xs text-gray-400">
                        {norm.votes_for} for, {norm.votes_against} against • Enforcement: {(norm.enforcement * 100).toFixed(0)}%
                      </p>
                    </div>
                  )) : (
                    <p className="text-gray-400 text-sm">No active norms</p>
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
            className="bg-gray-800 rounded-lg border border-gray-700 p-6"
          >
            <div className="flex items-center space-x-3 mb-6">
              <TrendingUp className="h-6 w-6 text-yellow-400" />
              <h2 className="text-lg font-semibold">Economic Overview</h2>
            </div>
            
            <div>
              <h3 className="text-sm font-medium text-gray-300 mb-3">Trade Activity</h3>
              <div className="grid grid-cols-3 gap-4 text-center">
                <div className="bg-gray-700 rounded p-3">
                  <p className="text-lg font-bold text-white">{useMockData ? data.economy.trades.length : 0}</p>
                  <p className="text-xs text-gray-400">Active Trades</p>
                </div>
                <div className="bg-gray-700 rounded p-3">
                  <p className="text-lg font-bold text-white">{useMockData ? data.economy.trades.length * 3 : 0}</p>
                  <p className="text-xs text-gray-400">Completed Trades</p>
                </div>
                <div className="bg-gray-700 rounded p-3">
                  <p className="text-lg font-bold text-white">{useMockData ? data.economy.gini_coefficient.toFixed(2) : 'N/A'}</p>
                  <p className="text-xs text-gray-400">Gini Coefficient</p>
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
          className="mt-8 bg-gray-800 rounded-lg border border-gray-700 p-6"
        >
          <div className="flex items-center space-x-3 mb-6">
            <Network className="h-6 w-6 text-purple-400" />
            <h2 className="text-lg font-semibold">Network Overview</h2>
          </div>
          
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
            <div className="text-center">
              <p className="text-2xl font-bold text-white">{useMockData ? data.status.agents_count : 0}</p>
              <p className="text-sm text-gray-400">Total Agents</p>
            </div>
            <div className="text-center">
              <p className="text-2xl font-bold text-white">{useMockData ? data.network.connections.length : 0}</p>
              <p className="text-sm text-gray-400">Connections</p>
            </div>
            <div className="text-center">
              <p className="text-2xl font-bold text-white">{useMockData ? (data.network.connections.length / data.status.agents_count).toFixed(2) : '0.00'}</p>
              <p className="text-sm text-gray-400">Avg Connections</p>
            </div>
            <div className="text-center">
              <p className="text-2xl font-bold text-white">{useMockData ? data.status.factions_count : 0}</p>
              <p className="text-sm text-gray-400">Factions</p>
            </div>
          </div>
        </motion.div>
      </div>
    </div>
  )
}

export default Dashboard