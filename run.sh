#!/bin/bash

# GenAI Prompt Generator - Setup and Run Script

echo "🤖 GenAI Prompt Generator - Setup and Run"
echo "=========================================="

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.8 or higher."
    exit 1
fi

# Check if pip is installed
if ! command -v pip3 &> /dev/null; then
    echo "❌ pip3 is not installed. Please install pip3."
    exit 1
fi

echo "✅ Python and pip3 are available"

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "📥 Installing dependencies..."
pip install -r requirements.txt

# Check if .env file exists
if [ ! -f ".env" ]; then
    echo "⚙️  Creating .env file from template..."
    cp .env.template .env
    echo "⚠️  Please edit the .env file with your LLM Farm configuration before running the app."
    echo "   - Set your API_KEY"
    echo "   - Set your LLM_FARM_URL"
    echo ""
    read -p "Press Enter after configuring .env file to continue..."
fi

# Run the application
echo "🚀 Starting GenAI Prompt Generator..."
echo "🌐 The application will be available at: http://localhost:8501"
echo "📝 Press Ctrl+C to stop the application"
echo ""

streamlit run app.py