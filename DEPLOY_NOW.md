# 🎯 DEPLOY NOW - Copy & Paste Ready

I've opened Render dashboard in your browser. Follow these exact steps:

---

## STEP 1: Login/Signup
- Click "**Sign up with GitHub**" (or Login if you have an account)
- Authorize Render to access your repositories

---

## STEP 2: Create Web Service
1. Click "**New +**" button (top right)
2. Select "**Web Service**"
3. In the repository list, find: **invoice-generator-api**
4. Click "**Connect**"

---

## STEP 3: Configure Service

**Copy these exact values:**

### Basic Settings:
- **Name**: `invoice-generator-api`
- **Region**: `Singapore` (or closest to you)
- **Branch**: `master`
- **Runtime**: `Python 3`

### Build & Start:
- **Build Command**: 
  ```
  pip install -r requirements.txt
  ```

- **Start Command**: 
  ```
  gunicorn run:app
  ```

- **Instance Type**: `Free`

---

## STEP 4: Environment Variables

Click "**Advanced**" (below Instance Type) → Scroll to "**Environment Variables**"

**Add these 6 variables** (Click "Add Environment Variable" for each):

### Variable 1:
- **Key**: `GEMINI_API_KEY`
- **Value**: `AIzaSyD9yxYwjCANE9MPgywYpAP6mst8RWdqIWo`

### Variable 2:
- **Key**: `BUSINESS_NAME`
- **Value**: `The pizza shop`

### Variable 3:
- **Key**: `BUSINESS_ADDRESS`
- **Value**: `iringalakuda`

### Variable 4:
- **Key**: `BUSINESS_PHONE`
- **Value**: `9265852`

### Variable 5:
- **Key**: `BUSINESS_EMAIL`
- **Value**: `info@yourbusiness.com`

### Variable 6:
- **Key**: `BUSINESS_GST`
- **Value**: `22AAAAA0000A1Z5`

---

## STEP 5: Deploy 🚀

1. Scroll down
2. Click "**Create Web Service**"
3. Wait 2-3 minutes for deployment

---

## STEP 6: Get Your URL

Once deployed (green checkmark):
1. You'll see your URL at the top: `https://invoice-generator-api.onrender.com`
2. Copy this URL
3. Test: `https://invoice-generator-api.onrender.com/api/health`

---

## TEST YOUR API

```bash
curl -X POST https://invoice-generator-api.onrender.com/api/generate-invoice \
  -H "Content-Type: application/json" \
  -d @sample_request.json \
  --output invoice.pdf
```

---

## ⚡ Quick Tips:

- ✅ Build takes 2-3 minutes
- ✅ Free tier includes 750 hours/month
- ⚠️ App sleeps after 15 min inactivity (30s wake time)
- 🔄 Auto-deploys on every GitHub push

---

**Your GitHub Repo**: https://github.com/Minhaj401/invoice-generator-api
**Render Dashboard**: https://dashboard.render.com/

---

🎉 **That's it!** Your API will be live in 3 minutes!
