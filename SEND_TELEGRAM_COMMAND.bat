@echo off
echo ========================================
echo TradingView Telegram Command Sender
echo ========================================
echo.
echo Available commands:
echo 1. Check last 24 cookies
echo 2. Send help message
echo 3. Custom command
echo.
set /p choice="Enter your choice (1-3): "

if "%choice%"=="1" (
    echo Sending 'check cookies' command to Telegram...
    python telegram_bot.py
) else if "%choice%"=="2" (
    echo Sending help command to Telegram...
    python -c "from telegram_bot import TradingViewTelegramBot; bot = TradingViewTelegramBot(); bot.handle_command('/help')"
) else if "%choice%"=="3" (
    set /p custom="Enter custom command: "
    echo Sending custom command to Telegram...
    python -c "from telegram_bot import TradingViewTelegramBot; bot = TradingViewTelegramBot(); bot.handle_command('%custom%')"
) else (
    echo Invalid choice. Please run the script again.
)

echo.
echo ========================================
echo Command sent! Check your Telegram.
echo ========================================
pause
