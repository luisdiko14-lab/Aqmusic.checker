# GitHub Pages & Custom Domain Setup

Complete guide to deploy AQMusic Checker to GitHub Pages with your custom domain `audioquackchecker.webap.cl`

## Quick Start (5 minutes)

### Step 1: Enable GitHub Pages in Repository Settings

1. Go to your repository: `https://github.com/luisdiko14-lab/Aqmusic.checker`
2. Click **Settings** → **Pages**
3. Under "Build and deployment":
   - Source: Select **"Deploy from a branch"**
   - Branch: Select **`gh-pages`** 
   - Folder: Select **`/ (root)`**
4. Click **Save**

### Step 2: Configure Custom Domain

1. Still in **Settings** → **Pages**
2. Under "Custom domain" section:
   - Enter: `audioquackchecker.webap.cl`
   - Click **Save**
3. ✓ GitHub will create a **CNAME file** automatically

### Step 3: Configure DNS at Domain Registrar

Update your DNS records at your domain registrar (where you registered webap.cl):

#### Add/Update CNAME Record:
```
subdomain: audioquackchecker
type: CNAME
value: luisdiko14-lab.github.io
TTL: 3600 (or default)
```

#### Expected DNS configuration:
```
audioquackchecker.webap.cl  CNAME  luisdiko14-lab.github.io
```

### Step 4: Wait for DNS Propagation

DNS changes take 5-48 hours to fully propagate. You can check status:

```bash
# Check CNAME resolution
nslookup audioquackchecker.webap.cl

# Or use dig
dig audioquackchecker.webap.cl

# Watch for resolution to GitHub's IP
# Expected: luisdiko14-lab.github.io → GitHub Pages IP
```

### Step 5: Deploy

Push code to trigger the workflow:

```bash
git push origin main
```

Or manually trigger:
1. Go to **Actions** tab
2. Click **"Deploy to GitHub Pages"** workflow
3. Click **"Run workflow"** button

### Step 6: Access Your Dashboard

Once DNS propagates, visit:
```
https://audioquackchecker.webap.cl
```

✓ Your AQMusic Checker is live!

---

## Configure Backend API

### Option A: Flask Server on Same VPS

If running on a VPS with your domain:

1. **Update Flask to use same domain:**
   ```python
   # In server.py
   FRONTEND_URL = "https://audioquackchecker.webap.cl"
   ```

2. **Use Nginx as reverse proxy:**
   ```nginx
   server {
       server_name audioquackchecker.webap.cl;
       
       location /api/ {
           proxy_pass http://localhost:5000;
       }
       
       location / {
           # Serve static files or forward to GitHub Pages
       }
   }
   ```

### Option B: Separate Backend Service

If your Flask backend runs elsewhere (e.g., Heroku, Railway, AWS):

1. **Update API endpoint in dashboard:**
   ```javascript
   // In index.html
   const API_URL = 'https://your-backend-api.com/api/check';
   ```

2. **Ensure CORS is enabled:**
   Flask server already has CORS enabled:
   ```python
   from flask_cors import CORS
   CORS(app, resources={r"/api/*": {"origins": "*"}})
   ```

### Option C: GitHub Actions Auto-Deploy

Deploy both frontend and backend:

1. **Frontend:** GitHub Pages (static HTML)
2. **Backend:** Choose platform:
   - Heroku (free tier deprecated, use Railway)
   - Railway.app
   - Render.com
   - DigitalOcean App Platform

---

## Troubleshooting

### DNS Not Resolving

```bash
# Flush your DNS cache
# macOS
sudo dscacheutil -flushcache

# Windows
ipconfig /flushdns

# Linux
sudo systemd-resolve --flush-caches
```

### GitHub Pages Not Updating

1. Check **Actions** tab for failed workflows
2. Verify branch is set to `gh-pages` in **Settings → Pages**
3. Clear browser cache: `Ctrl+Shift+R` or `Cmd+Shift+R`

### CNAME File Issues

1. Delete CNAME from custom domain settings
2. Wait 1 minute
3. Re-add custom domain
4. GitHub will recreate CNAME file

### API Returns 404

1. Ensure Flask backend is accessible
2. Check CORS headers:
   ```bash
   curl -I https://your-backend-api.com/api/check
   ```
3. Verify `Content-Type: application/json` is returned

### SSL Certificate Issues

GitHub Pages automatically provides SSL certificate via Let's Encrypt. If you see certificate warnings:

1. Wait 24 hours after adding custom domain
2. Clear browser SSL cache
3. Try in incognito/private mode

---

## DNS Setup Examples

### GoDaddy
1. Go to DNS Management
2. Add CNAME record:
   - Name: `audioquackchecker`
   - Type: `CNAME`
   - Value: `luisdiko14-lab.github.io`

### Namecheap
1. Go to DNS Records
2. Add new record:
   - Type: `CNAME Record`
   - Host: `audioquackchecker`
   - Value: `luisdiko14-lab.github.io`

### Route53 (AWS)
```json
{
  "Name": "audioquackchecker.webap.cl",
  "Type": "CNAME",
  "TTL": 300,
  "ResourceRecords": [
    {
      "Value": "luisdiko14-lab.github.io"
    }
  ]
}
```

---

## Monitoring Emails

GitHub Pages sends notification emails to:
- **your-email@github.com** (GitHub account email)

Check these events:
- ✓ Pages build and deployment succeeded
- ✗ Pages build and deployment failed
- SSL/TLS certificate issued/renewed

---

## Performance Tips

### Enable Caching Headers

Add to `.github/workflows/pages.yml`:

```yaml
- name: Set up caching headers
  run: |
    cat > docs/_headers << 'EOF'
    /*
      X-Frame-Options: DENY
      X-Content-Type-Options: nosniff
      X-XSS-Protection: 1; mode=block
      Cache-Control: public, max-age=3600
    EOF
```

### Optimize Images

```bash
# Update workflow to compress images
- name: Optimize images
  run: |
    npm install -g imagemin-cli imagemin-mozjpeg imagemin-pngquant
    imagemin docs --out-dir=docs
```

---

## Custom Domain via GitHub Pages vs Cloudflare Tunnel

| Feature | GitHub Pages | Cloudflare Tunnel |
|---------|---|---|
| Setup Time | 5-10 minutes | 2-3 minutes |
| Cost | Free | Free |
| Custom Domain | ✓ (requires DNS setup) | ✓ (subdomain) |
| SSL Certificate | ✓ (automatic) | ✓ (automatic) |
| Persistence | ✓ (permanent) | ✗ (URL changes on restart) |
| Backend API | Requires separate service | Works with localhost:5000 |
| Performance | Fast (CDN) | Variable (tunneling) |

---

## Next Steps

1. ✓ Enable GitHub Pages
2. ✓ Add custom domain
3. ✓ Configure DNS with your registrar
4. ✓ Deploy Flask backend (separate service)
5. ✓ Wait for DNS propagation
6. ✓ Access at https://audioquackchecker.webap.cl

**Questions?** Check [GitHub Pages Docs](https://docs.github.com/en/pages)
