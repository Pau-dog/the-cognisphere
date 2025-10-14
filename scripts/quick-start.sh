#!/bin/bash

# Quick start script for The Cognisphere
# This script provides multiple deployment options to avoid localhost issues

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
NC='\033[0m' # No Color

print_banner() {
    echo -e "${PURPLE}"
    echo "  _____                      _           _       _                 "
    echo " / ____|                    (_)         (_)     | |                "
    echo "| |     ___  _ __  _ __  ___ _ _ __ ___  _ _ __ | |__   ___ _ __ ___ "
    echo "| |    / _ \| '_ \| '_ \ / __| | '_ \` _ \| | '_ \| '_ \ / _ \ '__/ __|"
    echo "| |___| (_) | | | | | | | (__| | | | | | | |_) | | | |  __/ |  \__ \\"
    echo " \_____\___/|_| |_|_| |_|\___|_|_| |_| |_| .__/|_| |_|\___|_|  |___/"
    echo "                                        | |                      "
    echo "                                        |_|                      "
    echo -e "${NC}"
    echo -e "${BLUE}🚀 Emergent Intelligence Civilization Engine${NC}"
    echo ""
}

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

print_menu() {
    echo "🎯 Choose your deployment method:"
    echo ""
    echo "1. 🏠 Local Development (recommended for development)"
    echo "   - Uses cognisphere.dev domain"
    echo "   - Hot reloading enabled"
    echo "   - Minimal resource usage"
    echo ""
    echo "2. 🐳 Docker Development (recommended for testing)"
    echo "   - Uses cognisphere.local domain"
    echo "   - Full containerized environment"
    echo "   - Easy to reset and clean"
    echo ""
    echo "3. 🚀 Production Deployment (recommended for demos)"
    echo "   - Uses cognisphere.local domain"
    echo "   - SSL certificates"
    echo "   - Full monitoring stack"
    echo ""
    echo "4. 🌐 Cloud Deployment (for sharing)"
    echo "   - Deploy to cloud provider"
    echo "   - Public URL generation"
    echo "   - Production-ready setup"
    echo ""
    echo "5. 🔧 Management Options"
    echo "   - Stop all services"
    echo "   - View logs"
    echo "   - Reset environment"
    echo ""
    echo "0. ❌ Exit"
    echo ""
}

# Local development deployment
deploy_local_dev() {
    print_status "Starting local development deployment..."
    
    if [ -f "scripts/local-dev.sh" ]; then
        chmod +x scripts/local-dev.sh
        ./scripts/local-dev.sh
    else
        print_error "Local development script not found"
        exit 1
    fi
}

# Docker development deployment
deploy_docker_dev() {
    print_status "Starting Docker development deployment..."
    
    # Setup domain
    if ! grep -q "cognisphere.local" /etc/hosts; then
        echo "127.0.0.1 cognisphere.local" | sudo tee -a /etc/hosts
    fi
    
    # Start services
    docker-compose -f docker/docker-compose.yml up --build -d
    
    print_success "Docker development environment started!"
    echo ""
    echo "🌐 Access URLs:"
    echo "   Frontend: http://cognisphere.local:5173"
    echo "   API: http://cognisphere.local:8000"
    echo "   Neo4j: http://cognisphere.local:7474"
    echo ""
    echo "🔧 Management:"
    echo "   View logs: docker-compose -f docker/docker-compose.yml logs -f"
    echo "   Stop: docker-compose -f docker/docker-compose.yml down"
    echo ""
}

# Production deployment
deploy_production() {
    print_status "Starting production deployment..."
    
    if [ -f "scripts/deploy.sh" ]; then
        chmod +x scripts/deploy.sh
        ./scripts/deploy.sh
    else
        print_error "Production deployment script not found"
        exit 1
    fi
}

# Cloud deployment
deploy_cloud() {
    print_status "Cloud deployment options..."
    
    echo "🌐 Choose your cloud provider:"
    echo ""
    echo "1. 🐙 GitHub Codespaces (instant setup)"
    echo "2. ☁️  Railway (simple deployment)"
    echo "3. 🚀 Render (production ready)"
    echo "4. 🔥 Vercel + Railway (hybrid)"
    echo "5. 🐳 Docker Hub (container registry)"
    echo ""
    read -p "Enter choice (1-5): " cloud_choice
    
    case $cloud_choice in
        1)
            print_status "Setting up GitHub Codespaces deployment..."
            echo "To deploy on GitHub Codespaces:"
            echo "1. Push this repository to GitHub"
            echo "2. Open in Codespaces"
            echo "3. Run: ./scripts/quick-start.sh and choose option 1"
            ;;
        2)
            print_status "Setting up Railway deployment..."
            echo "To deploy on Railway:"
            echo "1. Install Railway CLI: npm install -g @railway/cli"
            echo "2. Run: railway login"
            echo "3. Run: railway init"
            echo "4. Run: railway up"
            ;;
        3)
            print_status "Setting up Render deployment..."
            echo "To deploy on Render:"
            echo "1. Connect your GitHub repository to Render"
            echo "2. Create a new Web Service"
            echo "3. Use docker-compose.prod.yml as build command"
            echo "4. Set environment variables"
            ;;
        4)
            print_status "Setting up hybrid deployment..."
            echo "Frontend on Vercel, Backend on Railway"
            echo "1. Deploy frontend to Vercel"
            echo "2. Deploy backend to Railway"
            echo "3. Update frontend environment variables"
            ;;
        5)
            print_status "Setting up Docker Hub deployment..."
            echo "To deploy via Docker Hub:"
            echo "1. Build and push images to Docker Hub"
            echo "2. Use docker-compose with your images"
            echo "3. Deploy on any Docker-compatible platform"
            ;;
        *)
            print_error "Invalid cloud choice"
            ;;
    esac
}

# Management options
manage_services() {
    print_status "Management options..."
    
    echo "🔧 What would you like to do?"
    echo ""
    echo "1. 🛑 Stop all services"
    echo "2. 📋 View logs"
    echo "3. 🔄 Restart services"
    echo "4. 🧹 Reset environment"
    echo "5. 📊 Check status"
    echo ""
    read -p "Enter choice (1-5): " manage_choice
    
    case $manage_choice in
        1)
            print_status "Stopping all services..."
            docker-compose -f docker/docker-compose.yml down 2>/dev/null || true
            docker-compose -f docker/docker-compose.prod.yml down 2>/dev/null || true
            if [ -f "scripts/local-dev.sh" ]; then
                ./scripts/local-dev.sh --stop 2>/dev/null || true
            fi
            print_success "All services stopped"
            ;;
        2)
            print_status "Viewing logs..."
            echo "Choose log source:"
            echo "1. Docker services"
            echo "2. Local development"
            read -p "Enter choice: " log_choice
            
            if [ "$log_choice" = "1" ]; then
                docker-compose -f docker/docker-compose.yml logs -f
            else
                if [ -f "logs/backend.log" ]; then
                    echo "=== Backend Logs ==="
                    tail -f logs/backend.log
                else
                    print_warning "No local logs found"
                fi
            fi
            ;;
        3)
            print_status "Restarting services..."
            docker-compose -f docker/docker-compose.yml restart
            print_success "Services restarted"
            ;;
        4)
            print_warning "This will reset your entire environment!"
            read -p "Are you sure? (y/N): " confirm
            if [ "$confirm" = "y" ] || [ "$confirm" = "Y" ]; then
                print_status "Resetting environment..."
                docker-compose -f docker/docker-compose.yml down -v
                docker system prune -f
                rm -rf logs/* 2>/dev/null || true
                print_success "Environment reset"
            fi
            ;;
        5)
            print_status "Checking service status..."
            docker-compose -f docker/docker-compose.yml ps
            ;;
        *)
            print_error "Invalid management choice"
            ;;
    esac
}

# Main menu loop
main() {
    print_banner
    
    while true; do
        print_menu
        read -p "Enter your choice (0-5): " choice
        
        case $choice in
            1)
                deploy_local_dev
                break
                ;;
            2)
                deploy_docker_dev
                break
                ;;
            3)
                deploy_production
                break
                ;;
            4)
                deploy_cloud
                break
                ;;
            5)
                manage_services
                ;;
            0)
                print_status "Goodbye! 👋"
                exit 0
                ;;
            *)
                print_error "Invalid choice. Please try again."
                ;;
        esac
        
        echo ""
        read -p "Press Enter to continue..."
        clear
        print_banner
    done
}

# Check if running in interactive mode
if [ -t 0 ]; then
    main
else
    print_error "This script requires an interactive terminal"
    exit 1
fi
