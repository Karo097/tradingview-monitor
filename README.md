# TradingView Hourly Cookie Monitor

## 🎯 **What This Does**

Automatically checks TradingView seller status every hour at 42 minutes past the hour and sends Telegram notifications with fresh cookies.

## 📱 **Features**

- ✅ **Hourly Notifications**: Every hour at 42 minutes (24 notifications/day)
- ✅ **Fresh Cookies**: Automatically extracts and saves fresh TradingView cookies
- ✅ **Telegram Integration**: Sends notifications via Telegram bot
- ✅ **Seller Status**: Reports when seller is online/offline
- ✅ **Automatic**: Runs 24/7 via GitHub Actions (free)

## 🚀 **How It Works**

1. **GitHub Actions** runs the script every hour at 42 minutes
2. **Checks seller status** at the oxaam.com website
3. **Extracts fresh cookies** if seller is online
4. **Sends Telegram notification** with status and cookies
5. **Saves cookies** to file for backup

## 📁 **Files**

- `tradingview_hourly_check.py` - Main script that checks seller and sends notifications
- `email_notifier.py` - Telegram bot integration
- `.github/workflows/tradingview-check.yml` - GitHub Actions workflow
- `tradingview_cookies.json` - Saved cookies (created automatically)

## 🔧 **Setup**

The system is already configured and running! It will automatically:

- Check seller status every hour at 42 minutes past the hour
- Send Telegram notifications with fresh cookies
- Save cookies to file for backup

## 📱 **Telegram Notifications**

You'll receive notifications like:

**When Seller is Online:**
```
TradingView Hourly Report - 14:42

Time: 2025-09-30 14:42:15
Status: Seller is ONLINE! 16 fresh cookies available
Cookies: 16 fresh cookies available

SELLER STATUS: ONLINE ✅

Fresh cookies are available and saved to file.
Download: https://tradingview-monitor.onrender.com/download-browser-import

Next update: 15:42
```

**When Seller is Offline:**
```
TradingView Hourly Report - 15:42 (OFFLINE)

Time: 2025-09-30 15:42:15
Status: Seller is OFFLINE - No fresh cookies available

SELLER STATUS: OFFLINE ⏳

No fresh cookies available at this time.
Last saved: 16 last saved cookies

The system continues monitoring and will notify you when the seller comes back online.

Next update: 16:42
```

## 🎉 **Benefits**

- 🚀 **Fully Automated**: No manual intervention needed
- 💰 **Completely Free**: Uses GitHub Actions free tier
- 🎯 **Reliable**: Runs on GitHub's infrastructure
- 📱 **Real-time**: Get notifications instantly
- 🔄 **24/7**: Works even when your computer is off

## 📊 **Schedule**

- **00:42, 01:42, 02:42, 03:42, 04:42, 05:42**
- **06:42, 07:42, 08:42, 09:42, 10:42, 11:42**
- **12:42, 13:42, 14:42, 15:42, 16:42, 17:42**
- **18:42, 19:42, 20:42, 21:42, 22:42, 23:42**

**24 notifications per day with fresh TradingView cookies!**
