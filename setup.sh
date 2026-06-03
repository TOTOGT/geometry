#!/bin/bash
# Quick-start script for Kelly JOMO Claude Agent
set -e

echo "🚀 Kelly JOMO Agent Setup"
echo "========================="

# Check Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 not found. Install Python 3.10+ and try again."
    exit 1
fi

echo "✅ Python found: $(python3 --version)"

# Create venv if needed
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

source venv/bin/activate
echo "✅ Virtual environment activated"

# Install dependencies
echo "📚 Installing dependencies..."
pip install -q -r requirements.txt
echo "✅ Dependencies installed"

# Check for .env
if [ ! -f ".env" ]; then
    echo "⚙️  Creating .env from template..."
    cp .env.example .env
    echo "⚠️  Edit .env with your ANTHROPIC_API_KEY"
    echo "   Then run: source venv/bin/activate && python agents/kelly_jomo_agent.py"
else
    echo "✅ .env found"
fi

# Check API key
if ! grep -q "sk-ant-" .env 2>/dev/null; then
    echo "⚠️  ANTHROPIC_API_KEY not configured in .env"
    echo "   Get your key at: https://console.anthropic.com"
    exit 1
fi

echo ""
echo "🎯 Ready to deploy!"
echo ""
echo "Options:"
echo "  1. Run agent locally:"
echo "     python agents/kelly_jomo_agent.py"
echo ""
echo "  2. View dashboard:"
echo "     streamlit run dashboard/kelly_jomo_dashboard.py"
echo ""
echo "  3. Run GitHub Actions:"
echo "     git push origin claude-agent-deployment"
echo ""
echo "  4. Docker:"
echo "     docker build -t kelly-jomo . && docker run -e ANTHROPIC_API_KEY=\$KEY kelly-jomo"
echo ""
