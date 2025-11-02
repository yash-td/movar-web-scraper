"""
Netlify Function: Scrape links from a webpage
"""

import json
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse


# Common downloadable file extensions
DOWNLOADABLE_EXTENSIONS = {
    'pdf', 'doc', 'docx', 'xls', 'xlsx', 'ppt', 'pptx',
    'zip', 'rar', '7z', 'tar', 'gz',
    'txt', 'csv', 'json', 'xml',
    'jpg', 'jpeg', 'png', 'gif', 'svg',
    'mp3', 'mp4', 'avi', 'mov', 'wmv',
}


def get_extension(url):
    """Extract file extension from URL"""
    parsed = urlparse(url)
    path = parsed.path.split('?')[0].split('#')[0]
    if '.' in path:
        return path.rsplit('.', 1)[-1].lower()
    return ''


def scrape_page(url, filter_extensions=None):
    """Scrape a single page for downloadable links"""
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }

        response = requests.get(url, timeout=8, headers=headers)
        response.raise_for_status()

        soup = BeautifulSoup(response.content, 'html.parser')
        links = []
        seen_urls = set()

        for tag in soup.find_all('a', href=True):
            href = tag['href']
            link_text = tag.get_text(strip=True) or 'No description'
            full_url = urljoin(url, href)
            extension = get_extension(full_url)

            # Filter by extension if specified
            if filter_extensions and extension not in filter_extensions:
                continue

            # Only include downloadable files
            if extension not in DOWNLOADABLE_EXTENSIONS:
                continue

            # Avoid duplicates
            if full_url in seen_urls:
                continue

            seen_urls.add(full_url)
            links.append({
                'url': full_url,
                'text': link_text[:100],  # Limit text length
                'extension': extension
            })

        return links

    except Exception as e:
        raise Exception(f"Error scraping {url}: {str(e)}")


def parse_page_range(page_range):
    """Parse page range string into list of page numbers"""
    try:
        pages = []
        parts = page_range.split(',')
        for part in parts:
            part = part.strip()
            if '-' in part:
                start, end = part.split('-')
                # Limit to 10 pages max for Netlify timeout
                pages.extend(range(int(start), min(int(end) + 1, int(start) + 10)))
            else:
                pages.append(int(part))
        return sorted(list(set(pages)))[:10]  # Max 10 pages
    except:
        return [1]


def handler(event, context):
    """Netlify Function handler"""

    # CORS headers
    headers = {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Headers': 'Content-Type',
        'Access-Control-Allow-Methods': 'POST, OPTIONS',
        'Content-Type': 'application/json'
    }

    # Handle OPTIONS request for CORS
    if event.get('httpMethod') == 'OPTIONS':
        return {
            'statusCode': 200,
            'headers': headers,
            'body': ''
        }

    try:
        # Parse request body
        body = json.loads(event.get('body', '{}'))

        url = body.get('url')
        if not url:
            return {
                'statusCode': 400,
                'headers': headers,
                'body': json.dumps({'error': 'URL is required'})
            }

        pagination_mode = body.get('pagination_mode', 'single')
        extensions = body.get('extensions', [])
        extensions_set = {ext.lower().replace('.', '') for ext in extensions} if extensions else None

        links = []

        if pagination_mode == 'single':
            links = scrape_page(url, extensions_set)

        elif pagination_mode == 'manual':
            pattern = body.get('url_pattern', url)
            page_range = body.get('page_range', '1')
            page_numbers = parse_page_range(page_range)

            for page_num in page_numbers:
                page_url = pattern.replace('{page}', str(page_num))
                try:
                    page_links = scrape_page(page_url, extensions_set)
                    links.extend(page_links)
                except:
                    continue

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

        return {
            'statusCode': 200,
            'headers': headers,
            'body': json.dumps({
                'success': True,
                'links': unique_links,
                'count': len(unique_links),
                'statistics': stats
            })
        }

    except Exception as e:
        return {
            'statusCode': 500,
            'headers': headers,
            'body': json.dumps({'error': str(e)})
        }
