#!/bin/bash

echo "========================================"
echo "   FlowCast Report Generator"
echo "========================================"
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python 3 is not installed"
    echo "Please install Python from https://python.org"
    exit 1
fi

# Check if pip dependencies are installed
if ! python3 -c "import streamlit" &> /dev/null; then
    echo "Installing required packages..."
    pip3 install -r requirements.txt
fi

echo ""
echo "Starting FlowCast..."
echo ""
echo "The app will open in your web browser automatically."
echo "To stop the app, press Ctrl+C"
echo ""

# Run the streamlit app
python3 -m streamlit run flowcast_app.py
