# AQMusic Checker

A comprehensive monitoring solution for AQMusic domains with both CLI and web dashboard interfaces.

## Features

- **Real-time Domain Monitoring**: Check status of multiple domains simultaneously
- **Detailed Metrics**: Collects response time, HTTP status codes, SSL certificate info, geolocation, and more
- **Web Dashboard**: Beautiful, responsive web interface with auto-refresh (10-second intervals)
- **Discord Integration**: Automatic webhook notifications for status changes
- **SSL Certificate Tracking**: Monitors SSL certificate expiry dates and issuers
- **Geolocation Data**: Shows IP address location information
- **Responsive Design**: Works on desktop, tablet, and mobile devices

## Components

### 1. `ping.py` - CLI Monitoring Script

Runs continuously and sends status reports to Discord every 60 seconds.

**Features:**
- Monitors three AQMusic domains
- Sends detailed Discord webhook embeds with status information
- Retries on 502 Bad Gateway errors
- Tracks SSL certificate expiry
- Collects geolocation data for each IP
- Color-coded status indicators (green/yellow/red)

**Status Indicators:**
- 🟢 **Website On** (HTTP 200, fast response)
- 🟡 **Degraded** (HTTP 200, but response time > 800ms)
- 🔴 **Error** (HTTP errors, timeouts, connection failures)

**Configuration:**
Edit the following in `ping.py`:
- `WEBHOOK_URL`: Discord webhook for status reports
- `SITES`: List of domains to monitor
- `CHECK_INTERVAL_SECONDS`: How often to check (default: 60 seconds)
- `HIGH_PING_MS`: Threshold for degraded status (default: 800ms)

**Usage:**
```bash
python ping.py
```

### 2. `server.py` - Web Dashboard Server

Starts a Flask web server with a beautiful dashboard showing real-time status of all domains.

**Features:**
- Auto-refreshing every 10 seconds
- Quick status overview grid
- Detailed status cards for each domain
- Shows all metrics: response time, IP, SSL info, server headers, content type, etc.
- Responsive design with smooth animations
- RESTful API endpoint for programmatic access

**Endpoints:**
- `GET /` - Main dashboard HTML
- `GET /api/check` - API endpoint returning JSON status for all domains
- `GET /health` - Health check

**Usage:**
```bash
# Install dependencies
pip install flask requests

# Start the server
python server.py

# Open in browser
http://localhost:5000
```

**API Response Example:**
```json
{
  "timestamp": "2026-05-10T12:00:00+00:00",
  "sites": [
    {
      "url": "https://aqmusic.qzz.io",
      "pretty_domain": "aqmusic.qzz.io",
      "state": "Website On",
      "ping_ms": 245,
      "status_code": 200,
      "ip": "1.2.3.4",
      "country": "US",
      "city": "New York",
      "ssl_issuer": "Let's Encrypt",
      "ssl_expiry_days": 85,
      ...
    }
  ]
}
```

## Installation

### Requirements
- Python 3.7+
- Packages: `requests`, `flask`

### Setup

1. **Clone the repository**
   ```bash
   git clone <repo-url>
   cd Aqmusic.checker
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure Discord Webhook** (for ping.py)
   - Get your webhook URL from Discord
   - Update `WEBHOOK_URL` in `ping.py`

4. **Run the monitor**
   ```bash
   # For CLI monitoring with Discord notifications
   python ping.py
   
   # OR for web dashboard only
   python server.py
   ```

## Monitored Domains

- https://aqmusic.qzz.io
- https://dash.aqmusic.qzz.io
- https://app.aqmusic.qzz.io

## Collected Metrics

For each domain, the system collects:
- HTTP status code
- Response time (ping) in milliseconds
- Final redirect URL
- Server headers
- Content-Type
- Content-Length
- IP address
- Geolocation (country, city)
- SSL certificate issuer
- SSL certificate expiry (days remaining)

## Deployment Options

### 🌐 GitHub Pages (Recommended for Static Hosting)

Deploy your dashboard to GitHub Pages with custom domain support:

```bash
git push origin main
# Automatically deploys to GitHub Pages via workflow
```

**Features:**
- ✓ Free hosting on GitHub Pages
- ✓ Custom domain: `audioquackchecker.webap.cl`
- ✓ Automatic SSL/TLS certificate
- ✓ CDN for fast global access

**Setup Guide:** See [GITHUB_PAGES_SETUP.md](GITHUB_PAGES_SETUP.md)

**DNS Configuration:**
```
audioquackchecker.webap.cl  CNAME  luisdiko14-lab.github.io
```

### 🚀 Cloudflare Tunnel (Quick Testing)

Create instant public URL without DNS configuration:

```bash
# Install
brew install cloudflare/cloudflare/cloudflared

# Create tunnel
cloudflared tunnel --url http://localhost:5000
```

**Features:**
- ✓ No DNS setup needed
- ✓ Instant public URL (changes on restart)
- ✓ Free tier available
- ✓ Works with localhost

**Setup Guide:** See [CLOUDFLARE_TUNNEL.md](CLOUDFLARE_TUNNEL.md)

## Color Coding

- 🟢 **Green** - Website is online and responsive (< 800ms)
- 🟡 **Yellow** - Website is online but degraded (> 800ms response time)
- 🔴 **Red** - Website is down, error, or timeout

## Files

- `ping.py` - Discord webhook monitoring script
- `server.py` - Flask web server with dashboard
- `index.html` - Web dashboard frontend
- `README.md` - This file

## Deployment

### Option 1: Local Development
```bash
python server.py
# Access at http://localhost:5000
```

### Option 2: Production Server (using gunicorn)
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:8000 server:app
# Access at http://your-server:8000
```

### Option 3: Docker (optional)
Create a `Dockerfile`:
```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 5000
CMD ["python", "server.py"]
```

## License

[Add your license here]

## Support

For issues or questions, please create an issue in the repository.