#!/bin/bash

# Multi-Agent Classroom - Quick Start Script
# Starts both FastAPI backend and Next.js frontend

echo "======================================================================"
echo "  Multi-Agent Classroom - FastAPI + Next.js"
echo "======================================================================"
echo ""

# Check if .env exists
if [ ! -f ".env" ]; then
    echo "⚠️  Warning: .env file not found"
    echo "Please create .env file with ANTHROPIC_API_KEY"
    echo ""
    echo "Example:"
    echo "  cp .env.example .env"
    echo "  # Edit .env and add your ANTHROPIC_API_KEY"
    echo ""
    exit 1
fi

# Check if backend dependencies are installed
if [ ! -d "backend/venv" ] && [ ! -d "venv" ]; then
    echo "⚠️  Python virtual environment not found"
    echo "Setting up backend..."
    cd backend
    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
    cd ..
fi

# Check if frontend dependencies are installed
if [ ! -d "frontend/node_modules" ]; then
    echo "⚠️  Node modules not found"
    echo "Installing frontend dependencies..."
    cd frontend
    npm install
    cd ..
fi

echo "✓ Dependencies checked"
echo ""

# Start backend in background
echo "Starting FastAPI backend on http://localhost:8000..."
cd backend
source venv/bin/activate 2>/dev/null || source ../venv/bin/activate
python main.py &
BACKEND_PID=$!
cd ..

# Wait for backend to start
sleep 3

# Start frontend
echo "Starting Next.js frontend on http://localhost:3000..."
cd frontend
npm run dev &
FRONTEND_PID=$!
cd ..

echo ""
echo "======================================================================"
echo "  🎉 Application started successfully!"
echo "======================================================================"
echo ""
echo "  Frontend:   http://localhost:3000"
echo "  Backend:    http://localhost:8000"
echo "  API Docs:   http://localhost:8000/docs"
echo ""
echo "  Press Ctrl+C to stop all servers"
echo ""
echo "======================================================================"

# Trap Ctrl+C and kill both processes
trap "echo ''; echo 'Stopping servers...'; kill $BACKEND_PID $FRONTEND_PID 2>/dev/null; exit" INT

# Wait for processes
wait
