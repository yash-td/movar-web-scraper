"""
File downloader module for downloading files from URLs
"""

import os
import time
import requests
from pathlib import Path
from urllib.parse import urlparse, unquote
from typing import List, Dict, Callable, Optional
import re


class FileDownloader:
    """Handles downloading files from URLs"""

    def __init__(self,
                 output_dir: str = "downloads",
                 timeout: int = 60,
                 chunk_size: int = 8192,
                 rate_limit: float = 0.5):
        """
        Initialize downloader

        Args:
            output_dir: Directory to save downloaded files
            timeout: Request timeout in seconds
            chunk_size: Size of chunks for streaming downloads
            rate_limit: Delay between downloads in seconds
        """
        self.output_dir = output_dir
        self.timeout = timeout
        self.chunk_size = chunk_size
        self.rate_limit = rate_limit

        # Create output directory
        Path(output_dir).mkdir(parents=True, exist_ok=True)

        # Setup session
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })

    def download_file(self,
                     url: str,
                     filename: Optional[str] = None,
                     progress_callback: Optional[Callable] = None) -> bool:
        """
        Download a single file

        Args:
            url: URL to download
            filename: Optional custom filename (will extract from URL if not provided)
            progress_callback: Optional callback function(current, total)

        Returns:
            True if successful, False otherwise
        """
        try:
            # Get filename
            if not filename:
                filename = self._get_filename_from_url(url)

            # Sanitize filename
            filename = self._sanitize_filename(filename)

            output_path = os.path.join(self.output_dir, filename)

            # Skip if file already exists
            if os.path.exists(output_path):
                return True

            # Download file
            response = self.session.get(url, timeout=self.timeout, stream=True)
            response.raise_for_status()

            # Get file size
            total_size = int(response.headers.get('content-length', 0))

            # Download with progress
            downloaded = 0
            with open(output_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=self.chunk_size):
                    if chunk:
                        f.write(chunk)
                        downloaded += len(chunk)

                        if progress_callback and total_size:
                            progress_callback(downloaded, total_size)

            return True

        except Exception as e:
            print(f"Error downloading {url}: {e}")
            # Clean up partial file
            if 'output_path' in locals() and os.path.exists(output_path):
                os.remove(output_path)
            return False

    def download_batch(self,
                      links: List[Dict[str, str]],
                      show_progress: bool = True) -> Dict[str, any]:
        """
        Download multiple files

        Args:
            links: List of link dictionaries with 'url' and 'text' keys
            show_progress: Whether to show progress output

        Returns:
            Dictionary with download statistics
        """
        total = len(links)
        successful = 0
        failed = 0
        skipped = 0
        failed_urls = []

        print(f"\n{'='*60}")
        print(f"Starting batch download: {total} files")
        print(f"Output directory: {os.path.abspath(self.output_dir)}")
        print(f"{'='*60}\n")

        for i, link in enumerate(links, 1):
            url = link['url']
            filename = self._get_filename_from_url(url)
            output_path = os.path.join(self.output_dir, self._sanitize_filename(filename))

            if show_progress:
                print(f"[{i}/{total}] ", end="")

            # Check if already exists
            if os.path.exists(output_path):
                if show_progress:
                    print(f"✓ Skipped (exists): {filename}")
                skipped += 1
                continue

            # Download
            success = self.download_file(url)

            if success:
                if show_progress:
                    print(f"✓ Downloaded: {filename}")
                successful += 1
            else:
                if show_progress:
                    print(f"✗ Failed: {filename}")
                failed += 1
                failed_urls.append(url)

            # Rate limiting
            if i < total:
                time.sleep(self.rate_limit)

        # Summary
        print(f"\n{'='*60}")
        print(f"Download Complete!")
        print(f"Successful: {successful}")
        print(f"Skipped (already exist): {skipped}")
        print(f"Failed: {failed}")
        print(f"Total: {total}")
        print(f"Files saved to: {os.path.abspath(self.output_dir)}")
        print(f"{'='*60}\n")

        return {
            'total': total,
            'successful': successful,
            'skipped': skipped,
            'failed': failed,
            'failed_urls': failed_urls
        }

    def _get_filename_from_url(self, url: str) -> str:
        """
        Extract filename from URL

        Args:
            url: URL to parse

        Returns:
            Filename
        """
        # Parse URL
        parsed = urlparse(url)
        path = unquote(parsed.path)

        # Get filename from path
        filename = os.path.basename(path)

        # If no filename, generate one
        if not filename or '.' not in filename:
            # Use domain and timestamp
            domain = parsed.netloc.replace('www.', '')
            timestamp = int(time.time())
            filename = f"{domain}_{timestamp}.file"

        return filename

    def _sanitize_filename(self, filename: str) -> str:
        """
        Sanitize filename to remove problematic characters

        Args:
            filename: Original filename

        Returns:
            Sanitized filename
        """
        # Remove/replace problematic characters
        filename = re.sub(r'[<>:"/\\|?*]', '_', filename)

        # Remove control characters
        filename = ''.join(char for char in filename if ord(char) >= 32)

        # Limit length
        name, ext = os.path.splitext(filename)
        if len(name) > 200:
            name = name[:200]
        filename = name + ext

        # Ensure not empty
        if not filename:
            filename = f"file_{int(time.time())}"

        return filename

    def set_output_dir(self, output_dir: str):
        """
        Change output directory

        Args:
            output_dir: New output directory path
        """
        self.output_dir = output_dir
        Path(output_dir).mkdir(parents=True, exist_ok=True)
