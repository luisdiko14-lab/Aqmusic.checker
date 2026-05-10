"""
Flask server for AQMusic Checker - Web interface for domain status monitoring
"""
from flask import Flask, render_template_string, jsonify
import time
import requests
from datetime import datetime, timezone
import socket
import urllib.parse
import ssl
import threading
import os

app = Flask(__name__)

SITES = [
    "https://aqmusic.qzz.io",
    "https://dash.aqmusic.qzz.io",
    "https://app.aqmusic.qzz.io",
]

HIGH_PING_MS = 800
VERY_HIGH_PING_MS = 1500

def pretty_domain(url: str) -> str:
    return (
        url.replace("https://", "")
           .replace("http://", "")
           .replace("www.", "")
           .rstrip("/")
    )

def get_ssl_info(domain: str):
    try:
        context = ssl.create_default_context()
        with socket.create_connection((domain, 443), timeout=5) as sock:
            with context.wrap_socket(sock, server_hostname=domain) as ssock:
                cert = ssock.getpeercert()
                expiry = datetime.strptime(cert['notAfter'], '%b %d %H:%M:%S %Y %Z')
                days_left = (expiry - datetime.now()).days
                issuer = dict(x[0] for x in cert['issuer'])['organizationName']
                return {"expiry_days": days_left, "issuer": issuer}
    except:
        return {"expiry_days": None, "issuer": "Unknown"}

def status_info(url: str):
    domain = urllib.parse.urlparse(url).netloc
    try:
        ip = socket.gethostbyname(domain)
    except socket.gaierror:
        ip = "Unknown"

    country = "Unknown"
    city = "Unknown"
    if ip != "Unknown":
        try:
            geo = requests.get(f"https://ipapi.co/{ip}/json/", timeout=5).json()
            country = geo.get("country_name", "Unknown")
            city = geo.get("city", "Unknown")
        except:
            pass

    ssl_info = get_ssl_info(domain)

    start = time.perf_counter()
    try:
        r = requests.get(url, timeout=15, allow_redirects=True)
        elapsed_ms = round((time.perf_counter() - start) * 1000)

        # Retry once for 502 Bad Gateway
        if r.status_code == 502:
            time.sleep(2)
            start = time.perf_counter()
            r = requests.get(url, timeout=15, allow_redirects=True)
            elapsed_ms = round((time.perf_counter() - start) * 1000)

        if r.status_code == 200:
            if elapsed_ms >= HIGH_PING_MS:
                state = "Degraded"
                color = 0xFACC15
            else:
                state = "Website On"
                color = 0x22C55E

        elif r.status_code == 404:
            state = "Not Found"
            color = 0xEF4444
        elif r.status_code == 502:
            state = "Website On"
            color = 0x22C55E
        elif r.status_code == 503:
            state = "Service Unavailable"
            color = 0xEF4444
        elif 500 <= r.status_code <= 599:
            state = "Server Error"
            color = 0xEF4444
        elif 300 <= r.status_code <= 399:
            state = "Redirecting"
            color = 0xFACC15
        else:
            state = "Problem detected"
            color = 0xEF4444

        return {
            "url": url,
            "pretty_domain": pretty_domain(url),
            "ok": r.status_code == 200,
            "state": state,
            "color": color,
            "status_code": r.status_code,
            "ping_ms": elapsed_ms,
            "final_url": r.url,
            "server": r.headers.get("server", "Unknown"),
            "content_type": r.headers.get("content-type", "Unknown"),
            "content_length": r.headers.get("content-length", "Unknown"),
            "ip": ip,
            "country": country,
            "city": city,
            "ssl_expiry_days": ssl_info["expiry_days"],
            "ssl_issuer": ssl_info["issuer"],
            "error": None,
        }

    except requests.Timeout:
        return {
            "url": url,
            "pretty_domain": pretty_domain(url),
            "ok": False,
            "state": "Timeout",
            "color": 0xEF4444,
            "status_code": "Timeout",
            "ping_ms": None,
            "final_url": url,
            "server": "Unknown",
            "content_type": "Unknown",
            "content_length": "Unknown",
            "ip": ip,
            "country": country,
            "city": city,
            "ssl_expiry_days": ssl_info["expiry_days"],
            "ssl_issuer": ssl_info["issuer"],
            "error": None,
        }
    except requests.RequestException as e:
        return {
            "url": url,
            "pretty_domain": pretty_domain(url),
            "ok": False,
            "state": f"Request failed",
            "color": 0xEF4444,
            "status_code": "Error",
            "ping_ms": None,
            "final_url": url,
            "server": "Unknown",
            "content_type": "Unknown",
            "content_length": "Unknown",
            "error": str(e),
            "ip": ip,
            "country": country,
            "city": city,
            "ssl_expiry_days": ssl_info["expiry_days"],
            "ssl_issuer": ssl_info["issuer"],
        }

@app.route('/')
def index():
    """Serve the main HTML dashboard"""
    try:
        with open(os.path.join(os.path.dirname(__file__), 'index.html'), 'r') as f:
            html_content = f.read()
        return html_content
    except:
        return "index.html not found", 404

@app.route('/api/check')
def api_check():
    """API endpoint to check all sites and return status"""
    results = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "sites": []
    }
    
    for site in SITES:
        try:
            info = status_info(site)
            results["sites"].append(info)
        except Exception as e:
            results["sites"].append({
                "url": site,
                "pretty_domain": pretty_domain(site),
                "ok": False,
                "state": "Error",
                "color": 0xEF4444,
                "status_code": "Error",
                "ping_ms": None,
                "final_url": site,
                "server": "Unknown",
                "content_type": "Unknown",
                "content_length": "Unknown",
                "ip": "Unknown",
                "country": "Unknown",
                "city": "Unknown",
                "ssl_expiry_days": None,
                "ssl_issuer": "Unknown",
                "error": str(e),
            })
    
    return jsonify(results)

@app.route('/health')
def health():
    """Health check endpoint"""
    return jsonify({"status": "ok"}), 200

if __name__ == '__main__':
    print("Starting AQMusic Checker Web Server...")
    print("Open http://localhost:5000 in your browser")
    app.run(debug=False, host='0.0.0.0', port=5000, threaded=True)
