# 🧠 The Cognisphere: Emergent Intelligence Civilization Engine

[![CI](https://github.com/zaydbashir/the-cognisphere/actions/workflows/ci.yml/badge.svg)](../../actions/workflows/ci.yml)
[![Release](https://github.com/zaydbashir/the-cognisphere/actions/workflows/release.yml/badge.svg)](../../actions/workflows/release.yml)
[![Pages](https://img.shields.io/badge/Deploy-GitHub%20Pages-222)](../../deployments/activity_log?environment=github-pages)
[![Backend](https://img.shields.io/badge/Deploy-Render-2b2b2b)](https://dashboard.render.com/)
[![Containers](https://ghcr-badge.egpl.dev/zaydbashir/the-cognisphere/latest_tag?label=GHCR)](https://github.com/zaydbashir?tab=packages)

A living ecosystem of cognitive agents that evolve language, culture, alliances, and institutions through emergent dynamics.

## 🌍 Overview

The Cognisphere simulates a digital civilization with hundreds to thousands of lightweight cognitive agents who:
- Evolve language, culture, alliances, norms, and mythology
- Maintain collective memory over simulated decades
- Negotiate, trade, betray, form factions, and build institutions
- React to real-world environmental stimuli
- Produce emergent structure without hard-coded scripts

## 🏗️ Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Frontend      │    │   Backend       │    │   Memory        │
│   React + Vite  │◄──►│   FastAPI       │◄──►│   Neo4j + FAISS │
│   Visualization │    │   Simulation    │    │   Graph + Vector│
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

## 🚀 Quick Start

### Option 1: Interactive Setup (Recommended)
```bash
# Clone and setup
git clone <your-repo-url>
cd the-cognisphere

# Run the interactive quick-start script
chmod +x scripts/quick-start.sh
./scripts/quick-start.sh
```

### Option 2: Direct Deployment
```bash
# Local Development (uses cognisphere.dev domain)
chmod +x scripts/local-dev.sh
./scripts/local-dev.sh

# Docker Development (uses cognisphere.local domain)
docker-compose -f docker/docker-compose.yml up --build

# Production Deployment (uses cognisphere.local with SSL)
chmod +x scripts/deploy.sh
./scripts/deploy.sh
```

### Option 3: One-Command Docker
```bash
# Quick Docker setup
docker-compose -f docker/docker-compose.yml up --build -d

# Run a simulation
python scripts/seed_and_run.py --preset lab --ticks 300 --seed 42
```

## 🌐 Access URLs (No Localhost Issues!)

- **Frontend Dashboard**: `http://cognisphere.local:5173` or `https://cognisphere.local`
- **API Documentation**: `http://cognisphere.local:8000/api/docs`
- **Neo4j Browser**: `http://cognisphere.local:7474`
- **Monitoring**: `http://cognisphere.local:3001` (Grafana)

## 🧠 Core Features

### Agent Cognitive Architecture
- Personality vectors (OCEAN-style)
- Trust calculus and relationship weights
- Ideology vectors for soft alignment
- Language lexicons with drifting slang
- Episodic, semantic, and social memory
- Internal deliberation with RAG from memory graph

### Economy & Social Dynamics
- Resource-based economy (food, energy, artifacts, influence)
- Bilateral negotiation with alternating offers
- Market fallback with double auction clearing
- Alliance/betrayal mechanics with reputation systems
- Faction dynamics and institution formation

### Cultural Evolution
- Language drift with slang mutation and JSD divergence tracking
- Myth generation and canonization
- Norm voting systems with soft penalties
- Cultural diffusion modeled as contagion

### Memory Layer
- Neo4j graph database for relationships and knowledge
- FAISS vector store for semantic retrieval
- Snapshot/rewind capability for time travel
- Deterministic seeded runs for reproducibility

## 📊 Dashboard Features

- Real-time agent network visualization
- Culture timeline with myths, slang, and norms
- Resource and economy panels
- Slang divergence plots
- Simulation control with play/pause/seed
- Snapshot playback capabilities

## 🧪 Testing & Benchmarks

```bash
# Run test suite
python -m pytest backend/tests/

# Performance benchmark
python scripts/seed_and_run.py --preset lab --ticks 300

# Determinism check
python scripts/seed_and_run.py --seed 42 --ticks 100
```

## 🔧 Configuration

| Variable | Default | Description |
|----------|---------|-------------|
| `AGENTS` | 300 | Number of agents in simulation |
| `SEED` | 42 | Random seed for reproducibility |
| `TICK_MS` | 100 | Milliseconds per simulation tick |
| `LLM_MODE` | mock | LLM mode: mock or openai |
| `MEM_BACKEND` | neo4j | Memory backend: neo4j or networkx |
| `VEC_BACKEND` | faiss | Vector backend: faiss or chroma |

## 📁 Project Structure

```
cognisphere/
├── backend/           # FastAPI simulation engine
├── frontend/          # React dashboard
├── docker/            # Containerization
├── scripts/           # Utilities and seeding
├── data/              # Sample stimuli and configs
└── README.md          # This file
```

## 🎯 Acceptance Criteria

- ✅ One-command startup with Docker Compose
- ✅ Working dashboard with emergent myths, slang, alliances
- ✅ Deterministic seeded runs
- ✅ 500+ agent mock runs on laptop
- ✅ Beautiful, clean architecture & documentation

## 🚀 Deployment

### 🌐 Live Deployment

**Frontend (GitHub Pages)**: [https://zaydbashir.github.io/the-cognisphere](https://zaydbashir.github.io/the-cognisphere)

**Backend (Render)**: [https://cognisphere-backend.onrender.com](https://cognisphere-backend.onrender.com)

**API Documentation**: [https://cognisphere-backend.onrender.com/docs](https://cognisphere-backend.onrender.com/docs)

### 🐳 Docker Images

```bash
# Pull latest images
docker pull ghcr.io/zaydbashir/cognisphere-backend:latest
docker pull ghcr.io/zaydbashir/cognisphere-frontend:latest

# Run with Docker Compose
docker-compose up -d
```

### 🔧 Environment Configuration

Copy the example environment files and configure:

```bash
# Backend
cp backend/.env.example backend/.env

# Frontend  
cp frontend/.env.example frontend/.env.local
```

### 📦 Release Process

1. **Tag a release**: `git tag v0.1.0 && git push origin v0.1.0`
2. **Automatic builds**: Docker images pushed to GHCR
3. **Auto-deploy**: Frontend to GitHub Pages, Backend to Render
4. **Health checks**: Automated deployment verification

### 🛠️ CI/CD Pipeline

- **Continuous Integration**: Lint, type-check, tests on every push
- **Release Automation**: Build and push Docker images on tags
- **Auto-Deployment**: Frontend (GitHub Pages) + Backend (Render)
- **Health Monitoring**: Automated deployment verification

## 📄 License

MIT License - See LICENSE file for details.
