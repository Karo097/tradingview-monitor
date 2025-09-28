@echo off
echo ========================================
echo    TradingView Monitor Auto Deploy
echo ========================================
echo.

echo [1/4] Preparing files for deployment...
echo.

echo [2/4] Creating deployment package...
echo - web_monitor.py (updated)
echo - email_notifier.py (updated) 
echo - requirements.txt (ready)
echo - Procfile (ready)
echo.

echo [3/4] Files ready for GitHub upload:
echo.
echo UPLOAD THESE FILES TO GITHUB:
echo =============================
echo 1. web_monitor.py
echo 2. email_notifier.py
echo.
echo GitHub Repository: https://github.com/Karo097/tradingview-monitor
echo.
echo QUICK UPLOAD STEPS:
echo ===================
echo 1. Go to: https://github.com/Karo097/tradingview-monitor
echo 2. Click "Add file" ^> "Upload files"
echo 3. Drag and drop: web_monitor.py and email_notifier.py
echo 4. Commit message: "Fix privacy, monitoring, and add cookie storage"
echo 5. Click "Commit changes"
echo.

echo [4/4] After upload:
echo - Render.com will auto-deploy in 2-3 minutes
echo - Check: https://tradingview-monitor.onrender.com
echo - Your email will be hidden from public view
echo - Monitoring will show 30 minutes (not 5 minutes)
echo - Cookies will be saved for offline access
echo.

echo ========================================
echo    DEPLOYMENT READY!
echo ========================================
echo.
echo Press any key to open GitHub repository...
pause >nul

start https://github.com/Karo097/tradingview-monitor

echo.
echo GitHub opened! Upload the 2 files and you're done!
echo.
pause
