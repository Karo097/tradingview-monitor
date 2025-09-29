# TradingView Hourly Notifications - Cloud Cron Setup

## 🎯 **Simple, Reliable Solution**

This solution uses a cloud cron service to call our script every hour at 42 minutes past the hour. No Render.com complexity!

## 📁 **Files Created:**

1. **`tradingview_hourly_check.py`** - Main script that checks seller and sends Telegram notifications
2. **`email_notifier.py`** - Telegram bot integration (already working)
3. **`simple_web_service.py`** - Optional web service for hosting
4. **`CLOUD_CRON_SETUP.md`** - This setup guide

## 🚀 **Setup Options (Choose One):**

### **Option 1: Free Cloud Cron Service (Recommended)**

#### **Step 1: Choose a Free Cron Service**
- **cron-job.org** (Free, reliable)
- **easycron.com** (Free tier)
- **cronitor.io** (Free tier)
- **GitHub Actions** (Free, 2000 minutes/month)

#### **Step 2: Set Up Cron Job**
1. **URL to call**: `https://your-hosted-script.com/check`
2. **Schedule**: `42 * * * *` (every hour at 42 minutes)
3. **Method**: GET
4. **Timeout**: 60 seconds

#### **Step 3: Host the Script**
- **PythonAnywhere** (Free tier)
- **Heroku** (Free tier - but has limitations)
- **Railway** (Free tier)
- **Replit** (Free tier)

### **Option 2: GitHub Actions (Easiest)**

#### **Step 1: Create GitHub Repository**
1. Upload all files to a new GitHub repository
2. Go to **Actions** tab
3. Create new workflow

#### **Step 2: Create Workflow File**
Create `.github/workflows/tradingview-check.yml`:

```yaml
name: TradingView Hourly Check

on:
  schedule:
    - cron: '42 * * * *'  # Every hour at 42 minutes
  workflow_dispatch:  # Allow manual trigger

jobs:
  check:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v2
    - name: Set up Python
      uses: actions/setup-python@v2
      with:
        python-version: '3.9'
    - name: Install dependencies
      run: |
        pip install requests
    - name: Run TradingView check
      run: python tradingview_hourly_check.py
```

### **Option 3: Local Computer + Task Scheduler**

#### **Step 1: Set Up Task Scheduler**
1. Open **Task Scheduler** (Windows) or **crontab** (Mac/Linux)
2. Create new task
3. **Trigger**: Daily, repeat every 1 hour
4. **Action**: Run `python tradingview_hourly_check.py`

#### **Step 2: Keep Computer On**
- Computer must stay on 24/7
- Use power settings to prevent sleep

## 🎯 **Recommended: GitHub Actions**

**Why GitHub Actions is best:**
- ✅ **Completely free** (2000 minutes/month)
- ✅ **Reliable** (GitHub's infrastructure)
- ✅ **No hosting needed** (runs on GitHub's servers)
- ✅ **Easy setup** (just upload files and create workflow)
- ✅ **No sleep issues** (always available)

## 📋 **Quick Setup (5 minutes):**

1. **Upload files** to GitHub repository
2. **Create workflow** file (copy the YAML above)
3. **Enable Actions** in repository settings
4. **Done!** - Notifications will start at next 42-minute mark

## 🔧 **Testing:**

### **Test Locally:**
```bash
python tradingview_hourly_check.py
```

### **Test Web Service:**
```bash
python simple_web_service.py
# Then visit: http://localhost:5000/check
```

## 📱 **What You'll Get:**

- **Hourly notifications** at 42 minutes past each hour
- **Fresh JSON cookies** when seller is online
- **Last saved cookies** when seller is offline
- **24 notifications per day** with actual cookie data

## 🎉 **Benefits of This Solution:**

- 🚀 **No Render.com complexity**
- 💰 **Completely free**
- 🎯 **More reliable** (no sleep issues)
- 🔧 **Easier to maintain**
- ⚡ **Faster setup** (5 minutes vs hours)

## 📞 **Support:**

If you need help with any of these options, just let me know which one you'd prefer and I'll guide you through the setup!
