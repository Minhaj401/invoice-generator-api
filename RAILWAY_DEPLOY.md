# Railway Deployment Guide

## Quick Deploy to Railway

Your code is now on GitHub! Here's how to deploy to Railway:

### Step 1: Go to Railway
Visit: **https://railway.app/**

### Step 2: Sign Up/Login
- Click "Login" and sign in with your GitHub account
- Authorize Railway to access your repositories

### Step 3: Create New Project
1. Click "**New Project**"
2. Select "**Deploy from GitHub repo**"
3. Choose: **Minhaj401/invoice-generator-api**

### Step 4: Configure Environment Variables
Railway will automatically detect your Python app. Add these environment variables:

```
GEMINI_API_KEY=your_actual_gemini_api_key_here
BUSINESS_NAME=Your Business Name
BUSINESS_ADDRESS=Your Business Address
BUSINESS_PHONE=+91-1234567890
BUSINESS_EMAIL=your@business.com
BUSINESS_GST=YOUR_GST_NUMBER
```

**To add variables:**
1. Go to your project
2. Click on the service (invoice-generator-api)
3. Click "**Variables**" tab
4. Click "**+ New Variable**"
5. Add each variable one by one

### Step 5: Deploy
- Railway will automatically build and deploy your app
- Wait for the build to complete (2-3 minutes)
- Once deployed, you'll get a public URL

### Step 6: Get Your Public URL
1. Click on "**Settings**" tab
2. Scroll to "**Networking**"
3. Click "**Generate Domain**"
4. Copy your public URL (e.g., `https://invoice-generator-api-production.up.railway.app`)

### Step 7: Test Your API
```bash
curl -X POST https://your-railway-url.up.railway.app/api/generate-invoice \
  -H "Content-Type: application/json" \
  -d @sample_request.json \
  --output invoice.pdf
```

## Important Notes

✅ **Free Tier**: Railway offers $5 free credit per month
✅ **Auto Deploy**: Any push to GitHub will automatically redeploy
✅ **Environment Variables**: Required for API to work
✅ **Build Time**: First deploy takes 2-3 minutes

## Troubleshooting

### Build Failed?
- Check the build logs in Railway dashboard
- Ensure all dependencies in `requirements.txt` are correct

### App Crashed?
- Check environment variables are set correctly
- Look at deployment logs for error messages
- Ensure `GEMINI_API_KEY` is valid

### Can't Access API?
- Make sure you generated a domain in Settings > Networking
- Check if service is running (green status)

## Your GitHub Repository
🔗 https://github.com/Minhaj401/invoice-generator-api

## Railway Dashboard
🔗 https://railway.app/dashboard

---

**Need Help?** Check the full DEPLOYMENT.md for other platform options!
