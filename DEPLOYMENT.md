# Deploying to Render.com

This guide will help you deploy the Pothole Detection System to Render.com for free.

## Prerequisites

- GitHub account with your code pushed
- Render.com account (free tier)

## Deployment Steps

### 1. Sign Up for Render

1. Go to [Render.com](https://render.com)
2. Click "Get Started" or "Sign Up"
3. Sign up with your GitHub account (recommended)

### 2. Create New Web Service

1. Click "New +" button in Render dashboard
2. Select "Web Service"
3. Connect your GitHub repository:
   - Click "Connect account" if not connected
   - Find and select your `pothole-detector` repository
   - Click "Connect"

### 3. Configure the Service

Render will auto-detect the `render.yaml` file, but verify these settings:

- **Name**: `pothole-detector` (or your choice)
- **Region**: Oregon (or closest to you)
- **Branch**: `main`
- **Runtime**: Python 3
- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `gunicorn app:app`
- **Plan**: Free

### 4. Environment Variables (Optional)

Add these if needed:
- `PYTHON_VERSION`: `3.11.0`
- `USE_DEPTH_ESTIMATION`: `true`

### 5. Deploy!

1. Click "Create Web Service"
2. Render will start building your app
3. Wait 5-10 minutes for first deployment
4. You'll get a URL like: `https://pothole-detector.onrender.com`

## Important Notes

### ⚠️ Free Tier Limitations

- **Sleeps after 15 minutes** of inactivity
- **Wakes up in ~30 seconds** when accessed
- **512MB RAM** (might be tight for depth estimation)
- **750 hours/month** free

### 🔧 Troubleshooting

**If deployment fails:**

1. **Out of Memory**: Disable depth estimation
   - Set `USE_DEPTH_ESTIMATION=false` in `app.py`
   - Or upgrade to paid tier ($7/month for 512MB+)

2. **Build timeout**: 
   - Render free tier has 15-minute build limit
   - PyTorch installation might timeout
   - Consider using lighter dependencies

3. **Model not found**:
   - Trained model (`best.pt`) is in `.gitignore`
   - You'll need to train on Render or upload separately
   - For demo, it will use pretrained YOLOv8

### 📱 Using the Deployed App

Once deployed:
- Access from anywhere: `https://your-app.onrender.com`
- Camera works (HTTPS enabled)
- Share the link with anyone
- Works on mobile devices

### 🚀 Performance Tips

1. **Keep it awake**: Visit every 14 minutes to prevent sleep
2. **Optimize images**: Compress uploads before detection
3. **Disable depth estimation**: If too slow, turn it off
4. **Upgrade plan**: $7/month for better performance

## Updating Your App

After making changes locally:

```bash
git add .
git commit -m "Your update message"
git push
```

Render will automatically detect the push and redeploy!

## Alternative: Deploy Without Depth Estimation

If Render free tier is too limited, disable depth estimation:

In `app.py`, change:
```python
USE_DEPTH_ESTIMATION = False  # Set to False
```

This will:
- Reduce memory usage
- Speed up detection
- Remove severity classification
- Make it work better on free tier

---

**Need help?** Check Render's logs in the dashboard for error messages.
