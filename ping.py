import time
import requests
from datetime import datetime, timezone

WEBHOOK_URL = "PUT_YOUR_DISCORD_WEBHOOK_URL_HERE"

SITES = [
    "https://aqmusic.qzz.io",
    "https://dash.aqmusic.qzz.io"
]

CHECK_INTERVAL_SECONDS = 300   # 5 minutes
HIGH_PING_MS = 800             # yellow if above this
VERY_HIGH_PING_MS = 1500       # orange if above this

def pretty_domain(url: str) -> str:
    return (
        url.replace("https://", "")
           .replace("http://", "")
           .replace("www.", "")
           .rstrip("/")
    )

def status_info(url: str):
    start = time.perf_counter()
    try:
        r = requests.get(url, timeout=15, allow_redirects=True)
        elapsed_ms = round((time.perf_counter() - start) * 1000)

        if r.status_code == 200:
            if elapsed_ms >= VERY_HIGH_PING_MS:
                state = "Degraded"
                color = 0xF59E0B  # orange
            elif elapsed_ms >= HIGH_PING_MS:
                state = "Degraded"
                color = 0xFACC15  # yellow
            else:
                state = "Website On"
                color = 0x22C55E  # green

        elif r.status_code == 404:
            state = "Domain not working"
            color = 0xEF4444  # red
        elif 500 <= r.status_code <= 599:
            state = "Server error"
            color = 0xEF4444
        elif 300 <= r.status_code <= 399:
            state = "Redirecting"
            color = 0x38BDF8  # blue
        else:
            state = "Problem detected"
            color = 0xEF4444

        return {
            "ok": r.status_code == 200,
            "state": state,
            "color": color,
            "status_code": r.status_code,
            "ping_ms": elapsed_ms,
            "final_url": r.url,
            "server": r.headers.get("server", "Unknown"),
            "content_type": r.headers.get("content-type", "Unknown"),
            "content_length": r.headers.get("content-length", "Unknown"),
        }

    except requests.Timeout:
        return {
            "ok": False,
            "state": "Timeout",
            "color": 0xEF4444,
            "status_code": "Timeout",
            "ping_ms": None,
            "final_url": url,
            "server": "Unknown",
            "content_type": "Unknown",
            "content_length": "Unknown",
        }
    except requests.RequestException as e:
        return {
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
        }

def send_webhook_embed(site_url: str, info: dict):
    site_name = pretty_domain(site_url)
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")

    description = (
        f"**Status:** {info['state']}\n"
        f"**Ping:** {info['ping_ms']} ms\n" if info["ping_ms"] is not None else f"**Status:** {info['state']}\n"
    )

    fields = [
        {"name": "Domain", "value": site_name, "inline": True},
        {"name": "HTTP Code", "value": str(info["status_code"]), "inline": True},
        {"name": "Final URL", "value": info["final_url"], "inline": False},
        {"name": "Server", "value": str(info.get("server", "Unknown")), "inline": True},
        {"name": "Content Type", "value": str(info.get("content_type", "Unknown")), "inline": True},
        {"name": "Content Length", "value": str(info.get("content_length", "Unknown")), "inline": True},
        {"name": "Checked At", "value": now, "inline": False},
    ]

    if "error" in info:
        fields.append({"name": "Error", "value": info["error"][:1000], "inline": False})

    payload = {
        "username": "Website Monitor",
        "embeds": [
            {
                "title": f"{site_name} status report",
                "description": description,
                "color": info["color"],
                "fields": fields,
                "footer": {"text": "Website stats monitor"},
            }
        ]
    }

    requests.post(WEBHOOK_URL, json=payload, timeout=15)

def check_all_sites():
    for site in SITES:
        info = status_info(site)
        send_webhook_embed(site, info)

def main():
    print("Starting website monitor...")
    while True:
        check_all_sites()
        time.sleep(CHECK_INTERVAL_SECONDS)

if __name__ == "__main__":
    main()
