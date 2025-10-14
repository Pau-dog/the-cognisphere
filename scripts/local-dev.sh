#!/bin/bash

# Local development script with proper domain setup
# Avoids localhost issues by using a dedicated domain

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

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

# Configuration
DOMAIN="cognisphere.dev"
BACKEND_PORT="8001"
FRONTEND_PORT="3001"

print_status "🛠️  Starting The Cognisphere in development mode..."

# Check prerequisites
check_prerequisites() {
    print_status "Checking prerequisites..."
    
    if ! command -v python3 &> /dev/null; then
        print_error "Python 3 is not installed. Please install Python 3 first."
        exit 1
    fi
    
    if ! command -v node &> /dev/null; then
        print_error "Node.js is not installed. Please install Node.js first."
        exit 1
    fi
    
    if ! command -v npm &> /dev/null; then
        print_error "npm is not installed. Please install npm first."
        exit 1
    fi
    
    print_success "Prerequisites check passed"
}

# Setup development domain
setup_dev_domain() {
    print_status "Setting up development domain: $DOMAIN"
    
    # Add domain to /etc/hosts if not already present
    if ! grep -q "$DOMAIN" /etc/hosts; then
        print_status "Adding $DOMAIN to /etc/hosts..."
        echo "127.0.0.1 $DOMAIN" | sudo tee -a /etc/hosts
        print_success "Development domain added to /etc/hosts"
    else
        print_status "Development domain already exists in /etc/hosts"
    fi
}

# Setup environment for development
setup_dev_environment() {
    print_status "Setting up development environment..."
    
    # Backend environment
    cat > backend/.env << EOF
# Development Environment
PYTHONPATH=/app
SIMULATION_SEED=42
SIMULATION_AGENTS=100
SIMULATION_TICKS=1000
LLM_MODE=mock
MEMORY_BACKEND=networkx
VECTOR_BACKEND=faiss
LOG_LEVEL=DEBUG
ENABLE_METRICS=false

# Database URLs (local development)
DATABASE_URL=sqlite:///./cognisphere_dev.db
NEO4J_URI=bolt://localhost:7687
NEO4J_AUTH=neo4j/dev_password

# API Configuration
API_HOST=0.0.0.0
API_PORT=$BACKEND_PORT
CORS_ORIGINS=["http://$DOMAIN:$FRONTEND_PORT", "https://$DOMAIN:$FRONTEND_PORT"]
EOF

    # Frontend environment
    cat > frontend/.env.local << EOF
# Development Environment
VITE_API_URL=http://$DOMAIN:$BACKEND_PORT
VITE_WS_URL=ws://$DOMAIN:$BACKEND_PORT
VITE_ENVIRONMENT=development
VITE_DEBUG=true
EOF

    print_success "Development environment configured"
}

# Install dependencies
install_dependencies() {
    print_status "Installing dependencies..."
    
    # Backend dependencies
    if [ ! -d "backend/venv" ]; then
        print_status "Creating Python virtual environment..."
        cd backend
        python3 -m venv venv
        source venv/bin/activate
        pip install -r requirements.txt
        cd ..
        print_success "Backend dependencies installed"
    else
        print_status "Backend virtual environment already exists"
    fi
    
    # Frontend dependencies
    if [ ! -d "frontend/node_modules" ]; then
        print_status "Installing frontend dependencies..."
        cd frontend
        npm install
        cd ..
        print_success "Frontend dependencies installed"
    else
        print_status "Frontend dependencies already installed"
    fi
}

# Start Neo4j (if available)
start_neo4j() {
    print_status "Starting Neo4j database..."
    
    if command -v neo4j &> /dev/null; then
        if ! pgrep -f "neo4j" > /dev/null; then
            neo4j start || print_warning "Could not start Neo4j (will use NetworkX fallback)"
        else
            print_status "Neo4j is already running"
        fi
    else
        print_warning "Neo4j not installed, will use NetworkX fallback"
    fi
}

# Start backend
start_backend() {
    print_status "Starting backend server..."
    
    cd backend
    source venv/bin/activate
    
    # Start backend in background
    nohup python -m uvicorn app:app --host 0.0.0.0 --port $BACKEND_PORT --reload > ../logs/backend.log 2>&1 &
    BACKEND_PID=$!
    echo $BACKEND_PID > ../logs/backend.pid
    cd ..
    
    print_success "Backend server started (PID: $BACKEND_PID)"
}

# Start frontend
start_frontend() {
    print_status "Starting frontend development server..."
    
    cd frontend
    
    # Start frontend in background
    nohup npm run dev -- --host 0.0.0.0 --port $FRONTEND_PORT > ../logs/frontend.log 2>&1 &
    FRONTEND_PID=$!
    echo $FRONTEND_PID > ../logs/frontend.pid
    cd ..
    
    print_success "Frontend server started (PID: $FRONTEND_PID)"
}

# Wait for services
wait_for_services() {
    print_status "Waiting for services to be ready..."
    
    # Wait for backend
    print_status "Waiting for backend API..."
    timeout=30
    while [ $timeout -gt 0 ]; do
        if curl -f -s "http://$DOMAIN:$BACKEND_PORT/api/health" > /dev/null 2>&1; then
            print_success "Backend API is ready"
            break
        fi
        sleep 1
        timeout=$((timeout - 1))
    done
    
    if [ $timeout -le 0 ]; then
        print_error "Backend API failed to start within timeout"
        exit 1
    fi
    
    # Wait for frontend
    print_status "Waiting for frontend..."
    timeout=30
    while [ $timeout -gt 0 ]; do
        if curl -f -s "http://$DOMAIN:$FRONTEND_PORT" > /dev/null 2>&1; then
            print_success "Frontend is ready"
            break
        fi
        sleep 1
        timeout=$((timeout - 1))
    done
    
    if [ $timeout -le 0 ]; then
        print_error "Frontend failed to start within timeout"
        exit 1
    fi
}

# Initialize simulation
initialize_simulation() {
    print_status "Initializing development simulation..."
    
    sleep 5
    
    # Initialize simulation via API
    curl -X POST "http://$DOMAIN:$BACKEND_PORT/api/simulation/initialize" \
        -H "Content-Type: application/json" \
        -d '{
            "num_agents": 50,
            "seed": 42,
            "max_ticks": 1000,
            "llm_mode": "mock",
            "tick_duration_ms": 100,
            "agents_per_tick": 10,
            "interactions_per_tick": 25,
            "memory_backend": "networkx",
            "vector_backend": "faiss"
        }' || print_warning "Simulation initialization may have failed (this is normal)"
    
    print_success "Development simulation initialized"
}

# Display access information
show_access_info() {
    print_success "🎉 The Cognisphere development environment is running!"
    echo ""
    echo "🌐 Access URLs:"
    echo "   Frontend: http://$DOMAIN:$FRONTEND_PORT"
    echo "   API: http://$DOMAIN:$BACKEND_PORT"
    echo "   API Docs: http://$DOMAIN:$BACKEND_PORT/api/docs"
    echo "   Health Check: http://$DOMAIN:$BACKEND_PORT/api/health"
    echo ""
    echo "📊 Monitoring:"
    echo "   Backend Logs: tail -f logs/backend.log"
    echo "   Frontend Logs: tail -f logs/frontend.log"
    echo ""
    echo "🔧 Management:"
    echo "   Stop Backend: kill \$(cat logs/backend.pid)"
    echo "   Stop Frontend: kill \$(cat logs/frontend.pid)"
    echo "   Stop All: $0 --stop"
    echo ""
    echo "💡 Hot reloading is enabled for both frontend and backend!"
    echo ""
}

# Stop services
stop_services() {
    print_status "Stopping services..."
    
    if [ -f "logs/backend.pid" ]; then
        BACKEND_PID=$(cat logs/backend.pid)
        if kill -0 $BACKEND_PID 2>/dev/null; then
            kill $BACKEND_PID
            print_success "Backend stopped"
        fi
        rm -f logs/backend.pid
    fi
    
    if [ -f "logs/frontend.pid" ]; then
        FRONTEND_PID=$(cat logs/frontend.pid)
        if kill -0 $FRONTEND_PID 2>/dev/null; then
            kill $FRONTEND_PID
            print_success "Frontend stopped"
        fi
        rm -f logs/frontend.pid
    fi
    
    print_success "All services stopped"
}

# Main function
main() {
    # Create logs directory
    mkdir -p logs
    
    check_prerequisites
    setup_dev_domain
    setup_dev_environment
    install_dependencies
    start_neo4j
    start_backend
    start_frontend
    wait_for_services
    initialize_simulation
    show_access_info
}

# Parse command line arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --stop)
            stop_services
            exit 0
            ;;
        --restart)
            stop_services
            sleep 2
            main
            exit 0
            ;;
        --help)
            echo "Usage: $0 [options]"
            echo "Options:"
            echo "  --stop      Stop all running services"
            echo "  --restart   Restart all services"
            echo "  --help      Show this help message"
            exit 0
            ;;
        *)
            print_error "Unknown option: $1"
            exit 1
            ;;
    esac
done

# Run main function
main
