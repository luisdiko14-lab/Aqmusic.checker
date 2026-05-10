#!/bin/bash

# AQMusic Checker - Local Test Script
# This script tests the Flask server and verifies all endpoints

echo "=========================================="
echo "AQMusic Checker - Local Test"
echo "=========================================="
echo ""

# Check if Flask is installed
echo "1. Checking dependencies..."
python -c "import flask; print('✓ Flask installed')" 2>/dev/null || echo "✗ Flask not installed - run: pip install -r requirements.txt"
python -c "import requests; print('✓ Requests installed')" 2>/dev/null || echo "✗ Requests not installed"
echo ""

# Start server
echo "2. Starting Flask server..."
python server.py &
SERVER_PID=$!
echo "   Server PID: $SERVER_PID"
sleep 2
echo ""

# Test endpoints
echo "3. Testing endpoints..."

# Health check
echo -n "   Health endpoint: "
if curl -s http://localhost:5000/health > /dev/null 2>&1; then
    echo "✓"
else
    echo "✗"
fi

# Index page
echo -n "   Index page: "
if curl -s http://localhost:5000/ | grep -q "AQMusic Checker"; then
    echo "✓"
else
    echo "✗"
fi

# API endpoint
echo -n "   API endpoint: "
if curl -s http://localhost:5000/api/check | grep -q "timestamp"; then
    echo "✓"
else
    echo "✗"
fi
echo ""

# API response preview
echo "4. API Response Sample (first 500 chars):"
curl -s http://localhost:5000/api/check | head -c 500
echo ""
echo ""
echo ""

# Cleanup
echo "5. Cleanup..."
kill $SERVER_PID 2>/dev/null
wait $SERVER_PID 2>/dev/null
echo "   Server stopped"
echo ""

echo "=========================================="
echo "Test complete!"
echo "=========================================="
echo ""
echo "To run the server manually:"
echo "  python server.py"
echo ""
echo "Then open: http://localhost:5000"
