@echo off
echo ========================================
echo Starting Interactive Telegram Bot
echo ========================================
echo.
echo This will start the bot that can respond
echo to your messages directly in Telegram.
echo.
echo The bot will:
echo - Listen for your messages
echo - Respond to commands like "check cookies"
echo - Test your cookies and send results
echo.
echo Press Ctrl+C to stop the bot when done.
echo.
pause

py INTERACTIVE_TELEGRAM_BOT.py

echo.
echo ========================================
echo Bot stopped.
echo ========================================
pause
