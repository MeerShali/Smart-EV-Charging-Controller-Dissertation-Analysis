#!/bin/bash
# One-command setup script

set -e
echo "🚀 Setting up Smart EV Charging Analysis"

# Check Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 not found"
    exit 1
fi

# Create venv
if [ ! -d "venv" ]; then
    python3 -m venv venv
    echo "✓ Virtual environment created"
fi

source venv/bin/activate

# Install dependencies
pip install -q -r requirements.txt
echo "✓ Dependencies installed"

# Create output directories
mkdir -p figures/survey_charts
mkdir -p figures/energy_analysis
echo "✓ Output directories created"

# Generate figures
echo "🎨 Generating figures..."
python -m src.energy_price_analysis
python -m src.survey_analysis

echo ""
echo "✅ Setup complete!"
echo "Figures saved to: figures/"
