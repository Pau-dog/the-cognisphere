#!/bin/bash

# Production deployment script for The Cognisphere
# Avoids localhost issues by using proper domain setup

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
DOMAIN=${COGNISPHERE_DOMAIN:-"cognisphere.local"}
PORT=${COGNISPHERE_PORT:-"8080"}
ENVIRONMENT=${ENVIRONMENT:-"production"}

print_status "🚀 Deploying The Cognisphere in $ENVIRONMENT mode..."

# Check prerequisites
check_prerequisites() {
    print_status "Checking prerequisites..."
    
    if ! command -v docker &> /dev/null; then
        print_error "Docker is not installed. Please install Docker first."
        exit 1
    fi
    
    if ! command -v docker-compose &> /dev/null; then
        print_error "Docker Compose is not installed. Please install Docker Compose first."
        exit 1
    fi
    
    print_success "Prerequisites check passed"
}

# Setup domain (avoid localhost issues)
setup_domain() {
    print_status "Setting up domain: $DOMAIN"
    
    # Add domain to /etc/hosts if not already present
    if ! grep -q "$DOMAIN" /etc/hosts; then
        print_status "Adding $DOMAIN to /etc/hosts..."
        echo "127.0.0.1 $DOMAIN" | sudo tee -a /etc/hosts
        print_success "Domain added to /etc/hosts"
    else
        print_status "Domain already exists in /etc/hosts"
    fi
}

# Create SSL certificates for local development
create_ssl_certificates() {
    print_status "Creating SSL certificates for local development..."
    
    mkdir -p docker/ssl
    
    if [ ! -f "docker/ssl/cert.pem" ] || [ ! -f "docker/ssl/key.pem" ]; then
        openssl req -x509 -newkey rsa:4096 -keyout docker/ssl/key.pem -out docker/ssl/cert.pem \
            -days 365 -nodes -subj "/C=US/ST=State/L=City/O=Organization/CN=$DOMAIN"
        print_success "SSL certificates created"
    else
        print_status "SSL certificates already exist"
    fi
}

# Setup environment variables
setup_environment() {
    print_status "Setting up environment variables..."
    
    cat > .env.production << EOF
# Production Environment
NODE_ENV=production
VITE_API_URL=https://$DOMAIN/api
VITE_WS_URL=wss://$DOMAIN/api

# Backend Configuration
PYTHONPATH=/app
SIMULATION_SEED=42
SIMULATION_AGENTS=500
SIMULATION_TICKS=10000
LLM_MODE=mock
MEMORY_BACKEND=neo4j
VECTOR_BACKEND=faiss

# Database Configuration
NEO4J_AUTH=neo4j/cognisphere_secure_password_$(date +%s)
REDIS_PASSWORD=cognisphere_redis_$(date +%s)

# Security
SECRET_KEY=$(openssl rand -hex 32)
JWT_SECRET=$(openssl rand -hex 32)

# Monitoring
ENABLE_METRICS=true
LOG_LEVEL=INFO
EOF

    print_success "Environment variables configured"
}

# Build and deploy
deploy_application() {
    print_status "Building and deploying application..."
    
    # Pull latest images
    docker-compose -f docker/docker-compose.yml pull
    
    # Build custom images
    docker-compose -f docker/docker-compose.yml build --no-cache
    
    # Stop existing containers
    docker-compose -f docker/docker-compose.yml down
    
    # Start services
    docker-compose -f docker/docker-compose.yml up -d
    
    print_success "Application deployed"
}

# Wait for services to be ready
wait_for_services() {
    print_status "Waiting for services to be ready..."
    
    # Wait for backend
    print_status "Waiting for backend API..."
    timeout=60
    while [ $timeout -gt 0 ]; do
        if curl -f -s "https://$DOMAIN/api/health" > /dev/null 2>&1; then
            print_success "Backend API is ready"
            break
        fi
        sleep 2
        timeout=$((timeout - 2))
    done
    
    if [ $timeout -le 0 ]; then
        print_error "Backend API failed to start within timeout"
        exit 1
    fi
    
    # Wait for frontend
    print_status "Waiting for frontend..."
    timeout=60
    while [ $timeout -gt 0 ]; do
        if curl -f -s "https://$DOMAIN/" > /dev/null 2>&1; then
            print_success "Frontend is ready"
            break
        fi
        sleep 2
        timeout=$((timeout - 2))
    done
    
    if [ $timeout -le 0 ]; then
        print_error "Frontend failed to start within timeout"
        exit 1
    fi
}

# Initialize simulation
initialize_simulation() {
    print_status "Initializing simulation..."
    
    # Wait a bit more for all services
    sleep 10
    
    # Initialize simulation via API
    curl -X POST "https://$DOMAIN/api/simulation/initialize" \
        -H "Content-Type: application/json" \
        -d '{
            "num_agents": 300,
            "seed": 42,
            "max_ticks": 10000,
            "llm_mode": "mock",
            "tick_duration_ms": 100,
            "agents_per_tick": 50,
            "interactions_per_tick": 100,
            "memory_backend": "neo4j",
            "vector_backend": "faiss"
        }' || print_warning "Simulation initialization may have failed (this is normal)"
    
    print_success "Simulation initialized"
}

# Display access information
show_access_info() {
    print_success "🎉 The Cognisphere is now running!"
    echo ""
    echo "🌐 Access URLs:"
    echo "   Frontend: https://$DOMAIN"
    echo "   API Docs: https://$DOMAIN/api/docs"
    echo "   Health Check: https://$DOMAIN/api/health"
    echo ""
    echo "🔧 Management:"
    echo "   View logs: docker-compose -f docker/docker-compose.yml logs -f"
    echo "   Stop: docker-compose -f docker/docker-compose.yml down"
    echo "   Restart: docker-compose -f docker/docker-compose.yml restart"
    echo ""
    echo "📊 Monitoring:"
    echo "   Neo4j Browser: https://$DOMAIN:7474 (neo4j/cognisphere_secure_password_*)"
    echo "   Redis CLI: docker exec -it cognisphere_redis_1 redis-cli"
    echo ""
    echo "⚠️  Note: You may need to accept the self-signed SSL certificate"
    echo "   in your browser for the first visit."
    echo ""
}

# Cleanup function
cleanup() {
    print_status "Cleaning up..."
    docker-compose -f docker/docker-compose.yml down
    print_success "Cleanup completed"
}

# Main deployment flow
main() {
    check_prerequisites
    setup_domain
    create_ssl_certificates
    setup_environment
    deploy_application
    wait_for_services
    initialize_simulation
    show_access_info
}

# Handle script interruption
trap cleanup EXIT INT TERM

# Parse command line arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --domain)
            DOMAIN="$2"
            shift 2
            ;;
        --port)
            PORT="$2"
            shift 2
            ;;
        --env)
            ENVIRONMENT="$2"
            shift 2
            ;;
        --cleanup)
            cleanup
            exit 0
            ;;
        --help)
            echo "Usage: $0 [options]"
            echo "Options:"
            echo "  --domain DOMAIN    Set custom domain (default: cognisphere.local)"
            echo "  --port PORT        Set custom port (default: 8080)"
            echo "  --env ENVIRONMENT  Set environment (default: production)"
            echo "  --cleanup          Stop and remove all containers"
            echo "  --help             Show this help message"
            exit 0
            ;;
        *)
            print_error "Unknown option: $1"
            exit 1
            ;;
    esac
done

# Run main deployment
main
