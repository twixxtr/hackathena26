#!/bin/bash

echo "==============================================="
echo "   AI SECURITY HUNTER/TESTER PROTOTYPE"
echo "==============================================="

# Activate virtual environment
source venv/bin/activate

# Start the dummy vulnerable AI in the background
echo "[*] Starting Dummy Vulnerable AI on port 11434..."
python dummy_ai.py &
DUMMY_PID=$!

# Wait a second for it to initialize
sleep 2

# Start the main FastAPI prototype server
echo "[*] Starting Main Prototype Server on port 8000..."
echo "[*] Access the dashboard at: http://localhost:8000"
PYTHONPATH="$PWD/backend" uvicorn backend.main:app --host 0.0.0.0 --port 8000 &
MAIN_PID=$!

# Function to handle cleanup on exit
cleanup() {
    echo ""
    echo "[!] Shutting down servers..."
    kill $DUMMY_PID 2>/dev/null
    kill $MAIN_PID 2>/dev/null
    echo "[!] Goodbye."
    exit 0
}

# Trap SIGINT (Ctrl+C) and call cleanup
trap cleanup SIGINT

# Wait indefinitely to keep the script running
wait
