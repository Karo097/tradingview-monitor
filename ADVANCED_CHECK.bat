@echo off
echo ========================================
echo Advanced TradingView Cookie Checker
echo ========================================
echo.
echo This will perform an advanced test of your
echo cookie files by actually trying to access
echo TradingView pages.
echo.
echo This test is more thorough and will tell you
echo exactly which cookies are working.
echo.
pause

py ADVANCED_COOKIE_CHECK.py

echo.
echo ========================================
echo Advanced check completed! Check your Telegram.
echo ========================================
echo.
echo The bot has sent you detailed results showing:
echo - Which cookies actually work with TradingView
echo - Which pages are accessible with each cookie
echo - Detailed status for each cookie file
echo.
pause
