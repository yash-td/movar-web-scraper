# 🚀 Deploying Movar Web Scraper to Netlify

This guide will walk you through deploying your web scraper to Netlify.

## 📋 Prerequisites

- A GitHub account
- A Netlify account (free tier is fine)
- Git installed on your computer

## 🎯 Quick Deploy

### Option 1: Deploy from GitHub (Recommended)

1. **Push to GitHub**

```bash
# Navigate to your project
cd /Users/ytkd/Desktop/code/web-scraper-download

# Initialize git (if not already done)
git init

# Add all files
git add .

# Commit
git commit -m "Initial commit - Movar Web Scraper"

# Create a new repository on GitHub named 'movar-web-scraper'
# Then connect and push:
git remote add origin https://github.com/YOUR_USERNAME/movar-web-scraper.git
git branch -M main
git push -u origin main
```

2. **Connect to Netlify**

- Go to [Netlify](https://app.netlify.com)
- Click "Add new site" → "Import an existing project"
- Choose "Deploy with GitHub"
- Select your `movar-web-scraper` repository
- Netlify will auto-detect the settings from `netlify.toml`
- Click "Deploy site"

3. **Configure Site Name**

- Once deployed, go to Site settings
- Change site name to `movar-web-scraper`
- Your site will be at: `https://movar-web-scraper.netlify.app`

### Option 2: Deploy with Netlify CLI

```bash
# Install Netlify CLI
npm install -g netlify-cli

# Login to Netlify
netlify login

# Deploy (from project directory)
cd /Users/ytkd/Desktop/code/web-scraper-download
netlify init

# Follow the prompts:
# - Create & configure a new site
# - Team: Choose your team
# - Site name: movar-web-scraper
# - Build command: (leave empty)
# - Directory to deploy: public
# - Netlify functions folder: netlify/functions

# Deploy
netlify deploy --prod
```

### Option 3: Manual Drag & Drop

1. Go to [Netlify Drop](https://app.netlify.com/drop)
2. Drag the entire `web-scraper-download` folder
3. Netlify will deploy it automatically

Note: This method won't auto-deploy updates when you push to Git.

## 📁 Project Structure for Netlify

```
web-scraper-download/
├── netlify/
│   └── functions/
│       ├── scrape.py          # Scraping function
│       └── requirements.txt   # Python dependencies
├── public/
│   └── index.html            # Static frontend
├── netlify.toml              # Netlify configuration
└── runtime.txt               # Python version
```

## ⚙️ Configuration Files

### netlify.toml
Configures:
- Build settings
- Functions directory
- CORS headers
- Python runtime
- Function timeout (26 seconds max)

### runtime.txt
Specifies Python 3.11 for Netlify Functions

### netlify/functions/requirements.txt
Python packages for serverless functions:
- requests
- beautifulsoup4
- lxml

## 🔧 Post-Deployment Configuration

### Custom Domain (Optional)

1. Go to Site settings → Domain management
2. Click "Add custom domain"
3. Follow instructions to configure DNS

### Environment Variables (If needed)

1. Go to Site settings → Environment variables
2. Add any required variables
3. Redeploy for changes to take effect

## 🧪 Testing Your Deployment

1. Visit `https://YOUR_SITE_NAME.netlify.app`
2. Try scraping a public website:
   - URL: `https://example.com`
   - Click "Scrape Links"
3. Download found files

## ⚠️ Important Limitations

### Netlify Free Tier Limits:
- **Function timeout**: 10 seconds (26 seconds for paid)
- **Function invocations**: 125,000/month
- **Bandwidth**: 100 GB/month
- **Build minutes**: 300/month

### Scraping Limitations:
- Limited to 10 pages per scrape (to stay within timeout)
- Some sites may block scraping from Netlify IPs
- CORS restrictions may affect some sites
- Downloads are client-side (browser downloads each file)

## 🐛 Troubleshooting

### Function Timeout

If scraping takes too long:
- Reduce page count (max 5 pages)
- Use single page mode
- Filter by specific file types

### CORS Errors

Some websites block requests from browsers:
- This is normal browser security
- Try different URLs
- Some sites require authentication

### Build Errors

If deployment fails:
```bash
# Check logs in Netlify dashboard
# Common fixes:

# 1. Ensure runtime.txt has: 3.11
# 2. Check requirements.txt syntax
# 3. Verify netlify.toml is valid
```

### Function Errors

Check function logs:
1. Go to Netlify dashboard
2. Functions → Select function
3. View logs

## 🔄 Updating Your Site

### With Git/GitHub:
```bash
git add .
git commit -m "Update scraper"
git push
```
Netlify auto-deploys on push!

### Manual Update:
1. Make changes locally
2. Run `netlify deploy --prod`

## 📊 Monitoring

View analytics in Netlify dashboard:
- Function invocations
- Bandwidth usage
- Error rates
- Deployment history

## 🆙 Upgrading

### To Remove Limitations:

Consider upgrading to:
- **Netlify Pro**: Longer function timeout (26s)
- **Self-hosted option**: Use Railway/Render for full Python Flask app

See `README.md` for self-hosted deployment options.

## 🎉 Success!

Your Movar Web Scraper is now live at:
`https://movar-web-scraper.netlify.app`

Share it with others and happy scraping! 🌐

## 📝 Additional Resources

- [Netlify Functions Docs](https://docs.netlify.com/functions/overview/)
- [Netlify Python Functions](https://docs.netlify.com/functions/build-with-python/)
- [Netlify TOML Reference](https://docs.netlify.com/configure-builds/file-based-configuration/)

---

**Need Help?** Check the issues on GitHub or contact support.
