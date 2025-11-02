#!/usr/bin/env python3
"""
Universal Web Scraper & Downloader
A tool to scrape downloadable links from any webpage and download them all
"""

import sys
import argparse
from scraper import LinkScraper
from downloader import FileDownloader


def print_banner():
    """Print application banner"""
    banner = """
    ╔═══════════════════════════════════════════════════════════╗
    ║    Universal Web Scraper & Downloader                     ║
    ║    Extract and download files from any webpage            ║
    ╚═══════════════════════════════════════════════════════════╝
    """
    print(banner)


def interactive_mode():
    """Run in interactive mode with user prompts"""
    print_banner()

    # Get URL
    url = input("Enter the webpage URL to scrape: ").strip()
    if not url:
        print("Error: URL is required")
        return

    # Initialize scraper
    scraper = LinkScraper(base_url=url)

    # Ask about pagination
    print("\n--- Pagination Options ---")
    print("1. Single page only")
    print("2. Auto-detect pagination")
    print("3. Manual pagination (e.g., page 1-10)")

    pagination_choice = input("\nSelect option (1/2/3): ").strip()

    links = []

    if pagination_choice == "1":
        # Single page
        links = scraper.scrape_page(url)

    elif pagination_choice == "2":
        # Auto-detect pagination
        print("\nAuto-detecting pagination...")
        page_urls = scraper.auto_detect_pagination(url)
        print(f"Found {len(page_urls)} pages")

        for page_url in page_urls:
            print(f"Scraping: {page_url}")
            links.extend(scraper.scrape_page(page_url))

    elif pagination_choice == "3":
        # Manual pagination
        pattern = input("\nEnter URL pattern with {page} placeholder\n(e.g., https://example.com/docs/page/{page}): ").strip()
        page_range = input("Enter page range (e.g., 1-10 or 1,2,3,5): ").strip()

        # Parse page range
        page_numbers = parse_page_range(page_range)
        if not page_numbers:
            print("Invalid page range")
            return

        links = scraper.scrape_multiple_pages(pattern, page_numbers)

    else:
        print("Invalid option")
        return

    # Remove duplicates
    seen_urls = set()
    unique_links = []
    for link in links:
        if link['url'] not in seen_urls:
            seen_urls.add(link['url'])
            unique_links.append(link)

    links = unique_links

    if not links:
        print("\n❌ No downloadable files found!")
        return

    # Show statistics
    print(f"\n{'='*60}")
    print(f"Found {len(links)} downloadable files")

    stats = scraper.get_statistics(links)
    print("\nFile types breakdown:")
    for ext, count in sorted(stats.items(), key=lambda x: x[1], reverse=True):
        print(f"  .{ext}: {count} files")

    # Ask about filtering
    print(f"\n{'='*60}")
    filter_choice = input("\nFilter by file type? (y/n): ").strip().lower()

    if filter_choice == 'y':
        extensions = input("Enter extensions to download (comma-separated, e.g., pdf,doc,zip): ").strip()
        if extensions:
            filter_exts = {ext.strip().lower().replace('.', '') for ext in extensions.split(',')}
            links = [link for link in links if link['extension'] in filter_exts]
            print(f"\nFiltered to {len(links)} files")

    if not links:
        print("\n❌ No files match the filter!")
        return

    # Show preview
    print(f"\n{'='*60}")
    print("Preview of files to download:")
    for i, link in enumerate(links[:10], 1):
        print(f"{i}. [{link['extension'].upper()}] {link['text'][:60]}")
    if len(links) > 10:
        print(f"... and {len(links) - 10} more")

    # Confirm download
    print(f"\n{'='*60}")
    confirm = input(f"\nDownload {len(links)} files? (y/n): ").strip().lower()

    if confirm != 'y':
        print("Download cancelled")
        return

    # Get output directory
    output_dir = input("\nEnter output directory (press Enter for 'downloads'): ").strip()
    if not output_dir:
        output_dir = "downloads"

    # Download
    downloader = FileDownloader(output_dir=output_dir)
    results = downloader.download_batch(links)

    # Show failed downloads
    if results['failed'] > 0:
        print("\nFailed downloads:")
        for url in results['failed_urls']:
            print(f"  - {url}")


def command_line_mode(args):
    """Run in command-line mode with arguments"""
    print_banner()

    scraper = LinkScraper(base_url=args.url)

    # Scrape links
    if args.pages:
        page_numbers = parse_page_range(args.pages)
        if not page_numbers:
            print("Error: Invalid page range")
            sys.exit(1)

        pattern = args.url if '{page}' in args.url else f"{args.url}/page/{{page}}"
        links = scraper.scrape_multiple_pages(pattern, page_numbers, filter_extensions=args.extensions)
    else:
        links = scraper.scrape_page(args.url, filter_extensions=args.extensions)

    if not links:
        print("❌ No downloadable files found!")
        sys.exit(1)

    # Show statistics
    print(f"\nFound {len(links)} downloadable files")
    stats = scraper.get_statistics(links)
    print("\nFile types:")
    for ext, count in sorted(stats.items(), key=lambda x: x[1], reverse=True):
        print(f"  .{ext}: {count}")

    if not args.yes:
        confirm = input(f"\nDownload {len(links)} files? (y/n): ").strip().lower()
        if confirm != 'y':
            print("Download cancelled")
            sys.exit(0)

    # Download
    downloader = FileDownloader(output_dir=args.output)
    downloader.download_batch(links)


def parse_page_range(page_range: str):
    """
    Parse page range string into list of page numbers

    Args:
        page_range: String like "1-10" or "1,2,3,5"

    Returns:
        List of page numbers
    """
    try:
        pages = []

        # Handle ranges and individual numbers
        parts = page_range.split(',')
        for part in parts:
            part = part.strip()
            if '-' in part:
                # Range
                start, end = part.split('-')
                pages.extend(range(int(start), int(end) + 1))
            else:
                # Individual number
                pages.append(int(part))

        return sorted(list(set(pages)))  # Remove duplicates and sort

    except (ValueError, AttributeError):
        return []


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description="Universal Web Scraper & Downloader - Extract and download files from any webpage",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Interactive mode
  python main.py

  # Download all files from a page
  python main.py --url https://example.com/documents

  # Download only PDFs from multiple pages
  python main.py --url "https://example.com/docs/page/{page}" --pages 1-10 --extensions pdf

  # Download PDFs and DOCs to custom directory
  python main.py --url https://example.com/docs --extensions pdf,doc --output my-docs
        """
    )

    parser.add_argument(
        '--url',
        help='URL to scrape (use {page} placeholder for pagination)'
    )

    parser.add_argument(
        '--pages',
        help='Page range to scrape (e.g., "1-10" or "1,2,3,5")'
    )

    parser.add_argument(
        '--extensions', '-e',
        help='Comma-separated list of file extensions to download (e.g., pdf,doc,zip)',
        type=lambda x: set(ext.strip().lower() for ext in x.split(',')) if x else None
    )

    parser.add_argument(
        '--output', '-o',
        default='downloads',
        help='Output directory for downloaded files (default: downloads)'
    )

    parser.add_argument(
        '--yes', '-y',
        action='store_true',
        help='Skip confirmation prompt'
    )

    args = parser.parse_args()

    # Interactive mode if no URL provided
    if not args.url:
        try:
            interactive_mode()
        except KeyboardInterrupt:
            print("\n\nOperation cancelled by user")
            sys.exit(0)
    else:
        command_line_mode(args)


if __name__ == "__main__":
    main()
