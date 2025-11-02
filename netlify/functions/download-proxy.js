/**
 * Netlify Function: Download Proxy
 * Downloads files server-side to bypass CORS restrictions
 */

const axios = require('axios');

exports.handler = async (event, context) => {
  // CORS headers
  const headers = {
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Headers': 'Content-Type',
    'Access-Control-Allow-Methods': 'POST, OPTIONS',
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
        headers: { ...headers, 'Content-Type': 'application/json' },
        body: JSON.stringify({ error: 'URL is required' })
      };
    }

    // Download file with timeout (8 seconds to leave buffer for processing)
    const response = await axios.get(url, {
      responseType: 'arraybuffer',
      timeout: 8000,
      maxContentLength: 10 * 1024 * 1024, // 10MB max
      headers: {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
      }
    });

    // Get filename from URL or Content-Disposition header
    let filename = url.split('/').pop().split('?')[0];
    const contentDisposition = response.headers['content-disposition'];
    if (contentDisposition) {
      const filenameMatch = contentDisposition.match(/filename="?(.+)"?/i);
      if (filenameMatch) {
        filename = filenameMatch[1];
      }
    }

    // Return file as base64 (required for Netlify Functions)
    return {
      statusCode: 200,
      headers: {
        ...headers,
        'Content-Type': response.headers['content-type'] || 'application/octet-stream',
      },
      body: Buffer.from(response.data).toString('base64'),
      isBase64Encoded: true
    };

  } catch (error) {
    console.error('Download error:', error.message);

    let errorMessage = 'Failed to download file';
    let statusCode = 500;

    if (error.code === 'ECONNABORTED' || error.code === 'ETIMEDOUT') {
      errorMessage = 'Download timeout - file too large or slow server';
      statusCode = 504;
    } else if (error.response) {
      errorMessage = `HTTP ${error.response.status}: ${error.response.statusText}`;
      statusCode = error.response.status;
    }

    return {
      statusCode: statusCode,
      headers: { ...headers, 'Content-Type': 'application/json' },
      body: JSON.stringify({
        error: errorMessage,
        url: error.config?.url
      })
    };
  }
};
