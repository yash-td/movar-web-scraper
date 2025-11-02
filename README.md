# 🌐 Universal Web Scraper & Downloader

A powerful tool to scrape downloadable links from any webpage and download them all automatically. Supports both command-line interface and a beautiful web interface.

## ✨ Features

- **Universal Link Extraction**: Scrape any webpage for downloadable files
- **Smart Pagination**: Auto-detect or manually specify multiple pages
- **File Type Filtering**: Download only specific file types (PDF, DOC, ZIP, etc.)
- **Dual Interface**: Both CLI and Web GUI available
- **Batch Download**: Download hundreds of files automatically
- **Progress Tracking**: Real-time progress updates
- **Duplicate Prevention**: Automatically skips already downloaded files
- **ZIP Export**: Combine all downloads into a single ZIP file (Web GUI)

## 🚀 Quick Start

### Installation

1. Clone or download this repository
2. Install dependencies:

```bash
pip install -r requirements.txt
```

### Usage

#### Option 1: Web Interface (Recommended)

```bash
python app.py
```

Then open your browser to `http://localhost:5000`

**Web Interface Features:**
- Beautiful, modern UI
- Real-time progress tracking
- Download all files as a single ZIP
- Interactive file preview

#### Option 2: Command Line Interface

**Interactive Mode** (easiest):
```bash
python main.py
```

**Direct Commands**:

```bash
# Download all files from a single page
python main.py --url https://example.com/documents

# Download only PDFs from multiple pages
python main.py --url "https://example.com/docs/page/{page}" --pages 1-10 --extensions pdf

# Download PDFs and DOCs to a custom directory
python main.py --url https://example.com/docs --extensions pdf,doc --output my-docs

# Skip confirmation prompt
python main.py --url https://example.com/docs -y
```

## 📖 Detailed Usage

### Web Interface Guide

1. **Enter URL**: Paste the webpage URL you want to scrape
2. **Pagination**: Choose how to handle multiple pages:
   - **Single page**: Scrape only the URL provided
   - **Auto-detect**: Automatically find and scrape all pages
   - **Manual**: Specify page pattern and range
3. **Filter Extensions**: Optionally filter by file types (e.g., `pdf, doc, zip`)
4. **Scrape**: Click "Scrape Links" to find all downloadable files
5. **Review**: See all found files and statistics
6. **Download**: Click "Download All Files" to start batch download
7. **ZIP Export**: Download everything as a single ZIP file when complete

### CLI Guide

#### Interactive Mode

Run `python main.py` and follow the prompts:

1. Enter the webpage URL
2. Choose pagination mode:
   - Single page
   - Auto-detect pagination
   - Manual pagination (specify pattern and range)
3. Optionally filter by file types
4. Review found files and statistics
5. Confirm download
6. Specify output directory

#### Command-Line Arguments

```
--url URL              URL to scrape (use {page} placeholder for pagination)
--pages PAGES          Page range (e.g., "1-10" or "1,2,3,5")
--extensions EXT       Comma-separated extensions (e.g., "pdf,doc,zip")
--output DIR          Output directory (default: downloads)
--yes, -y             Skip confirmation prompt
```

## 📝 Examples

### Example 1: Download All PDFs from a Document Library

**Web Interface:**
1. URL: `https://example.com/documents`
2. Pagination: Auto-detect
3. Extensions: `pdf`
4. Click "Scrape Links" then "Download All Files"

**CLI:**
```bash
python main.py --url https://example.com/documents --extensions pdf -y
```

### Example 2: Scrape Multiple Pages

**Web Interface:**
1. URL: Leave blank
2. Pagination: Manual
3. URL Pattern: `https://example.com/docs/page/{page}`
4. Page Range: `1-20`

**CLI:**
```bash
python main.py --url "https://example.com/docs/page/{page}" --pages 1-20
```

### Example 3: Download Specific File Types Only

**CLI:**
```bash
# Download only PDFs, DOCs, and PPTs
python main.py --url https://example.com/resources --extensions pdf,doc,ppt,docx,pptx
```

## 🛠️ API Module Usage

You can also use the modules programmatically:

```python
from scraper import LinkScraper
from downloader import FileDownloader

# Scrape links
scraper = LinkScraper(base_url="https://example.com")
links = scraper.scrape_page("https://example.com/documents")

# Filter PDFs only
pdf_links = [link for link in links if link['extension'] == 'pdf']

# Download
downloader = FileDownloader(output_dir="my_downloads")
downloader.download_batch(pdf_links)
```

## 📂 Project Structure

```
web-scraper-download/
├── scraper.py              # Link scraping module
├── downloader.py           # File download module
├── main.py                 # CLI interface
├── app.py                  # Web GUI (Flask)
├── templates/
│   └── index.html         # Web interface template
├── requirements.txt        # Python dependencies
├── download_awe_docs.py   # Original AWE-specific scraper
└── README.md              # This file
```

## 🎯 Supported File Types

The scraper automatically detects these downloadable file types:

**Documents**: pdf, doc, docx, xls, xlsx, ppt, pptx, txt, csv
**Archives**: zip, rar, 7z, tar, gz
**Data**: json, xml
**Images**: jpg, jpeg, png, gif, svg
**Media**: mp3, mp4, avi, mov, wmv
**Executables**: exe, dmg, apk, deb, rpm

## ⚙️ Configuration

### Scraper Configuration

In `scraper.py`, you can modify:
- `DOWNLOADABLE_EXTENSIONS`: Add/remove supported file types
- `timeout`: Request timeout (default: 30 seconds)

### Downloader Configuration

In `downloader.py`, you can modify:
- `chunk_size`: Download chunk size (default: 8192 bytes)
- `rate_limit`: Delay between downloads (default: 0.5 seconds)
- `timeout`: Download timeout (default: 60 seconds)

## 🚨 Important Notes

### Rate Limiting
The tool includes a 0.5-second delay between downloads to be respectful to web servers. Adjust `rate_limit` in the FileDownloader if needed.

### Robots.txt
Please respect website robots.txt files and terms of service. This tool is for legitimate use cases like:
- Downloading public documents
- Backing up your own content
- Research and archival purposes

### Large Downloads
For large file collections:
- Use CLI mode for better performance
- Monitor disk space
- Consider downloading in batches

### Troubleshooting

**No files found?**
- Check if the website uses JavaScript to load content
- Try different pagination modes
- Verify the URL is correct

**Download fails?**
- Some files may require authentication
- Check your internet connection
- Increase timeout in configuration

**Permission errors?**
- Ensure you have write permissions in the output directory
- Try a different output directory

## 🤝 Contributing

Feel free to submit issues, fork the repository, and create pull requests!

## 📄 License

This project is open source and available for personal and educational use.

## 🙏 Credits

Built with:
- [Requests](https://requests.readthedocs.io/) - HTTP library
- [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/) - HTML parsing
- [Flask](https://flask.palletsprojects.com/) - Web framework

---

**Happy Scraping! 🎉**

For questions or issues, please open an issue on the repository.
