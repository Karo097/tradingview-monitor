@echo off
echo ========================================
echo Setting up Telegram Bot Webhook
echo ========================================
echo.
echo This will set up your Telegram bot to respond
echo to commands like "check last 24"
echo.
echo Step 1: Setting webhook URL...
echo.

REM Set webhook URL (you'll need to replace this with your actual webhook URL)
set WEBHOOK_URL=https://your-webhook-url.com/webhook

REM Set webhook
curl -X POST "https://api.telegram.org/bot7405449740:AAFWd4zQYqr8JyRTPB5jQ0oPV_D00ep28Ms/setWebhook" -H "Content-Type: application/json" -d "{\"url\":\"%WEBHOOK_URL%\"}"

echo.
echo Step 2: Testing webhook...
echo.

REM Test webhook
curl -X GET "https://api.telegram.org/bot7405449740:AAFWd4zQYqr8JyRTPB5jQ0oPV_D00ep28Ms/getWebhookInfo"

echo.
echo ========================================
echo Setup completed!
echo ========================================
echo.
echo NOTE: You need to deploy the webhook bot to a server
echo for it to respond to your commands.
echo.
echo For now, use RUN_SIMPLE_TEST.bat to check cookies.
echo.
pause
