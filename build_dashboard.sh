#!/bin/bash
# BUILD_DASHBOARD.sh
# Generate 30-day simulation and open dashboard

echo "🎬 Building 30-Day Historical Dashboard"
echo "=========================================="

# Check Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 not found"
    exit 1
fi

# Run simulation
echo ""
echo "📊 Generating 30-day simulation data..."
python3 tests/historical_simulation.py

if [ ! -f "simulation_data_30day.json" ]; then
    echo "❌ Simulation failed"
    exit 1
fi

echo "✅ Simulation data generated"

# Copy dashboard to accessible location
cp dashboard/historical_dashboard.html .

echo ""
echo "🌐 Dashboard ready!"
echo ""
echo "Open in browser:"
echo "  → file://$(pwd)/historical_dashboard.html"
echo ""
echo "Or run local server:"
echo "  → python3 -m http.server 8000"
echo "  → Then visit: http://localhost:8000/historical_dashboard.html"
echo ""
