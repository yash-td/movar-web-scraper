#!/bin/bash

echo "╔═══════════════════════════════════════════════════════════╗"
echo "║  Movar Web Scraper - Netlify Deployment Script           ║"
echo "╚═══════════════════════════════════════════════════════════╝"
echo ""

# Check if Netlify CLI is installed
if ! command -v netlify &> /dev/null; then
    echo "❌ Netlify CLI not found"
    echo ""
    echo "Installing Netlify CLI..."
    npm install -g netlify-cli

    if [ $? -ne 0 ]; then
        echo "❌ Failed to install Netlify CLI"
        echo "Please install Node.js first: https://nodejs.org/"
        exit 1
    fi
fi

echo "✓ Netlify CLI found"
echo ""

# Login to Netlify
echo "🔐 Logging into Netlify..."
netlify login

if [ $? -ne 0 ]; then
    echo "❌ Failed to login to Netlify"
    exit 1
fi

echo "✓ Logged in successfully"
echo ""

# Initialize site
echo "🚀 Initializing Netlify site..."
netlify init

if [ $? -ne 0 ]; then
    echo "❌ Failed to initialize site"
    exit 1
fi

echo ""
echo "✓ Site initialized"
echo ""

# Deploy
echo "📦 Deploying to Netlify..."
netlify deploy --prod

if [ $? -ne 0 ]; then
    echo "❌ Deployment failed"
    exit 1
fi

echo ""
echo "╔═══════════════════════════════════════════════════════════╗"
echo "║  🎉 Deployment Successful!                                ║"
echo "╚═══════════════════════════════════════════════════════════╝"
echo ""
echo "Your site is now live!"
echo ""
echo "Next steps:"
echo "1. Visit your site URL (shown above)"
echo "2. Test the scraper with a sample website"
echo "3. Share the URL with others!"
echo ""
echo "To redeploy after changes:"
echo "  git add ."
echo "  git commit -m 'Update'"
echo "  git push"
echo ""
