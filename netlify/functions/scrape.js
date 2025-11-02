/**
 * Netlify Function: Scrape links from a webpage (JavaScript version)
 * JavaScript functions are natively supported by Netlify
 */

const axios = require('axios');
const cheerio = require('cheerio');

// Common downloadable file extensions
const DOWNLOADABLE_EXTENSIONS = new Set([
  'pdf', 'doc', 'docx', 'xls', 'xlsx', 'ppt', 'pptx',
  'zip', 'rar', '7z', 'tar', 'gz',
  'txt', 'csv', 'json', 'xml',
  'jpg', 'jpeg', 'png', 'gif', 'svg',
  'mp3', 'mp4', 'avi', 'mov', 'wmv',
]);

function getExtension(url) {
  try {
    const urlObj = new URL(url);
    const path = urlObj.pathname.split('?')[0].split('#')[0];
    if (path.includes('.')) {
      return path.split('.').pop().toLowerCase();
    }
  } catch (e) {
    // Invalid URL
  }
  return '';
}

function normalizeUrl(base, href) {
  try {
    return new URL(href, base).href;
  } catch (e) {
    return null;
  }
}

async function scrapePage(url, filterExtensions = null) {
  try {
    const response = await axios.get(url, {
      timeout: 8000,
      headers: {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
      },
      maxRedirects: 5
    });

    const $ = cheerio.load(response.data);
    const links = [];
    const seenUrls = new Set();

    $('a[href]').each((i, elem) => {
      const href = $(elem).attr('href');
      const linkText = $(elem).text().trim() || 'No description';
      const fullUrl = normalizeUrl(url, href);

      if (!fullUrl) return;

      const extension = getExtension(fullUrl);

      // Filter by extension if specified
      if (filterExtensions && !filterExtensions.has(extension)) {
        return;
      }

      // Only include downloadable files
      if (!DOWNLOADABLE_EXTENSIONS.has(extension)) {
        return;
      }

      // Avoid duplicates
      if (seenUrls.has(fullUrl)) {
        return;
      }

      seenUrls.add(fullUrl);
      links.push({
        url: fullUrl,
        text: linkText.substring(0, 100),
        extension: extension
      });
    });

    return links;

  } catch (error) {
    throw new Error(`Error scraping ${url}: ${error.message}`);
  }
}

function parsePageRange(pageRange) {
  try {
    const pages = [];
    const parts = pageRange.split(',');

    for (const part of parts) {
      const trimmed = part.trim();
      if (trimmed.includes('-')) {
        const [start, end] = trimmed.split('-').map(n => parseInt(n));
        // Limit to 10 pages max for timeout
        const actualEnd = Math.min(end, start + 9);
        for (let i = start; i <= actualEnd; i++) {
          pages.push(i);
        }
      } else {
        pages.push(parseInt(trimmed));
      }
    }

    return [...new Set(pages)].sort((a, b) => a - b).slice(0, 10);
  } catch (e) {
    return [1];
  }
}

exports.handler = async (event, context) => {
  // CORS headers
  const headers = {
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Headers': 'Content-Type',
    'Access-Control-Allow-Methods': 'POST, OPTIONS',
    'Content-Type': 'application/json'
  };

  // Handle OPTIONS request for CORS
  if (event.httpMethod === 'OPTIONS') {
    return {
      statusCode: 200,
      headers,
      body: ''
    };
  }

  try {
    // Parse request body
    const body = JSON.parse(event.body || '{}');

    const url = body.url;
    if (!url) {
      return {
        statusCode: 400,
        headers,
        body: JSON.stringify({ error: 'URL is required' })
      };
    }

    const paginationMode = body.pagination_mode || 'single';
    const extensions = body.extensions || [];
    const extensionsSet = extensions.length > 0
      ? new Set(extensions.map(ext => ext.toLowerCase().replace('.', '')))
      : null;

    let links = [];

    if (paginationMode === 'single') {
      links = await scrapePage(url, extensionsSet);

    } else if (paginationMode === 'manual') {
      const pattern = body.url_pattern || url;
      const pageRange = body.page_range || '1';
      const pageNumbers = parsePageRange(pageRange);

      for (const pageNum of pageNumbers) {
        const pageUrl = pattern.replace('{page}', pageNum.toString());
        try {
          const pageLinks = await scrapePage(pageUrl, extensionsSet);
          links.push(...pageLinks);
        } catch (e) {
          // Continue on error
          console.error(`Error scraping page ${pageNum}:`, e.message);
        }
      }
    }

    // Remove duplicates
    const seen = new Set();
    const uniqueLinks = [];
    for (const link of links) {
      if (!seen.has(link.url)) {
        seen.add(link.url);
        uniqueLinks.push(link);
      }
    }

    // Get statistics
    const stats = {};
    for (const link of uniqueLinks) {
      const ext = link.extension;
      stats[ext] = (stats[ext] || 0) + 1;
    }

    return {
      statusCode: 200,
      headers,
      body: JSON.stringify({
        success: true,
        links: uniqueLinks,
        count: uniqueLinks.length,
        statistics: stats
      })
    };

  } catch (error) {
    console.error('Function error:', error);
    return {
      statusCode: 500,
      headers,
      body: JSON.stringify({
        error: error.message || 'Internal server error'
      })
    };
  }
};
