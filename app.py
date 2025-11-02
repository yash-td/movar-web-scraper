#!/usr/bin/env python3
"""
Web GUI for Universal Web Scraper & Downloader
Flask-based web interface
"""

from flask import Flask, render_template, request, jsonify, send_file, Response
import os
import json
import zipfile
from io import BytesIO
from scraper import LinkScraper
from downloader import FileDownloader
import threading
import uuid

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-here'

# Store active jobs
active_jobs = {}


class DownloadJob:
    """Represents a download job"""

    def __init__(self, job_id: str):
        self.job_id = job_id
        self.status = "pending"  # pending, scraping, downloading, completed, failed
        self.links = []
        self.progress = 0
        self.total = 0
        self.current_file = ""
        self.output_dir = f"downloads/{job_id}"
        self.error = None


@app.route('/')
def index():
    """Main page"""
    return render_template('index.html')


@app.route('/api/scrape', methods=['POST'])
def scrape():
    """API endpoint to scrape a webpage"""
    data = request.json

    url = data.get('url')
    if not url:
        return jsonify({'error': 'URL is required'}), 400

    try:
        scraper = LinkScraper(base_url=url)

        # Handle pagination
        pagination_mode = data.get('pagination_mode', 'single')
        links = []

        if pagination_mode == 'single':
            links = scraper.scrape_page(url)

        elif pagination_mode == 'auto':
            page_urls = scraper.auto_detect_pagination(url)
            for page_url in page_urls:
                links.extend(scraper.scrape_page(page_url))

        elif pagination_mode == 'manual':
            pattern = data.get('url_pattern', url)
            page_range = data.get('page_range', '1')
            page_numbers = parse_page_range(page_range)
            links = scraper.scrape_multiple_pages(pattern, page_numbers)

        # Filter by extensions if specified
        extensions = data.get('extensions', [])
        if extensions:
            extensions_set = {ext.lower().replace('.', '') for ext in extensions}
            links = [link for link in links if link['extension'] in extensions_set]

        # Remove duplicates
        seen = set()
        unique_links = []
        for link in links:
            if link['url'] not in seen:
                seen.add(link['url'])
                unique_links.append(link)

        # Get statistics
        stats = {}
        for link in unique_links:
            ext = link['extension']
            stats[ext] = stats.get(ext, 0) + 1

        return jsonify({
            'success': True,
            'links': unique_links,
            'count': len(unique_links),
            'statistics': stats
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/download', methods=['POST'])
def download():
    """API endpoint to start download job"""
    data = request.json

    links = data.get('links', [])
    if not links:
        return jsonify({'error': 'No links provided'}), 400

    # Create job
    job_id = str(uuid.uuid4())
    job = DownloadJob(job_id)
    job.links = links
    job.total = len(links)
    active_jobs[job_id] = job

    # Start download in background thread
    thread = threading.Thread(target=download_worker, args=(job,))
    thread.daemon = True
    thread.start()

    return jsonify({
        'success': True,
        'job_id': job_id
    })


@app.route('/api/job/<job_id>')
def get_job_status(job_id):
    """Get status of a download job"""
    job = active_jobs.get(job_id)

    if not job:
        return jsonify({'error': 'Job not found'}), 404

    return jsonify({
        'job_id': job_id,
        'status': job.status,
        'progress': job.progress,
        'total': job.total,
        'current_file': job.current_file,
        'error': job.error
    })


@app.route('/api/download-zip/<job_id>')
def download_zip(job_id):
    """Download all files as a ZIP"""
    job = active_jobs.get(job_id)

    if not job:
        return jsonify({'error': 'Job not found'}), 404

    if job.status != 'completed':
        return jsonify({'error': 'Job not completed yet'}), 400

    # Create ZIP in memory
    memory_file = BytesIO()

    with zipfile.ZipFile(memory_file, 'w', zipfile.ZIP_DEFLATED) as zf:
        # Add all downloaded files
        for filename in os.listdir(job.output_dir):
            file_path = os.path.join(job.output_dir, filename)
            if os.path.isfile(file_path):
                zf.write(file_path, filename)

    memory_file.seek(0)

    return send_file(
        memory_file,
        mimetype='application/zip',
        as_attachment=True,
        download_name=f'download_{job_id}.zip'
    )


def download_worker(job: DownloadJob):
    """Background worker to download files"""
    try:
        job.status = "downloading"

        downloader = FileDownloader(output_dir=job.output_dir, rate_limit=0.3)

        for i, link in enumerate(job.links):
            job.current_file = link['text'][:50]
            job.progress = i

            downloader.download_file(link['url'])

        job.progress = job.total
        job.status = "completed"

    except Exception as e:
        job.status = "failed"
        job.error = str(e)


def parse_page_range(page_range: str):
    """Parse page range string"""
    try:
        pages = []
        parts = page_range.split(',')
        for part in parts:
            part = part.strip()
            if '-' in part:
                start, end = part.split('-')
                pages.extend(range(int(start), int(end) + 1))
            else:
                pages.append(int(part))
        return sorted(list(set(pages)))
    except:
        return [1]


if __name__ == '__main__':
    # Create downloads directory
    os.makedirs('downloads', exist_ok=True)

    print("""
    ╔═══════════════════════════════════════════════════════════╗
    ║    Universal Web Scraper & Downloader - Web Interface    ║
    ╚═══════════════════════════════════════════════════════════╝

    Starting web server...
    Open your browser and navigate to: http://localhost:5000

    Press Ctrl+C to stop the server
    """)

    app.run(debug=True, host='0.0.0.0', port=5000)
