# Netlify Functions

This directory contains serverless functions for the Movar Web Scraper.

## Functions

### scrape.js
Main scraping function (JavaScript/Node.js)
- **Language**: JavaScript (Node.js)
- **Dependencies**: axios, cheerio
- **Endpoint**: `/.netlify/functions/scrape`

JavaScript functions are natively supported by Netlify with zero configuration.

### scrape.py.backup
Original Python version (backup)
- Python functions require additional setup and may have compatibility issues
- Kept as backup for reference

### test.py
Simple test function to verify Python support

## Why JavaScript?

JavaScript/Node.js functions are:
- ✅ Natively supported by Netlify
- ✅ Zero configuration required
- ✅ Faster cold start times
- ✅ More reliable on free tier

## Dependencies

Dependencies are managed via `package.json` and automatically installed by Netlify during deployment.
