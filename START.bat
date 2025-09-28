@echo off
title TradingView Cookie Manager
color 0A

echo.
echo ========================================
echo    TradingView Cookie Manager
echo ========================================
echo.

py --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed
    pause
    exit /b 1
)

echo Installing dependencies...
py -m pip install requests pyperclip --quiet

echo.
echo Starting TradingView Cookie Manager...
py tradingview_manager.py

pause