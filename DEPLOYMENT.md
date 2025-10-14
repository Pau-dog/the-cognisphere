# 🚀 The Cognisphere Deployment Guide

This guide provides multiple deployment options to avoid localhost issues and ensure robust, production-ready access to The Cognisphere.

## 🎯 Deployment Options Overview

| Method | Best For | Domain | SSL | Monitoring | Complexity |
|--------|----------|--------|-----|------------|------------|
| Local Dev | Development | cognisphere.dev | No | Basic | Low |
| Docker Dev | Testing | cognisphere.local | No | Basic | Medium |
| Production | Demos/Production | cognisphere.local | Yes | Full | High |
| Cloud | Sharing/Public | Custom | Yes | Full | Variable |

## 🏠 Local Development (Recommended for Development)

### Prerequisites
- Python 3.9+
- Node.js 18+
- npm/yarn

### Setup
```bash
# Run the interactive setup
./scripts/quick-start.sh

# Or run directly
./scripts/local-dev.sh
```

### Features
- ✅ Hot reloading for frontend and backend
- ✅ Uses `cognisphere.dev` domain (no localhost)
- ✅ Minimal resource usage
- ✅ Easy debugging
- ✅ NetworkX fallback (no Neo4j required)

### Access URLs
- Frontend: `http://cognisphere.dev:3001`
- API: `http://cognisphere.dev:8001`
- API Docs: `http://cognisphere.dev:8001/api/docs`

## 🐳 Docker Development (Recommended for Testing)

### Prerequisites
- Docker & Docker Compose
- 4GB+ RAM available

### Setup
```bash
# Quick setup
./scripts/quick-start.sh

# Or run directly
docker-compose -f docker/docker-compose.yml up --build
```

### Features
- ✅ Full containerized environment
- ✅ Uses `cognisphere.local` domain
- ✅ Neo4j database included
- ✅ Easy to reset and clean
- ✅ Consistent across machines

### Access URLs
- Frontend: `http://cognisphere.local:5173`
- API: `http://cognisphere.local:8000`
- Neo4j: `http://cognisphere.local:7474`

## 🚀 Production Deployment (Recommended for Demos)

### Prerequisites
- Docker & Docker Compose
- 8GB+ RAM available
- SSL certificates (auto-generated for local)

### Setup
```bash
# Run production deployment
./scripts/deploy.sh

# With custom domain
COGNISPHERE_DOMAIN=your-domain.local ./scripts/deploy.sh
```

### Features
- ✅ SSL/TLS encryption
- ✅ Nginx reverse proxy
- ✅ Full monitoring stack (Prometheus + Grafana)
- ✅ Production-grade security
- ✅ Auto-scaling ready
- ✅ Health checks and logging

### Access URLs
- Frontend: `https://cognisphere.local`
- API: `https://cognisphere.local/api`
- Neo4j: `https://cognisphere.local:7474`
- Monitoring: `https://cognisphere.local:3001`

## 🌐 Cloud Deployment Options

### GitHub Codespaces
```bash
# 1. Push repository to GitHub
git push origin main

# 2. Open in Codespaces
# 3. Run quick start
./scripts/quick-start.sh
```

### Railway
```bash
# 1. Install Railway CLI
npm install -g @railway/cli

# 2. Deploy
railway login
railway init
railway up
```

### Render
1. Connect GitHub repository to Render
2. Create new Web Service
3. Use `docker-compose.prod.yml`
4. Set environment variables

### Vercel + Railway (Hybrid)
- Frontend: Deploy to Vercel
- Backend: Deploy to Railway
- Update frontend environment variables

## 🔧 Environment Configuration

### Local Development (.env)
```bash
# Backend
PYTHONPATH=/app
SIMULATION_SEED=42
SIMULATION_AGENTS=100
LLM_MODE=mock
MEMORY_BACKEND=networkx
LOG_LEVEL=DEBUG

# Frontend
VITE_API_URL=http://cognisphere.dev:8001
VITE_WS_URL=ws://cognisphere.dev:8001
```

### Production (.env.production)
```bash
# Backend
SIMULATION_AGENTS=500
LLM_MODE=mock
MEMORY_BACKEND=neo4j
VECTOR_BACKEND=faiss
SECRET_KEY=<generated>
JWT_SECRET=<generated>

# Frontend
VITE_API_URL=https://cognisphere.local/api
VITE_WS_URL=wss://cognisphere.local/api
```

## 🛠️ Management Commands

### Service Control
```bash
# Start services
./scripts/quick-start.sh

# Stop all services
./scripts/local-dev.sh --stop
docker-compose -f docker/docker-compose.yml down

# Restart services
./scripts/local-dev.sh --restart
docker-compose -f docker/docker-compose.yml restart

# Reset environment
docker-compose -f docker/docker-compose.yml down -v
docker system prune -f
```

### Monitoring
```bash
# View logs
docker-compose -f docker/docker-compose.yml logs -f

# Check status
docker-compose -f docker/docker-compose.yml ps

# Access services
docker exec -it cognisphere_neo4j_1 cypher-shell
docker exec -it cognisphere_redis_1 redis-cli
```

## 🔍 Troubleshooting

### Common Issues

#### 1. Domain Not Resolving
```bash
# Check /etc/hosts
cat /etc/hosts | grep cognisphere

# Add domain if missing
echo "127.0.0.1 cognisphere.local" | sudo tee -a /etc/hosts
echo "127.0.0.1 cognisphere.dev" | sudo tee -a /etc/hosts
```

#### 2. Port Conflicts
```bash
# Check port usage
lsof -i :8000
lsof -i :5173
lsof -i :3001

# Kill conflicting processes
sudo kill -9 <PID>
```

#### 3. Docker Issues
```bash
# Clean Docker
docker system prune -a
docker volume prune

# Rebuild containers
docker-compose -f docker/docker-compose.yml build --no-cache
```

#### 4. SSL Certificate Issues
```bash
# Regenerate certificates
rm -rf docker/ssl/*
./scripts/deploy.sh
```

### Performance Optimization

#### For Large Simulations (1000+ agents)
```bash
# Increase Docker resources
# Docker Desktop -> Settings -> Resources
# Memory: 8GB+
# CPUs: 4+

# Use production deployment
./scripts/deploy.sh
```

#### For Development Speed
```bash
# Use local development
./scripts/local-dev.sh

# Reduce simulation size
export SIMULATION_AGENTS=50
```

## 📊 Monitoring & Observability

### Built-in Monitoring
- **Prometheus**: Metrics collection
- **Grafana**: Dashboards and visualization
- **Nginx**: Access logs and metrics
- **Application**: Custom metrics and health checks

### Access Monitoring
- Grafana: `https://cognisphere.local:3001`
- Prometheus: `https://cognisphere.local:9090`

### Key Metrics
- Agent count and activity
- Memory usage (Neo4j, Redis)
- API response times
- Simulation tick duration
- Error rates

## 🔒 Security Considerations

### Production Security
- SSL/TLS encryption
- Rate limiting
- Security headers
- Input validation
- Authentication (JWT)

### Network Security
- Internal Docker networks
- Firewall rules
- VPN access (for remote teams)

## 🚀 Scaling Options

### Horizontal Scaling
- Load balancer (Nginx)
- Multiple backend instances
- Database clustering (Neo4j)

### Vertical Scaling
- Increase container resources
- Optimize database settings
- Use faster storage (SSD)

## 📝 Best Practices

1. **Always use dedicated domains** (never localhost)
2. **Use environment-specific configurations**
3. **Monitor resource usage** during development
4. **Test with production-like data** before deploying
5. **Keep backups** of important simulation states
6. **Use version control** for all configuration changes

## 🆘 Getting Help

### Logs and Debugging
```bash
# Application logs
tail -f logs/backend.log
tail -f logs/frontend.log

# Docker logs
docker-compose -f docker/docker-compose.yml logs -f backend
docker-compose -f docker/docker-compose.yml logs -f frontend
```

### Health Checks
```bash
# API health
curl -f http://cognisphere.local:8000/api/health

# Frontend health
curl -f http://cognisphere.local:5173

# Database health
docker exec cognisphere_neo4j_1 cypher-shell "RETURN 1"
```

### Support
- Check this documentation first
- Review logs for error messages
- Ensure all prerequisites are installed
- Try different deployment methods

---

**Remember**: The Cognisphere is designed to avoid localhost issues entirely. Always use the provided domains (`cognisphere.local` or `cognisphere.dev`) for the best experience! 🚀
