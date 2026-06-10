# 📈 Pro Arbitrage Bot & Real-Time Dashboard

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)
![Status](https://img.shields.io/badge/Status-Active-success.svg)

A high-performance, WebSocket-based cross-exchange cryptocurrency arbitrage scanner with a lightweight real-time dashboard. This project is designed to detect and stream arbitrage opportunities across multiple exchanges with minimal latency.

---

## 🚀 Features

- **High-Performance Scanning**: Powered by `ccxt.pro`, utilizing WebSockets for real-time market data.
- **Cross-Exchange Capabilities**: Continuously monitors multiple exchanges for price discrepancies.
- **Live Real-Time Dashboard**: A lightweight `aiohttp` web server streaming live stats and arbitrage opportunities directly to your browser.
- **Env Variable Configuration**: Easy integration of API keys and Telegram bot tokens via `.env` file.

---

## 📁 Project Structure

- `pro_bot.py`: The core arbitrage engine handling multi-exchange WebSocket connections.
- `dashboard.py`: An `aiohttp` based web server to visualize the bot's findings in real-time.
- `requirements.txt`: Python package dependencies.

---

## 🛠️ Quick Start (Local Setup)

### 1. Environment Setup
Create a Python virtual environment and activate it:
```powershell
python -m venv .venv

# Windows
.\.venv\Scripts\Activate.ps1
# Linux/macOS
source .venv/bin/activate
```

### 2. Install Dependencies
Install the required packages to run the bot and dashboard:
```bash
pip install -r requirements.txt
pip install aiohttp
```
*(Note: `ccxt.pro` is required for real WebSocket connections)*

### 3. Configuration
Create a `.env` file in the root directory to store your API keys and configuration safely:
```env
# Exchange API Keys (Optional for basic scanning)
BINANCE_API_KEY=your_binance_key
BINANCE_SECRET=your_binance_secret
OKX_API_KEY=your_okx_key
OKX_SECRET=your_okx_secret
OKX_PASSPHRASE=your_okx_passphrase

# Notifications
TELEGRAM_TOKEN=your_telegram_bot_token
CHAT_ID=your_chat_id
```

### 4. Run the Bot and Dashboard
Start the real-time web UI, which will automatically initialize the arbitrage scanner:
```bash
python dashboard.py
```
🌐 **Open:** [http://localhost:8080](http://localhost:8080) in your web browser to view the live dashboard.

---

## 💡 Notes for Portfolio / Demo Use

- **Intended Use:** The dashboard is intentionally kept minimal for immediate demonstrations, recordings, or Upwork portfolio showcasing.
- **Production Recommendations:** Before deploying to a live production environment, consider adding:
  - Authentication to the dashboard.
  - Persistent logging mechanisms (e.g., database integrations).
  - Secure and robust API key management (like AWS Secrets Manager).
- **Showcasing:** Run the bot locally and use a screen recorder to capture the UI and terminal for a compelling Upwork portfolio piece.

---

## 🔮 Future Enhancements (Planned)
- Implement dashboard authentication.
- Add real-time price charts and historical logs visualization (e.g., Chart.js).
- Implement automated execution modules once opportunities are found.
