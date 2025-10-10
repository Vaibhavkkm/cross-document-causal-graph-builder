#!/bin/bash

# Causal Graph Builder - Quick Setup Script
# This script helps you get started quickly

echo "╔══════════════════════════════════════════════════════════════════╗"
echo "║   🚀 Causal Graph Builder - Quick Setup                         ║"
echo "╚══════════════════════════════════════════════════════════════════╝"
echo ""

# Get the directory where the script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

echo "📂 Working directory: $SCRIPT_DIR"
echo ""

# Step 1: Check Python
echo "1️⃣  Checking Python installation..."
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version)
    echo "   ✅ Found: $PYTHON_VERSION"
else
    echo "   ❌ Python 3 not found!"
    exit 1
fi
echo ""

# Step 2: Check dataset
echo "2️⃣  Checking dataset..."
if [ -d "final_dataset" ]; then
    FILE_COUNT=$(ls final_dataset/*.txt 2>/dev/null | wc -l)
    echo "   ✅ Found $FILE_COUNT text files"
else
    echo "   ❌ final_dataset directory not found!"
    exit 1
fi
echo ""

# Step 3: Install basic dependencies
echo "3️⃣  Installing basic dependencies..."
echo "   📦 Installing Flask..."
python3 -m pip install -q Flask
echo "   ✅ Flask installed"
echo ""

# Step 4: Optional NLP dependencies
echo "4️⃣  Optional: Install NLP dependencies? (recommended)"
read -p "   Install spaCy for better event extraction? [y/N]: " -n 1 -r
echo ""
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo "   📦 Installing spaCy..."
    python3 -m pip install -q spacy
    echo "   📦 Downloading English language model..."
    python3 -m spacy download en_core_web_sm
    echo "   ✅ spaCy installed"
else
    echo "   ⏭️  Skipped (you can install later with: pip install spacy)"
fi
echo ""

# Step 5: Run preprocessing
echo "5️⃣  Running initial preprocessing..."
read -p "   Process your dataset now? [Y/n]: " -n 1 -r
echo ""
if [[ ! $REPLY =~ ^[Nn]$ ]]; then
    echo "   🔄 Processing texts..."
    python3 step1_preprocess.py
    echo ""
else
    echo "   ⏭️  Skipped (run manually: python3 step1_preprocess.py)"
fi

# Step 6: Summary
echo ""
echo "╔══════════════════════════════════════════════════════════════════╗"
echo "║   ✨ Setup Complete!                                             ║"
echo "╚══════════════════════════════════════════════════════════════════╝"
echo ""
echo "📚 Next Steps:"
echo ""
echo "1️⃣  Extract events from texts:"
echo "   python3 step2_extract_events.py"
echo ""
echo "2️⃣  Build the causal graph:"
echo "   python3 step3_build_graph.py"
echo ""
echo "3️⃣  Start the visualization server:"
echo "   cd connected_papers_demo"
echo "   python3 server.py"
echo "   # Then open: http://127.0.0.1:5001"
echo ""
echo "📖 For detailed instructions, read PROJECT_GUIDE.md"
echo ""
echo "💡 Pro tip: Start with small batches first!"
echo "   Edit step2_extract_events.py and set sample_size=10"
echo ""
