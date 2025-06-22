#!/usr/bin/env python3
"""
Main entry point for the Sleep Science Explainer Bot.
This script provides a unified interface to start the application.
"""

import os
import sys
import subprocess
import time
import signal
import threading
from pathlib import Path
from typing import Optional

def print_banner():
    """Print application banner."""
    print("""
🌙 Sleep Science Explainer Bot
================================
A conversational AI for sleep science research
    """)

def check_dependencies():
    """Check if required dependencies are installed."""
    print("🔍 Checking dependencies...")
    
    # Check Python version
    if sys.version_info < (3, 9):
        print("❌ Python 3.9+ is required")
        return False
    
    # Check if virtual environment is activated
    if not hasattr(sys, 'real_prefix') and not (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix):
        print("⚠️  Virtual environment not detected. Consider activating one.")
    
    # Check if requirements are installed
    try:
        import fastapi
        import uvicorn
        import sqlalchemy
        print("✅ Backend dependencies found")
    except ImportError as e:
        print(f"❌ Missing backend dependency: {e}")
        print("Run: pip install -r requirements.txt")
        return False
    
    # Check if frontend dependencies are installed
    frontend_path = Path("frontend")
    if frontend_path.exists():
        node_modules = frontend_path / "node_modules"
        if not node_modules.exists():
            print("⚠️  Frontend dependencies not found")
            print("Run: cd frontend && npm install")
            return False
        else:
            print("✅ Frontend dependencies found")
    
    return True

def check_environment():
    """Check if environment is properly configured."""
    print("🔧 Checking environment configuration...")
    
    env_file = Path(".env")
    if not env_file.exists():
        print("⚠️  .env file not found")
        print("Run: cp env.example .env")
        print("Then edit .env with your configuration")
        return False
    
    # Check for required environment variables
    required_vars = [
        "DATABASE_URL",
        "AWS_ACCESS_KEY_ID", 
        "AWS_SECRET_ACCESS_KEY"
    ]
    
    missing_vars = []
    for var in required_vars:
        if not os.getenv(var):
            missing_vars.append(var)
    
    if missing_vars:
        print(f"⚠️  Missing environment variables: {', '.join(missing_vars)}")
        print("Please configure these in your .env file")
        return False
    
    print("✅ Environment configuration looks good")
    return True

def start_backend():
    """Start the FastAPI backend server."""
    print("🚀 Starting backend server...")
    try:
        subprocess.run([sys.executable, "app.py"], check=True)
    except subprocess.CalledProcessError as e:
        print(f"❌ Backend failed to start: {e}")
        return False
    except KeyboardInterrupt:
        print("\n🛑 Backend stopped by user")
        return True

def start_frontend():
    """Start the React frontend development server."""
    print("🎨 Starting frontend server...")
    try:
        frontend_dir = Path("frontend")
        if not frontend_dir.exists():
            print("❌ Frontend directory not found")
            return False
        
        os.chdir(frontend_dir)
        subprocess.run(["npm", "start"], check=True)
    except subprocess.CalledProcessError as e:
        print(f"❌ Frontend failed to start: {e}")
        return False
    except KeyboardInterrupt:
        print("\n🛑 Frontend stopped by user")
        return True

def start_both():
    """Start both backend and frontend servers."""
    print("🚀 Starting both backend and frontend servers...")
    
    # Start backend in a separate thread
    backend_thread = threading.Thread(target=start_backend, daemon=True)
    backend_thread.start()
    
    # Wait a moment for backend to start
    time.sleep(3)
    
    # Start frontend
    start_frontend()

def run_tests():
    """Run the test suite."""
    print("🧪 Running tests...")
    try:
        result = subprocess.run([
            sys.executable, "-m", "pytest", "tests/", "-v"
        ], check=True)
        print("✅ All tests passed!")
        return True
    except subprocess.CalledProcessError:
        print("❌ Some tests failed")
        return False

def generate_coverage():
    """Generate test coverage report."""
    print("📊 Generating coverage report...")
    try:
        subprocess.run([
            sys.executable, "-m", "pytest", "tests/", 
            "--cov=backend", "--cov-report=html", "--cov-report=term"
        ], check=True)
        print("✅ Coverage report generated!")
        print("📁 View report at: htmlcov/index.html")
        return True
    except subprocess.CalledProcessError:
        print("❌ Coverage generation failed")
        return False

def show_help():
    """Show help information."""
    print("""
Usage: python main.py [command]

Commands:
  start       Start the backend server only
  frontend    Start the frontend server only
  both        Start both backend and frontend servers
  test        Run the test suite
  coverage    Generate test coverage report
  check       Check dependencies and environment
  help        Show this help message

Examples:
  python main.py both        # Start both servers
  python main.py test        # Run tests
  python main.py coverage    # Generate coverage report
    """)

def main():
    """Main entry point."""
    print_banner()
    
    if len(sys.argv) < 2:
        show_help()
        return
    
    command = sys.argv[1].lower()
    
    if command == "help":
        show_help()
    elif command == "check":
        check_dependencies()
        check_environment()
    elif command == "test":
        if check_dependencies():
            run_tests()
    elif command == "coverage":
        if check_dependencies():
            generate_coverage()
    elif command == "start":
        if check_dependencies() and check_environment():
            start_backend()
    elif command == "frontend":
        if check_dependencies():
            start_frontend()
    elif command == "both":
        if check_dependencies() and check_environment():
            start_both()
    else:
        print(f"❌ Unknown command: {command}")
        show_help()

if __name__ == "__main__":
    main() 