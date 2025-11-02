"""
Web scraper module for extracting downloadable links from any webpage
"""

import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse, urlunparse
import re
from typing import List, Set, Dict


class LinkScraper:
    """Scraper to extract downloadable links from webpages"""

    # Common downloadable file extensions
    DOWNLOADABLE_EXTENSIONS = {
        'pdf', 'doc', 'docx', 'xls', 'xlsx', 'ppt', 'pptx',
        'zip', 'rar', '7z', 'tar', 'gz',
        'txt', 'csv', 'json', 'xml',
        'jpg', 'jpeg', 'png', 'gif', 'svg',
        'mp3', 'mp4', 'avi', 'mov', 'wmv',
        'exe', 'dmg', 'apk', 'deb', 'rpm'
    }

    def __init__(self, base_url: str, timeout: int = 30):
        """
        Initialize scraper

        Args:
            base_url: The base URL of the website
            timeout: Request timeout in seconds
        """
        self.base_url = base_url
        self.timeout = timeout
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })

    def scrape_page(self, url: str, filter_extensions: Set[str] = None) -> List[Dict[str, str]]:
        """
        Scrape a single page for downloadable links

        Args:
            url: URL to scrape
            filter_extensions: Set of file extensions to filter (e.g., {'pdf', 'doc'})
                             If None, returns all downloadable files

        Returns:
            List of dictionaries containing link info: {'url': str, 'text': str, 'extension': str}
        """
        try:
            response = self.session.get(url, timeout=self.timeout)
            response.raise_for_status()

            soup = BeautifulSoup(response.content, 'html.parser')
            links = []
            seen_urls = set()

            # Find all <a> tags with href
            for tag in soup.find_all('a', href=True):
                href = tag['href']

                # Get link text
                link_text = tag.get_text(strip=True) or 'No description'

                # Normalize URL
                full_url = urljoin(url, href)

                # Get extension
                extension = self._get_extension(full_url)

                # Filter by extension if specified
                if filter_extensions and extension not in filter_extensions:
                    continue

                # Only include downloadable files
                if extension not in self.DOWNLOADABLE_EXTENSIONS:
                    continue

                # Avoid duplicates
                if full_url in seen_urls:
                    continue

                seen_urls.add(full_url)
                links.append({
                    'url': full_url,
                    'text': link_text,
                    'extension': extension
                })

            return links

        except requests.RequestException as e:
            print(f"Error scraping {url}: {e}")
            return []

    def scrape_multiple_pages(self,
                            base_pattern: str,
                            page_numbers: List[int],
                            filter_extensions: Set[str] = None) -> List[Dict[str, str]]:
        """
        Scrape multiple pages with pagination

        Args:
            base_pattern: URL pattern with {page} placeholder
                         Example: "https://example.com/docs/page/{page}"
            page_numbers: List of page numbers to scrape
            filter_extensions: Set of file extensions to filter

        Returns:
            Combined list of all links from all pages
        """
        all_links = []

        for page_num in page_numbers:
            url = base_pattern.format(page=page_num)
            print(f"Scraping page {page_num}: {url}")

            links = self.scrape_page(url, filter_extensions)
            all_links.extend(links)

            print(f"  Found {len(links)} links")

        # Remove duplicates across pages
        seen = set()
        unique_links = []
        for link in all_links:
            if link['url'] not in seen:
                seen.add(link['url'])
                unique_links.append(link)

        return unique_links

    def auto_detect_pagination(self, url: str) -> List[str]:
        """
        Attempt to detect and extract pagination links from a page

        Args:
            url: URL to analyze

        Returns:
            List of discovered page URLs
        """
        try:
            response = self.session.get(url, timeout=self.timeout)
            response.raise_for_status()

            soup = BeautifulSoup(response.content, 'html.parser')
            page_urls = set([url])

            # Look for common pagination patterns
            pagination_selectors = [
                '.pagination a',
                '.pager a',
                'nav a',
                'a[rel="next"]',
                'a[rel="prev"]',
                'a.page-link',
                'a.page-numbers'
            ]

            for selector in pagination_selectors:
                for link in soup.select(selector):
                    href = link.get('href')
                    if href:
                        full_url = urljoin(url, href)
                        # Only add if it looks like a page URL (contains digits)
                        if re.search(r'/page/\d+|[\?&]page=\d+|\d+/?$', full_url):
                            page_urls.add(full_url)

            return sorted(list(page_urls))

        except requests.RequestException as e:
            print(f"Error detecting pagination: {e}")
            return [url]

    def _get_extension(self, url: str) -> str:
        """
        Extract file extension from URL

        Args:
            url: URL to parse

        Returns:
            File extension in lowercase (without dot)
        """
        parsed = urlparse(url)
        path = parsed.path

        # Remove query parameters and fragments
        path = path.split('?')[0].split('#')[0]

        # Get extension
        if '.' in path:
            ext = path.rsplit('.', 1)[-1].lower()
            return ext

        return ''

    def get_statistics(self, links: List[Dict[str, str]]) -> Dict[str, int]:
        """
        Get statistics about scraped links

        Args:
            links: List of link dictionaries

        Returns:
            Dictionary with statistics by file type
        """
        stats = {}
        for link in links:
            ext = link['extension']
            stats[ext] = stats.get(ext, 0) + 1

        return stats
