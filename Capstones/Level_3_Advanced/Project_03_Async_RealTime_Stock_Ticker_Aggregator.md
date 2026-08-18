# Capstone Project 3.3: Async Real-Time Market Ticker Stream

## 📌 Project Overview
Build a high-throughput **Asynchronous Financial Market Data Stream & Technical Indicator Engine**. The application simulates real-time price feeds for multiple equities across mock exchange sockets, aggregates thousands of price ticks per second using non-blocking `asyncio` streams, calculates rolling quantitative indicators (Moving Averages, RSI, Bollinger Bands) over sliding window ring buffers, and broadcasts trade alerts.

---

## 🎯 Learning Objectives
- **AsyncIO Concurrency**: Structuring asynchronous applications with `asyncio.TaskGroup`, `asyncio.Queue`, and `asyncio.gather`.
- **Producer-Consumer Architecture**: Managing backpressure between fast market data producers and slower analytics consumers.
- **Sliding Window Data Structures**: Implementing efficient fixed-size circular ring buffers (`collections.deque(maxlen=N)`) for constant-time $O(1)$ statistical updates.
- **Async Synchronization**: Coordinating concurrent access using `asyncio.Lock` and `asyncio.Event`.
- **Resilience & Reconnection**: Handling simulated socket dropouts with asynchronous exponential backoff and circuit breakers.

---

## 🏗️ System Architecture

```text
  [ Mock Exchange A ]       [ Mock Exchange B ]       [ Mock Exchange C ]
  (Async Socket Stream)     (Async Socket Stream)     (Async Socket Stream)
           |                         |                         |
           +-------------------------+-------------------------+
                                     |
                                     v
                        [ Ingestion Queue (asyncio) ]
                                     |
                                     v
                        [ Market Stream Aggregator ]
                                     |
                                     +-------------------+
                                     |                   |
                                     v                   v
                     [ Rolling Metric Calculator ]   [ Alert Dispatcher ]
                     - EMA (Exponential Average)     - Golden Cross (SMA)
                     - RSI (Relative Strength)       - Volatility Spikes
                     - Bollinger Bands ($2\sigma$)   - Push to subscribers
```

---

## 📋 Functional Requirements

### 1. Market Tick Model & Exchange Ingestion
- `Tick`: `symbol: str`, `price: float`, `volume: int`, `timestamp: float`, `exchange: str`.
- Simulate 5 concurrent exchanges streaming ticks asynchronously at randomized intervals (10ms to 50ms) using `asyncio.sleep()`.

### 2. Rolling Technical Indicator Calculator
Maintain a sliding window for each equity symbol (e.g. `AAPL`, `MSFT`, `GOOGL`, `BTC-USD`, `ETH-USD`):
- **Simple Moving Average (SMA-20, SMA-50)**: Rolling arithmetic average of the last $N$ closing prices.
- **Exponential Moving Average (EMA-12, EMA-26)**:
  $$\text{EMA}_t = (\text{Price}_t \times \alpha) + (\text{EMA}_{t-1} \times (1 - \alpha)), \quad \alpha = \frac{2}{N + 1}$$
- **Relative Strength Index (RSI-14)**:
  $$\text{RS} = \frac{\text{Average Gain}}{\text{Average Loss}}, \quad \text{RSI} = 100 - \left(\frac{100}{1 + \text{RS}}\right)$$
  Flag **Overbought** ($\text{RSI} \ge 70$) and **Oversold** ($\text{RSI} \le 30$) conditions.
- **Bollinger Bands ($20, 2\sigma$)**: Upper Band = $\text{SMA}_{20} + 2\sigma$, Lower Band = $\text{SMA}_{20} - 2\sigma$.

### 3. Backpressure & Queue Management
- Ingestion queue with bounded capacity (`maxsize=1000`).
- If the queue exceeds 80% capacity, trigger warning logs and apply rate-limiting to prevent memory exhaustion.

### 4. Live Terminal Dashboard
An asynchronous console loop rendering updated market summaries every 500ms using ANSI cursor positioning (updating ticker prices, daily highs/lows, moving averages, and alert notifications).

---

## 📐 Phased Implementation Guide

### Phase 1: Tick Data Class & Rolling Buffer
```python
from dataclasses import dataclass
from collections import deque
import statistics
import time

@dataclass(frozen=True)
class Tick:
    symbol: str
    price: float
    volume: int
    timestamp: float
    exchange: str

class TickerWindow:
    def __init__(self, symbol: str, window_size: int = 50):
        self.symbol = symbol
        self.prices = deque(maxlen=window_size)
        self.last_ema_12 = None

    def add_tick(self, tick: Tick) -> None:
        self.prices.append(tick.price)
        # Update EMA
        k = 2 / (12 + 1)
        if self.last_ema_12 is None:
            self.last_ema_12 = tick.price
        else:
            self.last_ema_12 = (tick.price * k) + (self.last_ema_12 * (1 - k))

    def get_sma(self, period: int = 20) -> float:
        if len(self.prices) < period:
            return 0.0
        subset = list(self.prices)[-period:]
        return sum(subset) / period
```

### Phase 2: Async Producer-Consumer Ingestion Pipeline
```python
import asyncio

async def exchange_stream_producer(exchange_name: str, symbols: list[str], queue: asyncio.Queue):
    import random
    prices = {s: random.uniform(100.0, 500.0) for s in symbols}
    while True:
        symbol = random.choice(symbols)
        # Random walk price shift
        delta = random.uniform(-0.5, 0.5)
        prices[symbol] = max(1.0, prices[symbol] + delta)
        
        tick = Tick(symbol=symbol, price=round(prices[symbol], 2), volume=random.randint(10, 500), timestamp=time.time(), exchange=exchange_name)
        await queue.put(tick)
        await asyncio.sleep(random.uniform(0.01, 0.05))
```

### Phase 3: Analytics Worker & Alert Engine
Consume from queue, update sliding windows, and dispatch signal events.

---

## 🧪 Verification Matrix & Edge Cases

| Scenario | Input / Action | Expected Behavior |
| :--- | :--- | :--- |
| **Rapid Burst Ingestion** | Ingest 5,000 ticks in 100ms | Queue buffers ticks without drops; metrics calculate accurately |
| **Insufficient Data** | Query 50-period SMA when only 10 ticks exist | Returns default/placeholder value without crashing with `ZeroDivisionError` |
| **RSI Overbought Alert** | Simulate 15 consecutive positive price increases | Correctly computes $\text{RSI} > 70$ and fires `OVERBOUGHT` alert event |
| **Graceful Async Cancellation** | Send `Ctrl+C` interrupt | Closes queues, cancels background producers, prints summary report |

---

## 🚀 Bonus Challenges
- **Real WebSocket Integration**: Connect to real public crypto feeds (e.g. Coinbase / Binance public WebSocket API) using `aiohttp` or `websockets`.
- **Order Book Depth Simulator**: Track Bid/Ask Order Book depth levels with order matching engine.
