#!/bin/bash

# Development startup script for The Cognisphere

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if we're in the right directory
if [ ! -f "README.md" ]; then
    print_error "Please run this script from the project root directory"
    exit 1
fi

print_status "🚀 Starting The Cognisphere development environment..."

# Create necessary directories
print_status "Creating directories..."
mkdir -p snapshots
mkdir -p logs
mkdir -p data

# Check Python version
print_status "Checking Python version..."
python_version=$(python3 --version 2>&1 | awk '{print $2}' | cut -d. -f1,2)
required_version="3.8"

if [ "$(printf '%s\n' "$required_version" "$python_version" | sort -V | head -n1)" != "$required_version" ]; then
    print_error "Python 3.8+ is required. Found: $python_version"
    exit 1
fi

print_success "Python version check passed: $python_version"

# Install backend dependencies
print_status "Installing backend dependencies..."
cd backend

if [ ! -d "venv" ]; then
    print_status "Creating virtual environment..."
    python3 -m venv venv
fi

source venv/bin/activate

print_status "Installing Python packages..."
pip install --upgrade pip
pip install -r requirements.txt

print_success "Backend dependencies installed"

# Install frontend dependencies
print_status "Installing frontend dependencies..."
cd ../frontend

if [ ! -d "node_modules" ]; then
    print_status "Installing Node.js packages..."
    npm install
fi

print_success "Frontend dependencies installed"

# Go back to project root
cd ..

# Check for Docker
if command -v docker &> /dev/null && command -v docker-compose &> /dev/null; then
    print_status "Docker found. You can use 'docker compose up' to run the full stack."
else
    print_warning "Docker not found. You'll need to run backend and frontend separately."
fi

# Create sample stimuli file
print_status "Creating sample stimuli file..."
cat > data/stimuli.sample.json << 'EOF'
[
  {
    "type": "heat_wave",
    "title": "Heat Wave Event",
    "description": "A prolonged heat wave affects resource production",
    "duration": 15,
    "intensity": 1.2,
    "resource_effects": {
      "food": 0.8,
      "energy": 0.9
    },
    "social_effects": {
      "cooperation_penalty": 0.1
    }
  },
  {
    "type": "meme_eruption",
    "title": "Viral Meme Spreads",
    "description": "A new cultural meme spreads rapidly through the population",
    "duration": 10,
    "intensity": 0.8,
    "cultural_effects": {
      "cultural_cohesion": 0.3,
      "myth_influence": 0.2
    }
  },
  {
    "type": "resource_discovery",
    "title": "New Resource Discovered",
    "description": "A new type of resource is discovered",
    "duration": 20,
    "intensity": 1.0,
    "resource_effects": {
      "artifacts": 1.5,
      "influence": 1.3
    }
  }
]
EOF

print_success "Sample stimuli file created"

# Create development configuration
print_status "Creating development configuration..."
cat > .env.development << 'EOF'
# Development environment variables
NODE_ENV=development
VITE_API_URL=http://localhost:8000
PYTHONPATH=./backend
SIMULATION_SEED=42
SIMULATION_AGENTS=300
SIMULATION_TICKS=1000
LLM_MODE=mock
MEMORY_BACKEND=networkx
VECTOR_BACKEND=faiss
EOF

print_success "Development configuration created"

# Make scripts executable
print_status "Making scripts executable..."
chmod +x scripts/*.py
chmod +x scripts/*.sh

print_success "Scripts made executable"

# Print usage instructions
echo ""
print_success "🎉 Development environment setup complete!"
echo ""
echo "To start the development servers:"
echo ""
echo "  Backend (Python/FastAPI):"
echo "    cd backend && source venv/bin/activate && python app.py"
echo ""
echo "  Frontend (React/Vite):"
echo "    cd frontend && npm run dev"
echo ""
echo "  Full stack with Docker:"
echo "    docker compose up --build"
echo ""
echo "To run a simulation:"
echo "    python scripts/seed_and_run.py --preset lab --ticks 300"
echo ""
echo "To run benchmarks:"
echo "    python scripts/seed_and_run.py --benchmark --runs 5"
echo ""
echo "Access points:"
echo "  Frontend: http://localhost:5173"
echo "  Backend API: http://localhost:8000"
echo "  API Docs: http://localhost:8000/docs"
echo ""
print_status "Happy coding! 🧠"
