# 🚀 Deployment Guide

This guide covers multiple deployment options for the Invoice Generator API.

## Quick Deployment Options

### 1. Render.com (Recommended - Free Tier)

**Step 1:** Push code to GitHub
```bash
git init
git add .
git commit -m "Initial commit"
git remote add origin YOUR_GITHUB_REPO_URL
git push -u origin main
```

**Step 2:** Deploy on Render
1. Go to [render.com](https://render.com) and sign up
2. Click "New +" → "Web Service"
3. Connect your GitHub repository
4. Render will auto-detect `render.yaml`
5. Add environment variables in Render dashboard:
   - `GEMINI_API_KEY`
   - `BUSINESS_NAME`
   - `BUSINESS_ADDRESS`
   - `BUSINESS_PHONE`
   - `BUSINESS_EMAIL`
   - `BUSINESS_GST`
6. Click "Create Web Service"

**Your API will be live at:** `https://your-app-name.onrender.com`

---

### 2. Railway.app (Easy & Fast)

**Step 1:** Install Railway CLI
```bash
npm i -g @railway/cli
```

**Step 2:** Deploy
```bash
railway login
railway init
railway up
```

**Step 3:** Set environment variables
```bash
railway variables set GEMINI_API_KEY=your_key
railway variables set BUSINESS_NAME="Your Business Name"
railway variables set BUSINESS_ADDRESS="Your Address"
railway variables set BUSINESS_PHONE="Your Phone"
railway variables set BUSINESS_EMAIL="your@email.com"
railway variables set BUSINESS_GST="Your GST Number"
```

---

### 3. Heroku

**Step 1:** Install Heroku CLI
Download from: https://devcenter.heroku.com/articles/heroku-cli

**Step 2:** Deploy
```bash
heroku login
heroku create your-invoice-api
git push heroku main
```

**Step 3:** Set environment variables
```bash
heroku config:set GEMINI_API_KEY=your_api_key
heroku config:set BUSINESS_NAME="Your Business Name"
heroku config:set BUSINESS_ADDRESS="Your Address"
heroku config:set BUSINESS_PHONE="Your Phone"
heroku config:set BUSINESS_EMAIL="your@email.com"
heroku config:set BUSINESS_GST="Your GST Number"
```

---

### 4. Docker Deployment

**Build and run locally:**
```bash
docker build -t invoice-generator .
docker run -p 5000:5000 --env-file .env invoice-generator
```

**Using Docker Compose:**
```bash
docker-compose up -d
```

**Deploy to any Docker hosting:**
- Google Cloud Run
- AWS ECS/Fargate
- Azure Container Instances
- DigitalOcean App Platform

---

### 5. PythonAnywhere (Free Hosting)

**Step 1:** Create account at [pythonanywhere.com](https://www.pythonanywhere.com)

**Step 2:** Upload files via dashboard or Git

**Step 3:** Configure Web App
1. Go to "Web" tab
2. Click "Add a new web app"
3. Choose Flask
4. Set working directory: `/home/yourusername/makeaton`
5. Edit WSGI configuration file:

```python
import sys
import os

# Add your project directory
project_home = '/home/yourusername/makeaton'
if project_home not in sys.path:
    sys.path.insert(0, project_home)

# Load environment variables
from dotenv import load_dotenv
load_dotenv(os.path.join(project_home, '.env'))

# Import Flask app
from run import app as application
```

**Step 4:** Install packages in Bash console:
```bash
cd makeaton
pip3 install --user -r requirements.txt
```

---

## Cloud Platform Deployment

### AWS EC2

1. Launch an EC2 instance (Ubuntu)
2. SSH into instance
3. Install Python and dependencies:
```bash
sudo apt update
sudo apt install python3-pip python3-venv
```

4. Clone/upload your project
5. Setup:
```bash
cd makeaton
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

6. Run with gunicorn:
```bash
gunicorn --bind 0.0.0.0:5000 run:app
```

7. Use Nginx as reverse proxy and systemd for process management

---

### Google Cloud Run (Serverless)

```bash
# Install gcloud CLI
gcloud init

# Build and deploy
gcloud run deploy invoice-generator \
  --source . \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --set-env-vars GEMINI_API_KEY=your_key,BUSINESS_NAME="Your Name"
```

---

### Vercel (Serverless)

1. Install Vercel CLI:
```bash
npm i -g vercel
```

2. Create `vercel.json`:
```json
{
  "builds": [
    {
      "src": "run.py",
      "use": "@vercel/python"
    }
  ],
  "routes": [
    {
      "src": "/(.*)",
      "dest": "run.py"
    }
  ]
}
```

3. Deploy:
```bash
vercel --prod
```

---

## Environment Variables Required

All deployments need these environment variables:

```env
GEMINI_API_KEY=your_gemini_api_key
BUSINESS_NAME=Your Business Name
BUSINESS_ADDRESS=Your Business Address
BUSINESS_PHONE=Your Phone Number
BUSINESS_EMAIL=your@email.com
BUSINESS_GST=Your GST Number
```

---

## Post-Deployment

### Test Your Deployment

```bash
# Health check
curl https://your-domain.com/api/health

# Generate invoice
curl -X POST https://your-domain.com/api/generate-invoice \
  -H "Content-Type: application/json" \
  -d @sample_request.json \
  --output invoice.pdf
```

### Monitor Your App

- **Render:** Built-in logs and metrics
- **Railway:** Real-time logs in dashboard
- **Heroku:** `heroku logs --tail`
- **Docker:** `docker logs container_name`

---

## Production Considerations

### Security
- Never commit `.env` file (already in `.gitignore`)
- Use environment variables for all secrets
- Enable HTTPS (most platforms do this automatically)
- Add rate limiting if needed

### Performance
- Gunicorn workers: `--workers 2-4` (adjust based on traffic)
- Set appropriate timeouts: `--timeout 60`
- Use Redis for caching if scaling

### Monitoring
- Set up error tracking (Sentry, Rollbar)
- Monitor API usage
- Track Gemini API quota

---

## Cost Comparison

| Platform | Free Tier | Notes |
|----------|-----------|-------|
| **Render** | ✅ 750 hrs/month | Sleeps after 15 min inactivity |
| **Railway** | ✅ $5 credit/month | No sleep, faster |
| **Heroku** | ✅ 550 hrs/month | Requires credit card |
| **PythonAnywhere** | ✅ Limited | Good for small traffic |
| **Vercel** | ✅ Generous | Serverless, auto-scaling |
| **Google Cloud Run** | ✅ 2M requests/month | Pay per use |

---

## Recommended Choice

**For beginners:** Render.com (easiest setup)
**For speed:** Railway.app
**For scale:** Google Cloud Run or AWS
**For control:** Docker on any VPS

Choose based on your needs and technical comfort level!
