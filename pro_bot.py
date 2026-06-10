"""
🚀 PRO ARBITRAGE BOT v2.0 - ULTRA OPTIMIZED
=============================================
- WebSocket real-time price feeds
- <0.1ms scan latency (optimized hot path)
- 100+ coins across 6 exchanges
- Pre-computed exchange pairs
- Async order execution
"""

import ccxt.pro as ccxtpro
import ccxt
import asyncio
import os
import time
from telegram import Bot
from datetime import datetime
from dotenv import load_dotenv
import aiohttp

load_dotenv()

# ================= CONFIG =================

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

# API Keys for trading (optional - works without for scanning)
BINANCE_API_KEY = os.getenv("BINANCE_API_KEY")
BINANCE_SECRET = os.getenv("BINANCE_SECRET")
OKX_API_KEY = os.getenv("OKX_API_KEY")
OKX_SECRET = os.getenv("OKX_SECRET")
OKX_PASSPHRASE = os.getenv("OKX_PASSPHRASE")

# ============ 100+ COINS TO SCAN ============
# Tier 1: High volume majors
TIER1_COINS = [
    "BTC/USDT", "ETH/USDT", "SOL/USDT", "XRP/USDT", "BNB/USDT",
    "DOGE/USDT", "ADA/USDT", "AVAX/USDT", "DOT/USDT", "LINK/USDT",
    "MATIC/USDT", "UNI/USDT", "LTC/USDT", "ATOM/USDT", "ETC/USDT",
]

# Tier 2: Meme coins (high volatility = more opportunities)
MEME_COINS = [
    "PEPE/USDT", "SHIB/USDT", "WIF/USDT", "BONK/USDT", "FLOKI/USDT",
    "MEME/USDT", "SATS/USDT", "RATS/USDT", "COQ/USDT", "MYRO/USDT",
    "LADYS/USDT", "TURBO/USDT", "BOB/USDT", "MONG/USDT", "WOJAK/USDT",
]

# Tier 3: AI & DeFi tokens
AI_DEFI_COINS = [
    "FET/USDT", "RNDR/USDT", "AGIX/USDT", "OCEAN/USDT", "TAO/USDT",
    "INJ/USDT", "AAVE/USDT", "SNX/USDT", "CRV/USDT", "COMP/USDT",
    "MKR/USDT", "LDO/USDT", "RPL/USDT", "PENDLE/USDT", "GMX/USDT",
]

# Tier 4: Layer 1/2 chains
L1_L2_COINS = [
    "SUI/USDT", "APT/USDT", "SEI/USDT", "TIA/USDT", "ARB/USDT",
    "OP/USDT", "STRK/USDT", "MANTA/USDT", "BLAST/USDT", "ZK/USDT",
    "NEAR/USDT", "FTM/USDT", "KAVA/USDT", "CELO/USDT", "ROSE/USDT",
]

# Tier 5: Gaming & NFT
GAMING_NFT_COINS = [
    "IMX/USDT", "GALA/USDT", "AXS/USDT", "SAND/USDT", "MANA/USDT",
    "ENJ/USDT", "ILV/USDT", "YGG/USDT", "MAGIC/USDT", "PRIME/USDT",
    "PIXEL/USDT", "PORTAL/USDT", "BIGTIME/USDT", "XAI/USDT", "RONIN/USDT",
]

# Tier 6: Low-cap altcoins (higher spreads but lower volume)
LOWCAP_COINS = [
    "ORDI/USDT", "BLUR/USDT", "ARKM/USDT", "CYBER/USDT", "LOOM/USDT",
    "ACE/USDT", "NFP/USDT", "MAVIA/USDT",
    "PYTH/USDT", "JTO/USDT", "JUP/USDT", "BOME/USDT",
    "SLERF/USDT", "MEW/USDT", "POPCAT/USDT", "DOGS/USDT",
]

# ⚠️ BLACKLIST - Tokens avec même nom mais différents projets sur chaque exchange
# Ces tokens causent des faux positifs car ce sont des tokens DIFFÉRENTS!
BLACKLIST = [
    "NEIRO/USDT",   # Différent token sur Binance vs KuCoin/autres
    "AI/USDT",      # Plusieurs projets "AI" 
    "XAI/USDT",     # Conflit de symbole
    "WEN/USDT",     # Différent sur chaque exchange
    "FLOW/USDT",    # Prix incohérents entre exchanges
]

# Tier 7: Classic altcoins
CLASSIC_COINS = [
    "TRX/USDT", "VET/USDT", "ALGO/USDT", "XLM/USDT", "HBAR/USDT",
    "ICP/USDT", "FIL/USDT", "THETA/USDT", "XTZ/USDT", "EOS/USDT",
    "EGLD/USDT", "FLOW/USDT", "MINA/USDT", "KSM/USDT", "ZEC/USDT",
]

# Combine all coins (excluding blacklisted)
SYMBOLS = [s for s in set(
    TIER1_COINS + MEME_COINS + AI_DEFI_COINS + L1_L2_COINS + 
    GAMING_NFT_COINS + LOWCAP_COINS + CLASSIC_COINS
) if s not in BLACKLIST]

print(f"📊 Total unique coins: {len(SYMBOLS)} (excl. {len(BLACKLIST)} blacklisted)")

# ============ TRADING SETTINGS (SAFER FOR AUTO-TRADE) ============
TRADE_AMOUNT_USDT = 50  # Start small! Increase after testing
TAKER_FEE = 0.001  # 0.1%
TOTAL_FEE = TAKER_FEE * 2  # Pre-computed: buy + sell fee

# ⚠️ PROFIT THRESHOLDS - HIGHER = SAFER
MIN_PROFIT_PCT = 0.005  # 0.5% minimum - SAFER for auto-trading!
MAX_PROFIT_PCT = 0.05   # 5% max - anything higher is likely false positive

# ⚠️ VOLUME REQUIREMENTS - Ensures enough liquidity
MIN_VOLUME_USDT = 100  # Minimum $100 volume on each side (was $50)

# ⚠️ RISK LEVELS
LOW_RISK_PROFIT = 0.007   # 0.7%+ = Low risk (green)
MED_RISK_PROFIT = 0.005   # 0.5-0.7% = Medium risk (yellow) 
# Below 0.3% = High risk (not shown with these settings)

ENABLE_TRADING = False  # Set True to enable real trading

# ==========================================

# Pre-computed exchange pairs for O(1) iteration
EXCHANGE_NAMES = ["binance", "okx", "bybit", "gate", "mexc", "kucoin"]
EXCHANGE_PAIRS = [(a, b) for a in EXCHANGE_NAMES for b in EXCHANGE_NAMES if a != b]

class PriceBook:
    """Ultra-fast price storage - optimized for <0.1ms access"""
    __slots__ = ['_data', '_timestamps', '_current_time']
    
    def __init__(self):
        # Use simple dicts for fastest access
        self._data = {}  # {symbol: {exchange: (bid, ask, bid_vol, ask_vol)}}
        self._timestamps = {}  # {symbol: {exchange: timestamp_ms}}
        self._current_time = 0
    
    def update(self, exchange: str, symbol: str, bid: float, ask: float, bid_vol: float, ask_vol: float):
        if symbol not in self._data:
            self._data[symbol] = {}
            self._timestamps[symbol] = {}
        self._data[symbol][exchange] = (bid, ask, bid_vol, ask_vol)
        self._timestamps[symbol][exchange] = time.time() * 1000
    
    def get_price(self, symbol: str, exchange: str):
        """Direct access - no dict creation"""
        sym_data = self._data.get(symbol)
        if sym_data:
            return sym_data.get(exchange)
        return None
    
    def get_timestamp(self, symbol: str, exchange: str) -> float:
        sym_ts = self._timestamps.get(symbol)
        if sym_ts:
            return sym_ts.get(exchange, 0)
        return 0
    
    def get_exchanges_for_symbol(self, symbol: str) -> list:
        sym_data = self._data.get(symbol)
        return list(sym_data.keys()) if sym_data else []


class ProArbitrageBot:
    def __init__(self):
        self.price_book = PriceBook()
        self.exchanges = {}
        self.running = False
        self.stats = {
            "opportunities": 0,
            "total_profit": 0,
            "best_profit": 0,
            "start_time": None,
            "latency_sum": 0,
            "latency_count": 0,
        }
        self.bot = Bot(token=TELEGRAM_TOKEN) if TELEGRAM_TOKEN else None
        self.last_alert_time = 0
        self.alert_cooldown = 5  # seconds between alerts
        # In-process event queue for dashboards / UIs to subscribe to
        # Use a bounded queue to avoid blocking the hot path
        try:
            self.event_queue = asyncio.Queue(maxsize=200)
        except Exception:
            # Fallback for synchronous contexts
            self.event_queue = None
        
    async def init_exchanges(self):
        """Initialize WebSocket connections to all exchanges"""
        print("🔌 Initializing WebSocket connections...")
        
        exchange_configs = {
            "binance": {
                "apiKey": BINANCE_API_KEY,
                "secret": BINANCE_SECRET,
                "enableRateLimit": True,
                "options": {"defaultType": "spot"}
            },
            "okx": {
                "apiKey": OKX_API_KEY,
                "secret": OKX_SECRET,
                "password": OKX_PASSPHRASE,
                "enableRateLimit": True,
            },
            "bybit": {"enableRateLimit": True},
            "gate": {"enableRateLimit": True},
            "mexc": {"enableRateLimit": True},
            "kucoin": {"enableRateLimit": True},
        }
        
        for name, config in exchange_configs.items():
            try:
                exchange_class = getattr(ccxtpro, name)
                self.exchanges[name] = exchange_class(config)
                print(f"  ✅ {name.upper()}: Ready")
            except Exception as e:
                print(f"  ❌ {name.upper()}: {e}")
        
        print(f"\n📡 {len(self.exchanges)} exchanges connected via WebSocket\n")

    async def watch_orderbook(self, exchange_name: str, symbol: str):
        """Watch orderbook for a single symbol on one exchange"""
        exchange = self.exchanges.get(exchange_name)
        if not exchange:
            return
        
        retry_count = 0
        max_retries = 5
        
        while self.running and retry_count < max_retries:
            try:
                orderbook = await exchange.watch_order_book(symbol, limit=5)
                
                if orderbook["bids"] and orderbook["asks"]:
                    bid = orderbook["bids"][0][0]
                    ask = orderbook["asks"][0][0]
                    bid_vol = orderbook["bids"][0][1]
                    ask_vol = orderbook["asks"][0][1]
                    
                    self.price_book.update(exchange_name, symbol, bid, ask, bid_vol, ask_vol)
                
                retry_count = 0  # Reset on success
                
            except ccxt.BadSymbol:
                return  # Symbol not available on this exchange
            except Exception as e:
                retry_count += 1
                if retry_count < max_retries:
                    await asyncio.sleep(1)

    async def arbitrage_scanner(self):
        """Ultra-fast arbitrage detection loop - OPTIMIZED <0.1ms"""
        print("🔍 Starting ULTRA-FAST arbitrage scanner (<0.1ms target)...\n")
        
        scan_count = 0
        current_time_ms = 0
        
        # Pre-allocate variables outside loop for speed
        _get_price = self.price_book.get_price
        _get_timestamp = self.price_book.get_timestamp
        _symbols = SYMBOLS
        _pairs = EXCHANGE_PAIRS
        _total_fee = TOTAL_FEE
        _min_profit = MIN_PROFIT_PCT
        _trade_amount = TRADE_AMOUNT_USDT
        
        while self.running:
            start_time = time.time()
            current_time_ms = start_time * 1000
            scan_count += 1
            
            best_profit = -999.0
            best_opp_data = None
            
            # OPTIMIZED HOT PATH - minimal function calls
            for symbol in _symbols:
                for buy_ex, sell_ex in _pairs:
                    # Direct tuple access (faster than dict)
                    buy_data = _get_price(symbol, buy_ex)
                    if not buy_data:
                        continue
                    
                    sell_data = _get_price(symbol, sell_ex)
                    if not sell_data:
                        continue
                    
                    # Inline freshness check
                    buy_ts = _get_timestamp(symbol, buy_ex)
                    sell_ts = _get_timestamp(symbol, sell_ex)
                    
                    if current_time_ms - buy_ts > 500 or current_time_ms - sell_ts > 500:
                        continue
                    
                    # Tuple unpacking: (bid, ask, bid_vol, ask_vol)
                    buy_price = buy_data[1]  # ask
                    sell_price = sell_data[0]  # bid
                    buy_vol = buy_data[3]  # ask_vol
                    sell_vol = sell_data[2]  # bid_vol
                    
                    if buy_price <= 0:
                        continue
                    
                    # Volume check - ensure enough liquidity
                    min_vol_usdt = min(buy_vol * buy_price, sell_vol * sell_price)
                    if min_vol_usdt < MIN_VOLUME_USDT:
                        continue
                    
                    # Inline profit calculation
                    net_profit = ((sell_price - buy_price) / buy_price) - _total_fee
                    
                    if net_profit > best_profit:
                        best_profit = net_profit
                        best_opp_data = (
                            symbol, buy_ex, sell_ex,
                            buy_price, sell_price,
                            buy_vol, sell_vol,  # ask_vol, bid_vol
                            current_time_ms - max(buy_ts, sell_ts)
                        )
            
            scan_time = (time.time() - start_time) * 1000
            self.stats["latency_sum"] += scan_time
            self.stats["latency_count"] += 1
            avg_latency = self.stats["latency_sum"] / self.stats["latency_count"]
            
            # Display status (outside hot path)
            # Publish lightweight stats for dashboards (non-blocking)
            try:
                stats_event = {
                    "type": "stats",
                    "scan_count": scan_count,
                    "avg_latency": avg_latency,
                    "best_profit": self.stats["best_profit"],
                    "opportunities": self.stats["opportunities"],
                }
                if getattr(self, "event_queue", None):
                    try:
                        self.event_queue.put_nowait(stats_event)
                    except Exception:
                        pass
            except Exception:
                pass

            if best_opp_data:
                symbol, buy_ex, sell_ex, buy_price, sell_price, buy_vol, sell_vol, latency = best_opp_data
                gross_profit = ((sell_price - buy_price) / buy_price) * 100
                net_profit_pct = best_profit * 100
                profit_usdt = best_profit * _trade_amount
                
                status_icon = "🟢" if best_profit > 0 else "🔴"
                
                print(f"\r[{datetime.now().strftime('%H:%M:%S.%f')[:-3]}] "
                      f"#{scan_count:,} | "
                      f"⚡{scan_time:.2f}ms | "
                      f"{status_icon} {symbol}: {buy_ex.upper()}→{sell_ex.upper()} "
                      f"{net_profit_pct:+.4f}% | "
                      f"Ops: {self.stats['opportunities']}", end="", flush=True)
                
                # PROFITABLE OPPORTUNITY FOUND!
                # Filter out unrealistic profits (>10% = likely false positive)
                if best_profit >= _min_profit and best_profit <= MAX_PROFIT_PCT:
                    self.stats["opportunities"] += 1
                    self.stats["total_profit"] += profit_usdt
                    
                    if net_profit_pct > self.stats["best_profit"]:
                        self.stats["best_profit"] = net_profit_pct
                    
                    # Build opportunity dict only when needed
                    opp = {
                        "symbol": symbol,
                        "buy_exchange": buy_ex.upper(),
                        "sell_exchange": sell_ex.upper(),
                        "buy_price": buy_price,
                        "sell_price": sell_price,
                        "buy_vol": buy_vol,
                        "sell_vol": sell_vol,
                        "gross_profit": gross_profit,
                        "net_profit": net_profit_pct,
                        "profit_usdt": profit_usdt,
                        "latency_ms": latency,
                    }
                    # Publish the opportunity for UIs/dashboards
                    if getattr(self, "event_queue", None):
                        try:
                            self.event_queue.put_nowait({"type": "opportunity", "opp": opp})
                        except Exception:
                            pass
                    await self.handle_opportunity(opp)
            else:
                print(f"\r[{datetime.now().strftime('%H:%M:%S.%f')[:-3]}] "
                      f"#{scan_count:,} | ⚡{scan_time:.2f}ms | "
                      f"Waiting for data... | Avg: {avg_latency:.2f}ms", end="", flush=True)
            
            # Minimal sleep to prevent CPU overload (0.5ms)
            await asyncio.sleep(0.0005)

    async def handle_opportunity(self, opp: dict):
        """Handle profitable opportunity - alert and optionally execute"""
        current_time = time.time()
        
        print(f"\n\n{'='*60}")
        print(f"🚨 PROFITABLE OPPORTUNITY DETECTED!")
        print(f"{'='*60}")
        print(f"  Symbol: {opp['symbol']}")
        print(f"  Route: {opp['buy_exchange']} → {opp['sell_exchange']}")
        print(f"  Buy:  ${opp['buy_price']:.8f} (vol: {opp['buy_vol']:.4f})")
        print(f"  Sell: ${opp['sell_price']:.8f} (vol: {opp['sell_vol']:.4f})")
        print(f"  Gross: +{opp['gross_profit']:.4f}%")
        print(f"  Net:   +{opp['net_profit']:.4f}%")
        print(f"  Profit: +${opp['profit_usdt']:.4f}")
        print(f"  Latency: {opp['latency_ms']:.1f}ms")
        print(f"{'='*60}\n")
        
        # Send Telegram alert (with cooldown)
        if current_time - self.last_alert_time > self.alert_cooldown:
            self.last_alert_time = current_time
            await self.send_telegram_alert(opp)
        
        # Execute trade if enabled
        if ENABLE_TRADING:
            await self.execute_arbitrage(opp)

    async def execute_arbitrage(self, opp: dict):
        """Execute arbitrage trade on both exchanges simultaneously"""
        print("⚡ EXECUTING ARBITRAGE...")
        
        buy_exchange = self.exchanges.get(opp["buy_exchange"].lower())
        sell_exchange = self.exchanges.get(opp["sell_exchange"].lower())
        
        if not buy_exchange or not sell_exchange:
            print("❌ Exchange not available for trading")
            return
        
        symbol = opp["symbol"]
        amount = TRADE_AMOUNT_USDT / opp["buy_price"]
        
        try:
            # Execute BOTH orders simultaneously
            start = time.time()
            
            buy_task = asyncio.create_task(
                buy_exchange.create_market_buy_order(symbol, amount)
            )
            sell_task = asyncio.create_task(
                sell_exchange.create_market_sell_order(symbol, amount)
            )
            
            buy_result, sell_result = await asyncio.gather(buy_task, sell_task, return_exceptions=True)
            
            execution_time = (time.time() - start) * 1000
            
            print(f"✅ Orders executed in {execution_time:.1f}ms")
            print(f"  Buy: {buy_result}")
            print(f"  Sell: {sell_result}")
            
        except Exception as e:
            print(f"❌ Execution error: {e}")

    async def send_telegram_alert(self, opp: dict):
        """Send detailed Telegram notification with risk assessment"""
        if not self.bot:
            return
        
        # Calculate risk metrics
        net_profit = opp['net_profit'] / 100  # Convert back to decimal
        min_volume = min(opp['buy_vol'], opp['sell_vol'])
        volume_usdt = min_volume * opp['buy_price']
        max_trade = min(volume_usdt * 0.5, TRADE_AMOUNT_USDT)  # Max 50% of available volume
        
        # Risk assessment
        if net_profit >= LOW_RISK_PROFIT:
            risk_level = "🟢 LOW RISK"
            risk_emoji = "✅"
            recommendation = "GOOD TO TRADE"
        elif net_profit >= MED_RISK_PROFIT:
            risk_level = "🟡 MEDIUM RISK"
            risk_emoji = "⚠️"
            recommendation = "TRADE WITH CAUTION"
        else:
            risk_level = "🔴 HIGH RISK"
            risk_emoji = "❌"
            recommendation = "NOT RECOMMENDED"
        
        # Slippage estimate (higher for low volume)
        if volume_usdt > 1000:
            slippage_est = "~0.01%"
            slippage_warning = ""
        elif volume_usdt > 200:
            slippage_est = "~0.05%"
            slippage_warning = ""
        else:
            slippage_est = "~0.1-0.3%"
            slippage_warning = "\n⚠️ LOW VOLUME - High slippage risk!"
        
        # Confidence score (0-100)
        confidence = min(100, int(
            (net_profit / 0.01) * 30 +  # Profit component (max 30)
            min(30, (volume_usdt / 500) * 30) +  # Volume component (max 30)
            max(0, (500 - opp['latency_ms']) / 500 * 20) +  # Freshness (max 20)
            20  # Base score
        ))
        
        message = f"""
🚨 ARBITRAGE OPPORTUNITY!
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

{risk_emoji} {risk_level}
📊 Confidence: {confidence}/100
💡 {recommendation}

━━━━━━━ TRADE DETAILS ━━━━━━━

🪙 Token: {opp['symbol']}
🔄 Route: {opp['buy_exchange']} → {opp['sell_exchange']}

📈 PRICES
┃ Buy @  ${opp['buy_price']:.8f}
┃ Sell @ ${opp['sell_price']:.8f}
┃ Spread: {opp['gross_profit']:.4f}%

💰 PROFIT ANALYSIS
┃ Gross Profit: +{opp['gross_profit']:.4f}%
┃ Fees (0.2%):  -0.2000%
┃ ─────────────────────
┃ Net Profit:   +{opp['net_profit']:.4f}%
┃ 
┃ On ${TRADE_AMOUNT_USDT}: +${opp['profit_usdt']:.2f}
┃ Max safe trade: ${max_trade:.0f}

━━━━━━━ RISK METRICS ━━━━━━━

📦 VOLUME
┃ Buy side:  {opp['buy_vol']:.4f} (~${opp['buy_vol'] * opp['buy_price']:.0f})
┃ Sell side: {opp['sell_vol']:.4f} (~${opp['sell_vol'] * opp['sell_price']:.0f})
┃ Est. slippage: {slippage_est}{slippage_warning}

⚡ SPEED
┃ Data age: {opp['latency_ms']:.1f}ms
┃ Status: {'🟢 Fresh' if opp['latency_ms'] < 100 else '🟡 OK' if opp['latency_ms'] < 300 else '🔴 Stale'}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
⏰ {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
🤖 Mode: {'🔴 LIVE TRADING' if ENABLE_TRADING else '👁️ SCAN ONLY'}
"""
        try:
            await self.bot.send_message(chat_id=CHAT_ID, text=message)
        except Exception as e:
            print(f"Telegram error: {e}")

    async def start(self):
        """Start the bot"""
        self.running = True
        self.stats["start_time"] = datetime.now()
        
        print("=" * 60)
        print("🚀 PRO ARBITRAGE BOT - Ultra Low Latency")
        print("=" * 60)
        print(f"📊 Symbols: {len(SYMBOLS)}")
        print(f"💰 Trade Size: ${TRADE_AMOUNT_USDT}")
        print(f"🎯 Min Profit: {MIN_PROFIT_PCT * 100:.3f}%")
        print(f"⚡ Mode: {'LIVE TRADING' if ENABLE_TRADING else 'SCAN ONLY'}")
        print("=" * 60)
        
        await self.init_exchanges()
        
        # Start WebSocket watchers for all symbols on all exchanges
        tasks = []
        for exchange_name in self.exchanges:
            for symbol in SYMBOLS:
                tasks.append(
                    asyncio.create_task(self.watch_orderbook(exchange_name, symbol))
                )
        
        # Add the scanner task
        tasks.append(asyncio.create_task(self.arbitrage_scanner()))
        
        # Send startup notification
        if self.bot:
            try:
                await self.bot.send_message(
                    chat_id=CHAT_ID,
                    text=f"🚀 PRO BOT STARTED\n{len(self.exchanges)} exchanges\n{len(SYMBOLS)} symbols\nMode: {'LIVE' if ENABLE_TRADING else 'SCAN'}"
                )
            except:
                pass
        
        print(f"\n🔥 Watching {len(SYMBOLS)} symbols across {len(self.exchanges)} exchanges")
        print("=" * 60)
        print()
        
        # Wait for all tasks
        try:
            await asyncio.gather(*tasks)
        except asyncio.CancelledError:
            pass
        finally:
            await self.close()

    async def close(self):
        """Close all connections"""
        self.running = False
        print("\n\n🛑 Shutting down...")
        
        for name, exchange in self.exchanges.items():
            try:
                await exchange.close()
            except:
                pass
        
        print("👋 Bot stopped")


async def main():
    bot = ProArbitrageBot()
    
    try:
        await bot.start()
    except KeyboardInterrupt:
        await bot.close()


if __name__ == "__main__":
    print("\n🔐 Loading Pro Arbitrage Bot...")
    print("📡 Using WebSocket for real-time prices (sub-100ms latency)\n")
    
    asyncio.run(main())
