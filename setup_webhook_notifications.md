# Setup Webhook Notifications for TradingView Monitor

## Problem
Render.com free tier blocks outbound SMTP connections, so emails cannot be sent directly.

## Solution
Use free webhook services to send notifications.

## Option 1: Telegram Bot (Recommended - Free & Reliable)

### Setup Steps:
1. **Create Telegram Bot:**
   - Message @BotFather on Telegram
   - Send `/newbot`
   - Choose a name: "TradingView Monitor"
   - Choose a username: "tradingview_monitor_bot"
   - Get your bot token

2. **Get Your Chat ID:**
   - Message your bot
   - Visit: `https://api.telegram.org/bot<YOUR_BOT_TOKEN>/getUpdates`
   - Find your chat ID in the response

3. **Update the Code:**
   - Replace the Telegram webhook URL in `email_notifier.py`
   - Use format: `https://api.telegram.org/bot<TOKEN>/sendMessage?chat_id=<CHAT_ID>&text=`

## Option 2: Discord Webhook (Free)

### Setup Steps:
1. **Create Discord Server** (if you don't have one)
2. **Create Webhook:**
   - Go to Server Settings > Integrations > Webhooks
   - Click "Create Webhook"
   - Copy the webhook URL
3. **Update the Code:**
   - Replace Discord webhook URL in `email_notifier.py`

## Option 3: EmailJS (Free Email Service)

### Setup Steps:
1. **Sign up at emailjs.com**
2. **Create Email Service:**
   - Connect your Gmail account
   - Get Service ID
3. **Create Email Template:**
   - Create template with variables: {{to_email}}, {{subject}}, {{message}}
   - Get Template ID
4. **Get User ID:**
   - Found in EmailJS dashboard
5. **Update the Code:**
   - Replace EmailJS credentials in `email_notifier.py`

## Quick Setup (Telegram - 5 minutes)

1. Message @BotFather: `/newbot`
2. Name: "TradingView Monitor"
3. Username: "tradingview_monitor_bot"
4. Copy the token
5. Message your bot
6. Visit: `https://api.telegram.org/bot<TOKEN>/getUpdates`
7. Copy your chat ID
8. Update `email_notifier.py` with your token and chat ID

## Current Status
The system is logging notifications to console (visible in Render.com logs) as a fallback until webhook is configured.
