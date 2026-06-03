"""
SIMULATION_HARNESS.py
Realistic backtest that mimics live trading behavior
Includes market microstructure, slippage, and realistic order flow
"""

import asyncio
import json
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
from typing import List, Dict, Tuple
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)
logger = logging.getLogger("SimulationHarness")


class RealisticMarketSimulator:
    """
    Simulate realistic market conditions:
    - Price microstructure (bid-ask spread)
    - Order slippage (partial fill, price impact)
    - Market regime changes
    - Realistic order book dynamics
    """
    
    def __init__(self, initial_price: float = 47000, volatility: float = 0.015, spread_bps: float = 2):
        self.price = initial_price
        self.volatility = volatility  # 1.5% typical daily vol
        self.spread_bps = spread_bps  # 2 bps bid-ask on BTC
        
        self.bid = self.price * (1 - spread_bps / 10000)
        self.ask = self.price * (1 + spread_bps / 10000)
        
        self.price_history = [self.price]
        self.order_book_imbalance = 0.0  # -1 = all sells, 0 = neutral, 1 = all buys
    
    def generate_tick(self) -> Dict:
        """Generate one 5-second price tick"""
        # Geometric brownian motion with mean reversion
        drift = 0.0
        shock = np.random.normal(0, self.volatility / np.sqrt(250 * 24 * 12))  # ~5-sec intervals in day
        
        self.price *= np.exp(drift + shock)
        
        # Order book imbalance changes slowly
        self.order_book_imbalance += np.random.normal(0, 0.05)
        self.order_book_imbalance = np.clip(self.order_book_imbalance, -1, 1)
        
        # Spread widens during high volume
        volume_effect = abs(self.order_book_imbalance) * 0.5
        spread = self.spread_bps * (1 + volume_effect)
        
        self.bid = self.price * (1 - spread / 10000)
        self.ask = self.price * (1 + spread / 10000)
        
        self.price_history.append(self.price)
        
        return {
            "timestamp": len(self.price_history),
            "mid_price": self.price,
            "bid": self.bid,
            "ask": self.ask,
            "bid_ask_spread_bps": (self.ask - self.bid) / self.price * 10000,
            "imbalance": self.order_book_imbalance
        }
    
    def execute_market_order(self, direction: int, size: float) -> Tuple[float, float]:
        """
        Execute market order, accounting for slippage
        
        Returns: (execution_price, slippage_bps)
        """
        if direction > 0:  # Buy
            # Buy orders hit the ask, with slippage for larger orders
            slippage_factor = 1 + (size / 100000) * 0.01  # 1% slippage per $100k
            execution_price = self.ask * slippage_factor
            slippage_bps = (execution_price - self.price) / self.price * 10000
        else:  # Sell
            # Sell orders hit the bid, with slippage
            slippage_factor = 1 - (size / 100000) * 0.01
            execution_price = self.bid * slippage_factor
            slippage_bps = (self.price - execution_price) / self.price * 10000
        
        return execution_price, slippage_bps


class AdvancedSimulationHarness:
    """
    Run bot on realistic simulated market
    Includes:
    - Real price microstructure
    - Slippage + execution costs
    - Market regimes (trending, mean-revert, volatile)
    - Equity curve + Sharpe + max drawdown
    - Trade-by-trade PnL analysis
    """
    
    def __init__(self, initial_equity: float = 10000, kelly_cap: float = 0.5):
        self.initial_equity = initial_equity
        self.equity = initial_equity
        self.kelly_cap = kelly_cap
        
        self.market = RealisticMarketSimulator()
        self.trades = []
        self.equity_history = [initial_equity]
        self.price_history = [self.market.price]
        
        self.total_slippage = 0
        self.total_commissions = 0
    
    def kelly_size(self, confidence: float, edge: float = 0.05) -> float:
        """Kelly criterion with realistic edge"""
        b = 1.0
        p = (confidence + edge) / 2
        q = 1 - p
        f = (b * p - q) / b if b > 0 else 0
        return float(np.clip(f, 0, self.kelly_cap))
    
    def generate_signal(self, price_change_pct: float, volatility_regime: str) -> Tuple[int, float]:
        """Generate trading signal based on price + regime"""
        
        # Bias from momentum
        bias = 0.55 + price_change_pct * 10
        bias = np.clip(bias, 0.3, 0.8)
        
        # Confidence from regime
        if volatility_regime == "trending":
            confidence_boost = 0.15
        elif volatility_regime == "volatile":
            confidence_boost = -0.10
        else:
            confidence_boost = 0.0
        
        confidence = 0.6 + abs(price_change_pct) * 20 + confidence_boost
        confidence = np.clip(confidence, 0.5, 0.95)
        
        direction = 1 if bias > 0.5 else -1
        return direction, confidence
    
    def determine_regime(self, recent_returns: np.ndarray) -> str:
        """Classify market regime"""
        vol = np.std(recent_returns)
        momentum = np.mean(recent_returns[-5:]) if len(recent_returns) >= 5 else 0
        
        if vol > 0.01:
            return "volatile"
        elif abs(momentum) > 0.001:
            return "trending"
        else:
            return "mean_revert"
    
    def run_simulation(self, num_ticks: int = 1000, trade_frequency: float = 0.2) -> Dict:
        """
        Run 1000+ ticks (~ 1-2 hours of market data)
        Simulate 200+ trading decisions
        """
        logger.info(f"🎬 Simulation starting: {num_ticks} ticks")
        
        recent_prices = []
        
        for tick in range(num_ticks):
            tick_data = self.market.generate_tick()
            current_price = tick_data["mid_price"]
            recent_prices.append(current_price)
            self.price_history.append(current_price)
            
            # Keep last 20 for trend detection
            if len(recent_prices) > 20:
                recent_prices.pop(0)
            
            # Determine regime every 10 ticks
            if tick % 10 == 0 and len(recent_prices) >= 10:
                returns = np.diff(recent_prices) / recent_prices[:-1]
                regime = self.determine_regime(returns)
            else:
                regime = "mean_revert"
            
            # Decide to trade
            if np.random.random() < trade_frequency:
                prev_price = recent_prices[-2] if len(recent_prices) >= 2 else current_price
                price_change = (current_price - prev_price) / prev_price
                
                direction, confidence = self.generate_signal(price_change, regime)
                
                # JOMO: only trade on high confidence
                if confidence > 0.75:
                    size = self.kelly_size(confidence) * self.equity
                    
                    # Execute with slippage
                    execution_price, slippage_bps = self.market.execute_market_order(direction, size)
                    
                    # Commission (0.1%)
                    commission = size * 0.001
                    self.total_commissions += commission
                    
                    # Hold for 5-20 ticks
                    exit_tick = min(tick + np.random.randint(5, 20), num_ticks - 1)
                    exit_price = self.price_history[-1 + (exit_tick - tick)]
                    
                    # Calculate PnL
                    if direction > 0:
                        pnl = size * (exit_price - execution_price) / execution_price - commission
                    else:
                        pnl = size * (execution_price - exit_price) / execution_price - commission
                    
                    self.equity += pnl
                    
                    self.trades.append({
                        "tick": tick,
                        "entry_price": execution_price,
                        "exit_price": exit_price,
                        "direction": direction,
                        "size": size,
                        "confidence": confidence,
                        "regime": regime,
                        "slippage_bps": slippage_bps,
                        "commission": commission,
                        "pnl": pnl,
                        "pnl_pct": pnl / (size + commission) if (size + commission) > 0 else 0
                    })
                    
                    logger.info(f"  Tick {tick} | {direction:+1} | Conf: {confidence:.2f} | PnL: ${pnl:+.2f}")
            
            self.equity_history.append(self.equity)
            
            if (tick + 1) % 100 == 0:
                logger.info(f"  [{tick+1}/{num_ticks}] Equity: ${self.equity:.2f} | Trades: {len(self.trades)}")
        
        return self.compute_metrics()
    
    def compute_metrics(self) -> Dict:
        """Detailed performance analysis"""
        equity_hist = np.array(self.equity_history)
        returns = np.diff(equity_hist) / equity_hist[:-1]
        
        trades = self.trades
        if len(trades) == 0:
            return {
                "trades": 0,
                "win_rate": 0,
                "avg_win": 0,
                "avg_loss": 0,
                "profit_factor": 0,
                "total_return": 0,
                "sharpe": 0,
                "max_drawdown": 0,
                "final_equity": self.equity,
                "total_slippage": self.total_slippage,
                "total_commissions": self.total_commissions
            }
        
        pnls = [t["pnl"] for t in trades]
        wins = [p for p in pnls if p > 0]
        losses = [p for p in pnls if p < 0]
        
        profit_factor = sum(wins) / abs(sum(losses)) if losses else 0
        
        sharpe = np.mean(returns) / np.std(returns) * np.sqrt(250 * 288) if np.std(returns) > 0 else 0  # 5-sec ticks
        
        cummax = np.maximum.accumulate(equity_hist)
        drawdown = (equity_hist - cummax) / cummax
        max_dd = np.min(drawdown) if len(drawdown) > 0 else 0
        
        return {
            "trades": len(trades),
            "win_rate": len(wins) / len(trades) if trades else 0,
            "wins": len(wins),
            "losses": len(losses),
            "avg_win": np.mean(wins) if wins else 0,
            "avg_loss": np.mean(losses) if losses else 0,
            "profit_factor": float(profit_factor),
            "total_pnl": sum(pnls),
            "total_return": (self.equity - self.initial_equity) / self.initial_equity,
            "sharpe": float(sharpe),
            "max_drawdown": float(max_dd),
            "final_equity": self.equity,
            "total_slippage_usd": self.total_slippage,
            "total_commissions": self.total_commissions,
            "sample_trades": trades[:10]
        }


async def main():
    """Run advanced simulation"""
    print("🎬 Advanced Simulation Harness")
    print("=" * 60)
    
    harness = AdvancedSimulationHarness(initial_equity=10000, kelly_cap=0.5)
    
    print("\n📊 Running 1000+ tick simulation (realistic market microstructure)...\n")
    metrics = harness.run_simulation(num_ticks=1000, trade_frequency=0.2)
    
    print("\n" + "=" * 60)
    print("📈 SIMULATION RESULTS")
    print("=" * 60)
    print(f"Trades: {metrics['trades']}")
    print(f"Win Rate: {metrics['win_rate']:.1%}")
    print(f"Wins: {metrics['wins']} | Losses: {metrics['losses']}")
    print(f"Avg Win: ${metrics['avg_win']:.2f} | Avg Loss: ${metrics['avg_loss']:.2f}")
    print(f"Profit Factor: {metrics['profit_factor']:.2f}x")
    print(f"\nTotal PnL: ${metrics['total_pnl']:.2f}")
    print(f"Total Return: {metrics['total_return']:.2%}")
    print(f"Final Equity: ${metrics['final_equity']:.2f}")
    print(f"\nSharpe Ratio: {metrics['sharpe']:.2f}")
    print(f"Max Drawdown: {metrics['max_drawdown']:.2%}")
    print(f"\nTotal Slippage: ${metrics['total_slippage_usd']:.2f}")
    print(f"Total Commissions: ${metrics['total_commissions']:.2f}")
    
    # Save results
    with open("simulation_results.json", "w") as f:
        json.dump(metrics, f, indent=2)
    
    print("\n✅ Results saved to simulation_results.json")


if __name__ == "__main__":
    asyncio.run(main())
