@echo off
echo ========================================
echo    AUTO DEPLOY - TradingView Monitor
echo ========================================
echo.

echo Files ready for deployment:
echo - web_monitor.py (updated with all fixes)
echo - email_notifier.py (improved email handling)
echo - requirements.txt (dependencies)
echo - Procfile (Render.com config)
echo.

echo Initializing Git repository...
git init
git remote add origin https://github.com/Karo097/tradingview-monitor.git

echo.
echo Adding files to Git...
git add .

echo.
echo Committing changes...
git commit -m "Fix privacy, monitoring interval, and add cookie storage"

echo.
echo Pushing to GitHub...
git push -u origin main

echo.
echo ========================================
echo    DEPLOYMENT COMPLETE!
echo ========================================
echo.
echo What's been fixed:
echo - Email address removed from public display
echo - UI shows 30 minutes (not 5 minutes)
echo - 3-hour email notifications (not spam)
echo - Persistent cookie storage added
echo - Download endpoint for saved cookies
echo.
echo Check: https://tradingview-monitor.onrender.com
echo Render.com will auto-deploy in 2-3 minutes
echo.

pause
