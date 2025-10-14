import React from 'react'
import { Link, useLocation } from 'react-router-dom'
import { motion } from 'framer-motion'
import { Brain, X } from 'lucide-react'
import clsx from 'clsx'

interface NavigationItem {
  name: string
  href: string
  icon: React.ComponentType<{ className?: string }>
}

interface SidebarProps {
  navigation: NavigationItem[]
  onClose?: () => void
}

const Sidebar: React.FC<SidebarProps> = ({ navigation, onClose }) => {
  const location = useLocation()

  return (
    <div className="flex flex-col h-full bg-secondary-900 border-r border-secondary-800">
      {/* Logo */}
      <div className="flex items-center justify-between px-6 py-4">
        <div className="flex items-center space-x-3">
          <div className="flex items-center justify-center w-8 h-8 rounded-lg bg-gradient-primary">
            <Brain className="w-5 h-5 text-white" />
          </div>
          <div>
            <h1 className="text-lg font-bold text-white">Cognisphere</h1>
            <p className="text-xs text-secondary-400">Emergent Intelligence</p>
          </div>
        </div>
        {onClose && (
          <button
            onClick={onClose}
            className="lg:hidden p-1 rounded-md text-secondary-400 hover:text-secondary-200 hover:bg-secondary-800"
          >
            <X className="w-5 h-5" />
          </button>
        )}
      </div>

      {/* Navigation */}
      <nav className="flex-1 px-4 py-4 space-y-1">
        {navigation.map((item) => {
          const isActive = location.pathname === item.href
          
          return (
            <Link
              key={item.name}
              to={item.href}
              onClick={onClose}
              className={clsx(
                'group flex items-center px-3 py-2 text-sm font-medium rounded-lg transition-colors',
                isActive
                  ? 'bg-primary-600 text-white'
                  : 'text-secondary-300 hover:bg-secondary-800 hover:text-secondary-100'
              )}
            >
              <motion.div
                whileHover={{ scale: 1.1 }}
                whileTap={{ scale: 0.95 }}
                className="mr-3"
              >
                <item.icon className={clsx(
                  'w-5 h-5',
                  isActive ? 'text-white' : 'text-secondary-400 group-hover:text-secondary-200'
                )} />
              </motion.div>
              {item.name}
              {isActive && (
                <motion.div
                  layoutId="activeTab"
                  className="absolute inset-0 bg-primary-600 rounded-lg -z-10"
                  initial={false}
                  transition={{ type: 'spring', stiffness: 500, damping: 30 }}
                />
              )}
            </Link>
          )
        })}
      </nav>

      {/* Footer */}
      <div className="px-4 py-4 border-t border-secondary-800">
        <div className="text-xs text-secondary-500 text-center">
          <p>The Cognisphere v0.1.0</p>
          <p>Emergent Intelligence Engine</p>
        </div>
      </div>
    </div>
  )
}

export default Sidebar
