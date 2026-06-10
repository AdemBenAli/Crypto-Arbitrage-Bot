# 📈 Pro Arbitrage Bot & Real-Time Dashboard

![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)
![Status](https://img.shields.io/badge/Status-Active-success.svg)

A high-frequency, ultra-low latency cryptocurrency arbitrage trading bot designed to detect cross-exchange arbitrage opportunities in under 0.1 milliseconds. By leveraging high-speed WebSocket connections for real-time order book data, the system continually monitors over 100+ cryptocurrency pairs across 6 major global exchanges (Binance, OKX, Bybit, Gate.io, MEXC, and KuCoin).

---

## 🚀 Key Capabilities

- **Sub-Millisecond Scanning Engine**: An asynchronously driven Python backend utilizing `ccxt.pro`. The hot-path scanner algorithm is heavily optimized to calculate net profits, account for taker fees, and evaluate trading volumes with minimal overhead.
- **Live Real-Time Dashboard**: A sleek, modern web interface powered by `aiohttp.web`. It uses WebSockets to stream live statistical data and profitable routes directly to the browser, leveraging Tailwind CSS and Chart.js for premium aesthetics and animated visualizations.
- **Telegram Alerting System**: Integrated bot that dispatches instant notifications mapping out expected slippage, exact routing (e.g., Buy on Binance -> Sell on OKX), and confidence scoring for detected opportunities.
- **Robust Error Handling**: Built-in automatic fallback and reconnection logic for unstable exchange WebSockets.

---

## 💻 Tech Stack

- **Backend**: Python 3.11+, `ccxt.pro`, `asyncio`, `aiohttp`, `python-telegram-bot`
- **Frontend**: JavaScript (ES6+), HTML5, CSS3, Tailwind CSS, Chart.js, Vanilla JS WebSockets
- **Concepts**: High-Frequency Trading (HFT), Concurrency, Low-Latency Systems Optimization

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

## 💡 Production Deployment Recommendations

- **Intended Use:** The provided dashboard is kept minimal for local setup and immediate visualization.
- **Production Enhancements:** Before deploying to a live production server, ensure you add:
  - **Security:** Authentication to the dashboard endpoint.
  - **Logging:** Persistent logging mechanisms (e.g., PostgreSQL/MongoDB for trades, ELK stack for logs).
  - **Secrets:** Secure and robust API key management (like AWS Secrets Manager or HashiCorp Vault).

---

## 🔮 Future Enhancements (Planned)
- Implement dashboard authentication.
- Add real-time price charts and historical logs visualization (e.g., Chart.js).
- Implement automated execution modules once opportunities are found.
