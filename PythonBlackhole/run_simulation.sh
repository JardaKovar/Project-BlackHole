#!/bin/bash

echo "========================================"
echo "  BLACK HOLE SIMULATION LAUNCHER"
echo "========================================"
echo ""
echo "Checking dependencies..."

# Check if Python 3 is available
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is not installed!"
    exit 1
fi

# Check if required packages are installed
python3 -c "import numpy, colorama" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "Installing required packages..."
    pip3 install numpy colorama
fi

echo ""
echo "Starting simulation..."
echo ""
python3 black_hole_sim.py
