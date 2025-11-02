#!/bin/bash

# Quick Start Script for Universal Web Scraper & Downloader

echo "╔═══════════════════════════════════════════════════════════╗"
echo "║    Universal Web Scraper & Downloader - Quick Start      ║"
echo "╚═══════════════════════════════════════════════════════════╝"
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3 first."
    exit 1
fi

echo "✓ Python 3 found"

# Check if pip is installed
if ! command -v pip3 &> /dev/null; then
    echo "❌ pip3 is not installed. Please install pip3 first."
    exit 1
fi

echo "✓ pip3 found"

# Install dependencies
echo ""
echo "📦 Installing dependencies..."
pip3 install -r requirements.txt

if [ $? -ne 0 ]; then
    echo "❌ Failed to install dependencies"
    exit 1
fi

echo "✓ Dependencies installed successfully"
echo ""

# Ask user which mode to run
echo "Choose how to run the app:"
echo "1. Web Interface (recommended)"
echo "2. Command Line Interface"
echo ""
read -p "Enter choice (1 or 2): " choice

case $choice in
    1)
        echo ""
        echo "🚀 Starting web interface..."
        echo "Open your browser to: http://localhost:5000"
        echo ""
        python3 app.py
        ;;
    2)
        echo ""
        echo "🚀 Starting command line interface..."
        echo ""
        python3 main.py
        ;;
    *)
        echo "Invalid choice. Exiting."
        exit 1
        ;;
esac
