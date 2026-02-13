#!/bin/bash

echo "Starting Rapport Backend and Frontend..."

echo ""
echo "Starting Backend..."
cd backend
if [ ! -f .env ]; then
    echo "Creating .env from .env.example..."
    cp .env.example .env
fi
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000 &
BACKEND_PID=$!

echo ""
echo "Starting Frontend (uni-app H5)..."
cd ../frontend
if [ ! -f .env ]; then
    echo "Creating .env from .env.example..."
    cp .env.example .env
fi
echo "Installing dependencies..."
npm install
echo "Starting dev server..."
npm run dev:h5 &
FRONTEND_PID=$!

echo ""
echo "Both services are running..."
echo "Backend: http://localhost:8000"
echo "Frontend: http://localhost:5173"
echo "API Docs: http://localhost:8000/docs"
echo ""
echo "Press Ctrl+C to stop both services"

# Handle shutdown
trap "kill $BACKEND_PID $FRONTEND_PID; exit" INT TERM

wait
