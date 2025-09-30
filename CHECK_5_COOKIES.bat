@echo off
echo ========================================
echo Check Last 5 Cookie Files
echo ========================================
echo.
echo This will check your last 5 cookie files
echo and send the results to your Telegram bot.
echo.
echo It will also create a file with all working
echo cookies ready for import.
echo.
pause

py INTERACTIVE_COOKIE_CHECKER.py 5

echo.
echo ========================================
echo Check completed! Check your Telegram.
echo ========================================
echo.
echo The bot has sent you the results and created
echo a file with working cookies ready for import.
echo.
pause
