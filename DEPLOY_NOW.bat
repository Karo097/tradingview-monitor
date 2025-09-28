@echo off
chcp 65001 >nul
echo ========================================
echo    TradingView Monitor - DEPLOY NOW
echo ========================================
echo.

echo FILES READY FOR DEPLOYMENT:
echo ============================
echo 1. web_monitor.py (ALL FIXES APPLIED)
echo 2. email_notifier.py (IMPROVED)
echo.

echo WHAT'S BEEN FIXED:
echo ===================
echo - Email address removed from public page
echo - UI shows 30 minutes (not 5 minutes)  
echo - 3-hour email notifications (not spam)
echo - Persistent cookie storage added
echo - Download endpoint for offline access
echo.

echo DEPLOYMENT STEPS:
echo ==================
echo 1. GitHub will open automatically
echo 2. Click "Add file" ^> "Upload files"
echo 3. Upload: web_monitor.py and email_notifier.py
echo 4. Commit message: "Fix privacy and monitoring"
echo 5. Click "Commit changes"
echo.

echo Opening GitHub repository...
timeout /t 3 /nobreak >nul
start https://github.com/Karo097/tradingview-monitor

echo.
echo GitHub opened! Upload the 2 files now.
echo.
echo After upload:
echo - Render.com will auto-deploy in 2-3 minutes
echo - Check: https://tradingview-monitor.onrender.com
echo - Your email will be hidden from public view
echo.

pause
