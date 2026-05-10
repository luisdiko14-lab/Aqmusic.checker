# Cloudflare Tunnel Setup Guide

This guide explains how to run AQMusic Checker with Cloudflare Tunnel (trycloudflare) for public access.

## Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Install Cloudflared
- **macOS**: `brew install cloudflare/cloudflare/cloudflared`
- **Linux**: Download from https://github.com/cloudflare/cloudflared/releases
- **Windows**: Download from https://github.com/cloudflare/cloudflare/releases

### 3. Start Flask Server
```bash
python server.py
```

The server will start on `http://localhost:5000`

### 4. Create Tunnel (in another terminal)
```bash
cloudflared tunnel --url http://localhost:5000
```

This will output a unique URL like: `https://cute-animal-123.trycloudflare.com`

### 5. Access Your Dashboard
Open the tunnel URL in your browser. Your AQMusic Checker is now publicly accessible!

## Features

- ✓ Real-time domain status monitoring
- ✓ SSL certificate expiry tracking
- ✓ Geolocation information for servers
- ✓ Response time monitoring
- ✓ Automatic refresh every 10 seconds
- ✓ Quick status indicator
- ✓ Fully self-contained HTML/CSS/JS

## API Endpoints

### GET `/`
Returns the main dashboard HTML page.

### GET `/api/check`
Returns JSON data with status for all monitored domains:
```json
{
  "timestamp": "2024-01-01T12:00:00.000000+00:00",
  "sites": [
    {
      "pretty_domain": "aqmusic.qzz.io",
      "state": "Website On",
      "status_code": 200,
      "ping_ms": 245,
      "ssl_expiry_days": 365,
      "country": "US",
      "city": "New York"
    }
  ]
}
```

### GET `/health`
Simple health check endpoint.

## Monitored Sites

- https://aqmusic.qzz.io
- https://dash.aqmusic.qzz.io
- https://app.aqmusic.qzz.io

## Production Deployment

For production, you can:

1. **Use GitHub Actions** - Automatically deploys on push
2. **Use Docker** - Containerize your Flask app
3. **Use persistent tunnel** - Set up authentication and a custom domain
4. **Use Page Rule** - Set up caching and other optimizations

## Troubleshooting

### "Failed to fetch status: 404"
- Ensure Flask server is running on port 5000
- Check that `/api/check` endpoint is accessible
- Verify CORS is not blocking requests

### Tunnel URL expires
- Free tunnels change on restart
- For persistent URL, use `cloudflared tunnel create myname`

### Slow response times
- Check server logs: `python server.py` (verbose mode)
- Monitor geolocation API: ipapi.co
- Verify DNS resolution isn't slow

## Notes

- Free trycloudflare tunnels are temporary
- For production, register a domain and configure DNS
- The HTML file is fully self-contained (no external dependencies)
