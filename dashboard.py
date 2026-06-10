import asyncio
import json
from aiohttp import web
from pro_bot import ProArbitrageBot
from datetime import datetime

HTML = """
<!doctype html>
<html lang="en" class="dark">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Pro Arbitrage Bot - Dashboard</title>
  <script src="https://cdn.tailwindcss.com"></script>
  <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
  <script>
    tailwind.config = {
      darkMode: 'class',
      theme: {
        extend: {
          colors: {
            dark: '#0f172a',
            darker: '#020617',
            card: '#1e293b',
            primary: '#3b82f6',
            success: '#22c55e',
            danger: '#ef4444',
            warning: '#eab308'
          }
        }
      }
    }
  </script>
  <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet" />
  <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    body { background-color: #020617; color: #f8fafc; font-family: 'Inter', sans-serif; }
    .glass-card { background: rgba(30, 41, 59, 0.7); backdrop-filter: blur(10px); border: 1px solid rgba(255,255,255,0.1); border-radius: 1rem; }
    .pulse-green { animation: pulse-green 2s infinite; }
    .pulse-red { animation: pulse-red 2s infinite; }
    @keyframes pulse-green {
      0% { box-shadow: 0 0 0 0 rgba(34, 197, 94, 0.7); }
      70% { box-shadow: 0 0 0 10px rgba(34, 197, 94, 0); }
      100% { box-shadow: 0 0 0 0 rgba(34, 197, 94, 0); }
    }
    @keyframes pulse-red {
      0% { box-shadow: 0 0 0 0 rgba(239, 68, 68, 0.7); }
      70% { box-shadow: 0 0 0 10px rgba(239, 68, 68, 0); }
      100% { box-shadow: 0 0 0 0 rgba(239, 68, 68, 0); }
    }
    ::-webkit-scrollbar { width: 8px; height: 8px; }
    ::-webkit-scrollbar-track { background: #0f172a; }
    ::-webkit-scrollbar-thumb { background: #334155; border-radius: 4px; }
    ::-webkit-scrollbar-thumb:hover { background: #475569; }
  </style>
</head>
<body class="min-h-screen p-4 md:p-8">
  <div class="max-w-7xl mx-auto space-y-6">
    
    <!-- Header -->
    <header class="flex flex-col md:flex-row justify-between items-center glass-card p-6">
      <div class="flex items-center space-x-4">
        <div class="w-12 h-12 rounded-full bg-primary/20 flex items-center justify-center text-primary text-2xl">
          <i class="fa-solid fa-robot"></i>
        </div>
        <div>
          <h1 class="text-2xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-blue-400 to-purple-500">Pro Arbitrage Bot</h1>
          <p class="text-sm text-gray-400">Ultra Low Latency Scanner</p>
        </div>
      </div>
      <div class="mt-4 md:mt-0 flex items-center space-x-3 px-4 py-2 rounded-full bg-dark border border-gray-700">
        <div id="status-indicator" class="w-3 h-3 rounded-full bg-danger pulse-red"></div>
        <span id="status-text" class="text-sm font-medium text-gray-300">Disconnected</span>
      </div>
    </header>

    <!-- Stats Row -->
    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
      <div class="glass-card p-6 flex flex-col justify-between">
        <div class="flex justify-between items-start">
          <div>
            <p class="text-gray-400 text-sm font-medium">Total Scans</p>
            <h3 id="val-scans" class="text-3xl font-bold mt-1">0</h3>
          </div>
          <div class="p-3 rounded-lg bg-blue-500/10 text-blue-400">
            <i class="fa-solid fa-satellite-dish"></i>
          </div>
        </div>
      </div>

      <div class="glass-card p-6 flex flex-col justify-between">
        <div class="flex justify-between items-start">
          <div>
            <p class="text-gray-400 text-sm font-medium">Avg Latency</p>
            <h3 class="text-3xl font-bold mt-1 flex items-baseline gap-1">
              <span id="val-latency">0.00</span>
              <span class="text-sm text-gray-500 font-normal">ms</span>
            </h3>
          </div>
          <div class="p-3 rounded-lg bg-purple-500/10 text-purple-400">
            <i class="fa-solid fa-bolt"></i>
          </div>
        </div>
      </div>

      <div class="glass-card p-6 flex flex-col justify-between">
        <div class="flex justify-between items-start">
          <div>
            <p class="text-gray-400 text-sm font-medium">Best Profit</p>
            <h3 class="text-3xl font-bold mt-1 text-success flex items-baseline gap-1">
              <span id="val-profit">0.00</span>
              <span class="text-sm text-gray-500 font-normal">%</span>
            </h3>
          </div>
          <div class="p-3 rounded-lg bg-green-500/10 text-green-400">
            <i class="fa-solid fa-arrow-trend-up"></i>
          </div>
        </div>
      </div>

      <div class="glass-card p-6 flex flex-col justify-between">
        <div class="flex justify-between items-start">
          <div>
            <p class="text-gray-400 text-sm font-medium">Opportunities Found</p>
            <h3 id="val-opps" class="text-3xl font-bold mt-1 text-warning">0</h3>
          </div>
          <div class="p-3 rounded-lg bg-yellow-500/10 text-yellow-400">
            <i class="fa-solid fa-star"></i>
          </div>
        </div>
      </div>
    </div>

    <!-- Charts Row -->
    <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
      <div class="glass-card p-6">
        <h3 class="text-lg font-semibold mb-4 text-gray-200">Scanner Latency (ms)</h3>
        <div class="h-64">
          <canvas id="latencyChart"></canvas>
        </div>
      </div>
      <div class="glass-card p-6">
        <h3 class="text-lg font-semibold mb-4 text-gray-200">Best Profit (%)</h3>
        <div class="h-64">
          <canvas id="profitChart"></canvas>
        </div>
      </div>
    </div>

    <!-- Opportunities Table -->
    <div class="glass-card p-6 overflow-hidden flex flex-col">
      <div class="flex justify-between items-center mb-4">
        <h3 class="text-lg font-semibold text-gray-200">Recent Opportunities</h3>
        <span class="text-xs py-1 px-2 rounded-full bg-gray-800 text-gray-400 border border-gray-700">Live Updates</span>
      </div>
      <div class="overflow-x-auto">
        <table class="w-full text-left border-collapse">
          <thead>
            <tr class="border-b border-gray-700 text-sm text-gray-400">
              <th class="py-3 px-4 font-medium">Time</th>
              <th class="py-3 px-4 font-medium">Symbol</th>
              <th class="py-3 px-4 font-medium">Route</th>
              <th class="py-3 px-4 font-medium">Buy</th>
              <th class="py-3 px-4 font-medium">Sell</th>
              <th class="py-3 px-4 font-medium text-right">Net Profit</th>
              <th class="py-3 px-4 font-medium text-right">Profit USDT</th>
            </tr>
          </thead>
          <tbody id="opps-table-body" class="text-sm">
            <!-- Rows will be added here -->
          </tbody>
        </table>
      </div>
    </div>

  </div>

  <script>
    // --- Chart Setup ---
    Chart.defaults.color = '#94a3b8';
    Chart.defaults.font.family = 'Inter';
    
    const commonOptions = {
      responsive: true,
      maintainAspectRatio: false,
      animation: { duration: 0 },
      plugins: { legend: { display: false } },
      scales: {
        x: { display: false },
        y: { 
          grid: { color: 'rgba(255, 255, 255, 0.05)' },
          border: { display: false }
        }
      },
      elements: {
        point: { radius: 0, hitRadius: 10, hoverRadius: 4 }
      }
    };

    const latencyCtx = document.getElementById('latencyChart').getContext('2d');
    const latencyChart = new Chart(latencyCtx, {
      type: 'line',
      data: {
        labels: [],
        datasets: [{
          data: [],
          borderColor: '#a855f7',
          backgroundColor: 'rgba(168, 85, 247, 0.1)',
          borderWidth: 2,
          fill: true,
          tension: 0.4
        }]
      },
      options: { ...commonOptions, scales: { ...commonOptions.scales, y: { ...commonOptions.scales.y, min: 0 } } }
    });

    const profitCtx = document.getElementById('profitChart').getContext('2d');
    const profitChart = new Chart(profitCtx, {
      type: 'line',
      data: {
        labels: [],
        datasets: [{
          data: [],
          borderColor: '#22c55e',
          backgroundColor: 'rgba(34, 197, 94, 0.1)',
          borderWidth: 2,
          fill: true,
          tension: 0.4
        }]
      },
      options: commonOptions
    });

    // Data history
    const MAX_DATA_POINTS = 50;

    function addData(chart, label, data) {
      chart.data.labels.push(label);
      chart.data.datasets[0].data.push(data);
      if (chart.data.labels.length > MAX_DATA_POINTS) {
        chart.data.labels.shift();
        chart.data.datasets[0].data.shift();
      }
      chart.update();
    }

    // --- WebSocket Logic ---
    const statusIndicator = document.getElementById('status-indicator');
    const statusText = document.getElementById('status-text');
    
    const valScans = document.getElementById('val-scans');
    const valLatency = document.getElementById('val-latency');
    const valProfit = document.getElementById('val-profit');
    const valOpps = document.getElementById('val-opps');
    const oppsTableBody = document.getElementById('opps-table-body');

    function connect() {
      const wsUrl = (location.protocol === 'https:' ? 'wss://' : 'ws://') + location.host + '/ws';
      const ws = new WebSocket(wsUrl);
      
      ws.onopen = () => {
        statusIndicator.className = 'w-3 h-3 rounded-full bg-success pulse-green';
        statusText.textContent = 'Connected';
        statusText.className = 'text-sm font-medium text-success';
      };
      
      ws.onclose = () => {
        statusIndicator.className = 'w-3 h-3 rounded-full bg-danger pulse-red';
        statusText.textContent = 'Disconnected (reconnecting...)';
        statusText.className = 'text-sm font-medium text-danger';
        setTimeout(connect, 3000);
      };
      
      let lastStatsUpdate = 0;

      ws.onmessage = (e) => {
        try {
          const msg = JSON.parse(e.data);
          
          if (msg.type === 'stats') {
            valScans.textContent = msg.scan_count.toLocaleString();
            valLatency.textContent = msg.avg_latency.toFixed(2);
            valProfit.textContent = msg.best_profit.toFixed(4);
            valOpps.textContent = msg.opportunities.toLocaleString();
            
            // Throttle chart updates to max 2x per second
            const now = Date.now();
            if (now - lastStatsUpdate > 500) {
              const timeStr = new Date().toLocaleTimeString();
              addData(latencyChart, timeStr, msg.avg_latency);
              addData(profitChart, timeStr, msg.best_profit);
              lastStatsUpdate = now;
            }
          } else if (msg.type === 'opportunity') {
            const opp = msg.opp;
            const now = new Date();
            const timeStr = now.toLocaleTimeString([], { hour12: false }) + '.' + now.getMilliseconds().toString().padStart(3, '0');
            
            const tr = document.createElement('tr');
            tr.className = 'border-b border-gray-800 hover:bg-gray-800/50 transition-colors animate-fade-in';
            tr.innerHTML = `
              <td class="py-3 px-4 text-gray-400 whitespace-nowrap">${timeStr}</td>
              <td class="py-3 px-4 font-bold text-white">${opp.symbol}</td>
              <td class="py-3 px-4">
                <div class="flex items-center space-x-2">
                  <span class="px-2 py-1 bg-blue-500/20 text-blue-400 rounded text-xs">${opp.buy_exchange}</span>
                  <i class="fa-solid fa-arrow-right text-gray-500 text-xs"></i>
                  <span class="px-2 py-1 bg-purple-500/20 text-purple-400 rounded text-xs">${opp.sell_exchange}</span>
                </div>
              </td>
              <td class="py-3 px-4 text-gray-300">$${parseFloat(opp.buy_price).toFixed(6)}</td>
              <td class="py-3 px-4 text-gray-300">$${parseFloat(opp.sell_price).toFixed(6)}</td>
              <td class="py-3 px-4 text-right font-bold text-success">+${opp.net_profit.toFixed(4)}%</td>
              <td class="py-3 px-4 text-right text-success">+$${opp.profit_usdt.toFixed(2)}</td>
            `;
            
            oppsTableBody.insertBefore(tr, oppsTableBody.firstChild);
            
            // Keep only last 50 rows
            while (oppsTableBody.children.length > 50) {
              oppsTableBody.removeChild(oppsTableBody.lastChild);
            }
          }
        } catch (err) {
          console.error('WS Parse Error', err);
        }
      };
    }
    
    // Inject CSS for fade-in animation
    const style = document.createElement('style');
    style.textContent = `
      @keyframes fadeIn { from { opacity: 0; transform: translateY(-10px); background: rgba(34, 197, 94, 0.2); } to { opacity: 1; transform: translateY(0); background: transparent; } }
      .animate-fade-in { animation: fadeIn 0.5s ease-out forwards; }
    `;
    document.head.appendChild(style);

    connect();
  </script>
</body>
</html>
"""


async def websocket_handler(request):
    ws = web.WebSocketResponse()
    await ws.prepare(request)
    request.app['clients'].add(ws)
    try:
        async for msg in ws:
            # keep the connection alive; ignore incoming messages
            pass
    finally:
        request.app['clients'].discard(ws)
    return ws


async def index(request):
    return web.Response(text=HTML, content_type='text/html')


async def broadcast_events(app):
    bot: ProArbitrageBot = app['bot']
    clients = app['clients']
    if not getattr(bot, 'event_queue', None):
        print('⚠️  Bot has no event_queue; dashboard will show no live events')
        return

    while True:
        try:
            event = await bot.event_queue.get()
            data = json.dumps(event, default=str)
            to_remove = set()
            for ws in set(clients):
                try:
                    await ws.send_str(data)
                except Exception:
                    to_remove.add(ws)
            for ws in to_remove:
                clients.discard(ws)
        except asyncio.CancelledError:
            break
        except Exception:
            await asyncio.sleep(0.1)


async def start_bot_and_server():
    app = web.Application()
    app['clients'] = set()

    # Create bot instance and attach
    bot = ProArbitrageBot()
    app['bot'] = bot

    app.router.add_get('/', index)
    app.router.add_get('/ws', websocket_handler)

    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, '0.0.0.0', 8080)
    await site.start()

    print('🌐 Dashboard running on http://localhost:8080')

    # Start bot in background
    bot_task = asyncio.create_task(bot.start())

    # Start broadcaster
    bcast_task = asyncio.create_task(broadcast_events(app))

    try:
        await asyncio.gather(bot_task, bcast_task)
    except asyncio.CancelledError:
        pass
    finally:
        await bot.close()
        await runner.cleanup()


def main():
    try:
        asyncio.run(start_bot_and_server())
    except KeyboardInterrupt:
        print('\nShutting down')


if __name__ == '__main__':
    main()
