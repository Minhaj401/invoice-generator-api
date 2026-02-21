# 🚀 Deploy to Render - Step by Step

Your code is already on GitHub! Follow these simple steps:

## Step 1: Go to Render
Visit: **https://render.com/**

## Step 2: Sign Up with GitHub
1. Click "**Get Started for Free**" or "**Sign Up**"
2. Choose "**Sign up with GitHub**"
3. Authorize Render to access your repositories

## Step 3: Create New Web Service
1. Click "**New +**" button (top right)
2. Select "**Web Service**"
3. Click "**Connect a repository**"
4. Find and select: **Minhaj401/invoice-generator-api**
5. Click "**Connect**"

## Step 4: Configure Your Service

Fill in these details:

- **Name**: `invoice-generator-api` (or any name you like)
- **Region**: Choose closest to you (e.g., Singapore, Frankfurt)
- **Branch**: `master`
- **Runtime**: `Python 3`
- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `gunicorn run:app`
- **Instance Type**: `Free` (or upgrade if needed)

## Step 5: Add Environment Variables

Click "**Advanced**" → Scroll to "**Environment Variables**"

Add these variables one by one:

```
GEMINI_API_KEY=AIzaSyD9yxYwjCANE9MPgywYpAP6mst8RWdqIWo
BUSINESS_NAME=The pizza shop
BUSINESS_ADDRESS=iringalakuda
BUSINESS_PHONE=9265852
BUSINESS_EMAIL=info@yourbusiness.com
BUSINESS_GST=22AAAAA0000A1Z5
```

**How to add:**
1. Click "**Add Environment Variable**"
2. Enter Key (e.g., `GEMINI_API_KEY`)
3. Enter Value
4. Repeat for all variables

## Step 6: Deploy!

1. Click "**Create Web Service**" button
2. Wait 2-3 minutes for deployment
3. Your app will be live at: `https://invoice-generator-api.onrender.com`

## Step 7: Test Your API

Once deployed, test it:

```bash
curl -X POST https://invoice-generator-api.onrender.com/api/generate-invoice \
  -H "Content-Type: application/json" \
  -d @sample_request.json \
  --output invoice.pdf
```

Or visit in browser:
```
https://invoice-generator-api.onrender.com
```

## 🎉 Done!

Your API is now live and accessible from anywhere!

---

## Important Notes:

✅ **Free Tier**: Render free tier includes 750 hours/month
⚠️ **Cold Starts**: Free tier apps sleep after 15 mins of inactivity (takes ~30s to wake up)
🔄 **Auto Deploy**: Any push to GitHub master branch will automatically redeploy
🌐 **Custom Domain**: You can add your own domain in settings

## Troubleshooting

### Build Failed?
- Check the logs in Render dashboard
- Verify `requirements.txt` is correct
- Make sure Python version is compatible

### Service Not Starting?
- Check environment variables are set correctly
- Verify the start command: `gunicorn run:app`
- Look at the deployment logs

### 404 Error?
- Make sure you're accessing the correct URL
- Try: `https://your-app-name.onrender.com/api/health`

---

**Your GitHub Repo**: https://github.com/Minhaj401/invoice-generator-api
**Render Dashboard**: https://dashboard.render.com/
