import React from 'react'
import { motion } from 'framer-motion'
import { Brain, Users, Network, TrendingUp, BookOpen, Code, Zap } from 'lucide-react'

const About: React.FC = () => {
  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-purple-900 to-slate-900">
      <div className="container mx-auto px-4 py-8">
        {/* Header */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6 }}
          className="text-center mb-12"
        >
          <h1 className="text-5xl font-bold text-white mb-4">
            The Cognisphere
          </h1>
          <p className="text-xl text-gray-300 max-w-3xl mx-auto">
            An experimental simulation platform that explores emergent intelligence through multi-agent systems
          </p>
        </motion.div>

        {/* Main Content */}
        <div className="grid lg:grid-cols-2 gap-8 mb-12">
          {/* What Makes It Unique */}
          <motion.div
            initial={{ opacity: 0, x: -20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ duration: 0.6, delay: 0.2 }}
            className="bg-white/10 backdrop-blur-sm rounded-lg p-6"
          >
            <h2 className="text-2xl font-bold text-white mb-4 flex items-center">
              <Brain className="mr-3 text-purple-400" />
              What Makes It Unique
            </h2>
            <div className="space-y-4">
              <div>
                <h3 className="text-lg font-semibold text-purple-300 mb-2">Emergent Intelligence</h3>
                <p className="text-gray-300">
                  Unlike traditional simulations with hard-coded behaviors, agents develop their own strategies, 
                  relationships, and cultural norms through interaction and experience.
                </p>
              </div>
              <div>
                <h3 className="text-lg font-semibold text-purple-300 mb-2">Cultural Evolution</h3>
                <p className="text-gray-300">
                  Agents create myths, develop slang, establish social norms, and form institutions that 
                  persist and evolve over time. Language itself drifts and mutates.
                </p>
              </div>
              <div>
                <h3 className="text-lg font-semibold text-purple-300 mb-2">Economic Dynamics</h3>
                <p className="text-gray-300">
                  A fully functional economy emerges from agent interactions, including trade negotiations, 
                  resource management, and market dynamics.
                </p>
              </div>
            </div>
          </motion.div>

          {/* Core Concepts */}
          <motion.div
            initial={{ opacity: 0, x: 20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ duration: 0.6, delay: 0.4 }}
            className="bg-white/10 backdrop-blur-sm rounded-lg p-6"
          >
            <h2 className="text-2xl font-bold text-white mb-4 flex items-center">
              <Network className="mr-3 text-blue-400" />
              Core Concepts
            </h2>
            <div className="space-y-4">
              <div>
                <h3 className="text-lg font-semibold text-blue-300 mb-2">Agent Personality</h3>
                <p className="text-gray-300">
                  Each agent has a unique personality profile (OCEAN traits) that influences behavior, 
                  decision-making, and social interactions.
                </p>
              </div>
              <div>
                <h3 className="text-lg font-semibold text-blue-300 mb-2">Memory Systems</h3>
                <p className="text-gray-300">
                  Agents maintain episodic memory (events), semantic memory (concepts), and social memory 
                  (relationships) using graph and vector databases.
                </p>
              </div>
              <div>
                <h3 className="text-lg font-semibold text-blue-300 mb-2">Institutional Formation</h3>
                <p className="text-gray-300">
                  Agents can create lasting institutions like councils, temples, and governance systems 
                  that persist beyond individual lifespans.
                </p>
              </div>
            </div>
          </motion.div>
        </div>

        {/* Applications */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6, delay: 0.6 }}
          className="bg-white/10 backdrop-blur-sm rounded-lg p-6 mb-12"
        >
          <h2 className="text-2xl font-bold text-white mb-6 flex items-center">
            <BookOpen className="mr-3 text-green-400" />
            Applications
          </h2>
          <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-6">
            <div className="text-center">
              <div className="bg-green-500/20 rounded-full p-4 w-16 h-16 mx-auto mb-3 flex items-center justify-center">
                <TrendingUp className="text-green-400 text-2xl" />
              </div>
              <h3 className="text-lg font-semibold text-green-300 mb-2">Research</h3>
              <p className="text-gray-300 text-sm">
                Study emergent behavior, cultural evolution, economic dynamics, and social network formation.
              </p>
            </div>
            <div className="text-center">
              <div className="bg-blue-500/20 rounded-full p-4 w-16 h-16 mx-auto mb-3 flex items-center justify-center">
                <BookOpen className="text-blue-400 text-2xl" />
              </div>
              <h3 className="text-lg font-semibold text-blue-300 mb-2">Education</h3>
              <p className="text-gray-300 text-sm">
                Understand complex systems, agent-based modeling, and emergent intelligence concepts.
              </p>
            </div>
            <div className="text-center">
              <div className="bg-purple-500/20 rounded-full p-4 w-16 h-16 mx-auto mb-3 flex items-center justify-center">
                <Users className="text-purple-400 text-2xl" />
              </div>
              <h3 className="text-lg font-semibold text-purple-300 mb-2">Entertainment</h3>
              <p className="text-gray-300 text-sm">
                Watch fascinating civilizations develop, collapse, and evolve in unexpected ways.
              </p>
            </div>
            <div className="text-center">
              <div className="bg-orange-500/20 rounded-full p-4 w-16 h-16 mx-auto mb-3 flex items-center justify-center">
                <Code className="text-orange-400 text-2xl" />
              </div>
              <h3 className="text-lg font-semibold text-orange-300 mb-2">AI Development</h3>
              <p className="text-gray-300 text-sm">
                Explore how simple rules can lead to complex, intelligent-seeming behaviors.
              </p>
            </div>
          </div>
        </motion.div>

        {/* Technical Innovation */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6, delay: 0.8 }}
          className="bg-white/10 backdrop-blur-sm rounded-lg p-6"
        >
          <h2 className="text-2xl font-bold text-white mb-6 flex items-center">
            <Zap className="mr-3 text-yellow-400" />
            Technical Innovation
          </h2>
          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
            <div className="bg-gradient-to-r from-purple-500/20 to-blue-500/20 rounded-lg p-4">
              <h3 className="text-lg font-semibold text-white mb-2">Graph Databases</h3>
              <p className="text-gray-300 text-sm">Neo4j for relationship modeling and social networks</p>
            </div>
            <div className="bg-gradient-to-r from-blue-500/20 to-green-500/20 rounded-lg p-4">
              <h3 className="text-lg font-semibold text-white mb-2">Vector Databases</h3>
              <p className="text-gray-300 text-sm">FAISS for semantic memory and knowledge retrieval</p>
            </div>
            <div className="bg-gradient-to-r from-green-500/20 to-yellow-500/20 rounded-lg p-4">
              <h3 className="text-lg font-semibold text-white mb-2">Real-time Visualization</h3>
              <p className="text-gray-300 text-sm">Interactive network graphs and live monitoring</p>
            </div>
            <div className="bg-gradient-to-r from-yellow-500/20 to-orange-500/20 rounded-lg p-4">
              <h3 className="text-lg font-semibold text-white mb-2">Scalable Architecture</h3>
              <p className="text-gray-300 text-sm">Supporting thousands of agents simultaneously</p>
            </div>
            <div className="bg-gradient-to-r from-orange-500/20 to-red-500/20 rounded-lg p-4">
              <h3 className="text-lg font-semibold text-white mb-2">Deterministic Simulation</h3>
              <p className="text-gray-300 text-sm">Reproducible research with seeded randomness</p>
            </div>
            <div className="bg-gradient-to-r from-red-500/20 to-pink-500/20 rounded-lg p-4">
              <h3 className="text-lg font-semibold text-white mb-2">Live Dashboard</h3>
              <p className="text-gray-300 text-sm">Real-time monitoring and control interface</p>
            </div>
          </div>
        </motion.div>

        {/* Call to Action */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6, delay: 1.0 }}
          className="text-center mt-12"
        >
          <div className="bg-gradient-to-r from-purple-600/20 to-blue-600/20 rounded-lg p-8">
            <h2 className="text-3xl font-bold text-white mb-4">
              Ready to Explore?
            </h2>
            <p className="text-gray-300 mb-6 max-w-2xl mx-auto">
              Start your own civilization simulation and watch emergent intelligence unfold in real-time. 
              Customize agent personalities, cultural parameters, and economic systems to create unique scenarios.
            </p>
            <div className="flex flex-col sm:flex-row gap-4 justify-center">
              <a
                href="/"
                className="bg-purple-600 hover:bg-purple-700 text-white px-6 py-3 rounded-lg font-semibold transition-colors"
              >
                Launch Dashboard
              </a>
              <a
                href="https://github.com/zaydabash/the-cognisphere"
                target="_blank"
                rel="noopener noreferrer"
                className="bg-gray-600 hover:bg-gray-700 text-white px-6 py-3 rounded-lg font-semibold transition-colors"
              >
                View Source Code
              </a>
            </div>
          </div>
        </motion.div>
      </div>
    </div>
  )
}

export default About
