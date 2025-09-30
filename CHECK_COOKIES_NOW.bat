@echo off
echo ========================================
echo TradingView Cookie Checker
echo ========================================
echo.
echo This will check your last 24 cookie files
echo and send the results to your Telegram bot.
echo.
echo Sending command to Telegram...
echo.

py SIMPLE_COOKIE_TEST.py

echo.
echo ========================================
echo Check completed! Check your Telegram.
echo ========================================
echo.
echo The bot has sent you the cookie check results.
echo You should see a message with:
echo - Which cookies are working
echo - Which cookies are expired
echo - Recommendation for best cookie to use
echo.
pause
