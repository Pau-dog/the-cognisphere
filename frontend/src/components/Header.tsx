import React from 'react'
import { Menu, Activity, Wifi, WifiOff } from 'lucide-react'
import { useSimulation } from '../state/SimulationContext'

interface HeaderProps {
  onMenuClick: () => void
}

const Header: React.FC<HeaderProps> = ({ onMenuClick }) => {
  const { state } = useSimulation()

  return (
    <header className="bg-secondary-900 border-b border-secondary-800">
      <div className="px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">
          {/* Mobile menu button */}
          <button
            onClick={onMenuClick}
            className="lg:hidden p-2 rounded-md text-secondary-400 hover:text-secondary-200 hover:bg-secondary-800"
          >
            <Menu className="w-6 h-6" />
          </button>

          {/* Title */}
          <div className="flex-1 lg:flex-none">
            <h1 className="text-xl font-semibold text-white">
              The Cognisphere
            </h1>
          </div>

          {/* Status indicators */}
          <div className="flex items-center space-x-4">
            {/* Connection status */}
            <div className="flex items-center space-x-2">
              {state.connected ? (
                <Wifi className="w-4 h-4 text-green-400" />
              ) : (
                <WifiOff className="w-4 h-4 text-red-400" />
              )}
              <span className="text-sm text-secondary-300">
                {state.connected ? 'Connected' : 'Disconnected'}
              </span>
            </div>

            {/* Simulation status */}
            {state.status && (
              <div className="flex items-center space-x-2">
                <Activity className="w-4 h-4 text-primary-400" />
                <span className="text-sm text-secondary-300">
                  {state.status.state} • Tick {state.status.current_tick || 0}
                </span>
              </div>
            )}

            {/* Loading indicator */}
            {state.loading && (
              <div className="flex items-center space-x-2">
                <div className="spinner" />
                <span className="text-sm text-secondary-300">Loading...</span>
              </div>
            )}
          </div>
        </div>
      </div>
    </header>
  )
}

export default Header
