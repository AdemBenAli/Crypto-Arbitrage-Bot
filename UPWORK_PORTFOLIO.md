# Ultra-Fast Crypto Arbitrage Bot & Real-Time Dashboard

## 🚀 Project Overview
Developed a high-frequency, ultra-low latency cryptocurrency arbitrage trading bot designed to detect and execute cross-exchange arbitrage opportunities in under 0.1 milliseconds. By leveraging high-speed WebSocket connections for real-time order book data, the system continually monitors over 100+ cryptocurrency pairs across 6 major global exchanges (Binance, OKX, Bybit, Gate.io, MEXC, and KuCoin) and instantly dispatches detailed profitability alerts to a dedicated Telegram bot.

The project is split into two core components:
1. **The Trading Engine:** An asynchronously driven Python backend utilizing `ccxt.pro` for WebSocket-based live order book data fetching. The hot-path scanner algorithm is heavily optimized to calculate net profits, account for taker fees, and evaluate trading volumes with minimal overhead.
2. **The Real-Time Dashboard:** A sleek, modern, dark-themed web interface powered by `aiohttp.web`. It uses WebSockets to stream live statistical data and profitable arbitrage routes directly to the browser. The frontend leverages Tailwind CSS for premium aesthetics and Chart.js for live, animated latency and profit visualizations.

Furthermore, the system features an integrated Telegram bot that acts as an alerting mechanism, providing users with a comprehensive breakdown of risk metrics, liquidity, and potential profits for every detected opportunity.

## 🛠️ Skills & Technologies Used
* **Programming Languages:** Python 3.11+, JavaScript (ES6+), HTML5, CSS3
* **Libraries & Frameworks:** `ccxt.pro`, `asyncio`, `aiohttp`, `python-telegram-bot`
* **Frontend Technologies:** Tailwind CSS, Chart.js, Vanilla JS WebSockets
* **Core Competencies:**
  * High-Frequency Trading (HFT) Algorithms
  * Asynchronous Programming & Concurrency (Asyncio)
  * Real-Time WebSocket Data Streaming
  * API Integration (REST & WebSockets)
  * Low-Latency Systems Optimization
  * UI/UX Design for Financial Dashboards

## 📦 Deliverables
* **Arbitrage Scanner Engine:** A robust, memory-efficient Python script (`pro_bot.py`) capable of parsing thousands of order book updates per second and executing concurrent market orders.
* **Live Web Dashboard:** A responsive, single-page application served locally (`dashboard.py`) that visualizes the bot's health, scan rates, and found opportunities in real-time without requiring a database.
* **Telegram Alerting System:** Automated instant notifications mapping out expected slippage, exact routing (e.g., Buy on Binance -> Sell on OKX), and confidence scoring.
* **Deployment & Configuration Files:** Environment setup utilizing `.env` for secure API key and token management.

## 📈 Key Achievements
* **Sub-Millisecond Scanning:** Engineered the hot-path loop to achieve a consistent scan latency of less than 0.1ms per cycle.
* **Robust Error Handling:** Integrated automatic fallback and reconnection logic for unstable exchange WebSockets.
* **Professional Aesthetics:** Replaced a static text interface with a responsive, glassmorphism-styled dashboard tailored for crypto-traders, significantly improving the end-user experience.
