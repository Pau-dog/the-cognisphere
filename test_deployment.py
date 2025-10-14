#!/usr/bin/env python3
"""
Test script for The Cognisphere deployment verification.
"""

import requests
import json
import time
import sys

def test_backend(base_url="http://localhost:8000"):
    """Test backend endpoints."""
    print(f"Testing backend at {base_url}")
    
    tests = [
        ("/", "Root endpoint"),
        ("/healthz", "Health check"),
        ("/docs", "API documentation"),
        ("/simulate", "Simulation endpoint"),
        ("/graph", "Graph data")
    ]
    
    results = {}
    
    for endpoint, description in tests:
        try:
            url = f"{base_url}{endpoint}"
            response = requests.get(url, timeout=5)
            
            if response.status_code == 200:
                print(f"✅ {description}: OK")
                results[endpoint] = "OK"
            else:
                print(f"❌ {description}: HTTP {response.status_code}")
                results[endpoint] = f"HTTP {response.status_code}"
                
        except requests.exceptions.RequestException as e:
            print(f"❌ {description}: {str(e)}")
            results[endpoint] = str(e)
    
    return results

def test_frontend(base_url="http://localhost:5173"):
    """Test frontend accessibility."""
    print(f"\nTesting frontend at {base_url}")
    
    try:
        response = requests.get(base_url, timeout=5)
        if response.status_code == 200:
            print("✅ Frontend: OK")
            return "OK"
        else:
            print(f"❌ Frontend: HTTP {response.status_code}")
            return f"HTTP {response.status_code}"
    except requests.exceptions.RequestException as e:
        print(f"❌ Frontend: {str(e)}")
        return str(e)

def test_simulation_engine():
    """Test simulation engine functionality."""
    print("\nTesting simulation engine...")
    
    try:
        # Import simulation components
        import sys
        import os
        sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))
        
        from simulation.engine import SimulationEngine
        from simulation.world import World
        from backend.adapters.llm import MockLLMAdapter
        
        # Create a small test simulation
        world = World(num_agents=5)
        llm_adapter = MockLLMAdapter()
        engine = SimulationEngine(world, llm_adapter)
        
        # Run a few ticks
        for i in range(3):
            engine.advance_tick()
        
        print("✅ Simulation engine: OK")
        return "OK"
        
    except Exception as e:
        print(f"❌ Simulation engine: {str(e)}")
        return str(e)

def main():
    """Run all tests."""
    print("The Cognisphere Deployment Test")
    print("=" * 40)
    
    # Test local deployment
    backend_results = test_backend()
    frontend_result = test_frontend()
    simulation_result = test_simulation_engine()
    
    # Summary
    print("\n" + "=" * 40)
    print("DEPLOYMENT TEST SUMMARY")
    print("=" * 40)
    
    all_ok = True
    
    print("\nBackend Tests:")
    for endpoint, result in backend_results.items():
        status = "✅" if result == "OK" else "❌"
        print(f"  {status} {endpoint}: {result}")
        if result != "OK":
            all_ok = False
    
    print(f"\nFrontend Test:")
    status = "✅" if frontend_result == "OK" else "❌"
    print(f"  {status} Frontend: {frontend_result}")
    if frontend_result != "OK":
        all_ok = False
    
    print(f"\nSimulation Test:")
    status = "✅" if simulation_result == "OK" else "❌"
    print(f"  {status} Simulation: {simulation_result}")
    if simulation_result != "OK":
        all_ok = False
    
    print("\n" + "=" * 40)
    if all_ok:
        print("🎉 ALL TESTS PASSED!")
        print("The Cognisphere is ready for deployment!")
    else:
        print("⚠️  Some tests failed. Check the errors above.")
    
    print("\nNext Steps:")
    print("1. Create GitHub repository")
    print("2. Set up Render.com backend")
    print("3. Configure GitHub secrets")
    print("4. Push to trigger auto-deployment")
    
    return 0 if all_ok else 1

if __name__ == "__main__":
    sys.exit(main())
