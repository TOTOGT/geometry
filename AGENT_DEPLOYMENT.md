# Kelly JOMO Claude Agent Deployment

**Autonomous trading agent** powered by Claude 3.5 Sonnet + topological protection.

## 🚀 Quick Start

### 1. Set up environment
```bash
cp .env.example .env
# Edit .env with your API keys:
# - ANTHROPIC_API_KEY
# - POLYMARKET_API_KEY (optional)
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Run locally
```bash
# Single agent cycle
python agents/kelly_jomo_agent.py

# Or with custom cycles
TOTAL_CYCLES=10 python agents/kelly_jomo_agent.py
```

### 4. View dashboard
```bash
streamlit run dashboard/kelly_jomo_dashboard.py
```

---

## 📊 Architecture

### Core Components

#### `kelly_jomo_agent.py`
- **TopologicalOrthogenesisBot**: Anyon chain simulation + Kelly criterion
- **LiveDataAdapter**: Fetch BTC prices (Kraken) + Polymarket order books
- **KellyJOMOClaudeAgent**: Claude orchestration + autonomous decision-making

#### `dashboard/kelly_jomo_dashboard.py`
- Real-time equity curve + PnL tracking
- Braid word visualization (protected trade history)
- Coherence field heatmap
- Trade log + confidence distribution

### Trading Logic

```
C (Contact) → Ingest BTC price + market signal
    ↓
K (Conjugate) → Run topological cascade (K-crossing validation)
    ↓
F (Fixed Point) → Fuse anyons → compute confidence
    ↓
Claude Decision → Validate with LLM reasoning
    ↓
U (Unification) → Execute via Polymarket API if confidence > 0.75
```

**JOMO Principle**: Default to inaction. Only trade when:
1. K-crossing detected (coherence jump > threshold)
2. Confidence > 0.75
3. Kelly sizing ≤ 50% of equity
4. Claude approves reasoning

---

## 🔧 Configuration

Edit `.env`:

```bash
# API Keys
ANTHROPIC_API_KEY=sk-ant-...
POLYMARKET_API_KEY=...

# Bot Parameters
BOT_N_SITES=24              # Anyon chain length
BOT_K_THRESHOLD=0.28        # Coherence jump threshold
BOT_KELLY_CAP=0.5           # Max position size

# Execution
CYCLE_INTERVAL_SECONDS=300  # 5 min between cycles
TOTAL_CYCLES=0              # 0 = infinite
SIMULATION_MODE=true        # Demo mode (no real orders)
```

---

## 📈 Production Deployment

### GitHub Actions
The workflow in `.github/workflows/deploy-claude-agent.yml`:
- Runs on every push to `claude-agent-deployment` branch
- Spins up agent for N cycles
- Streams logs to artifacts
- Optionally deploys dashboard

### Docker (optional)
```bash
docker build -t kelly-jomo-agent .
docker run -e ANTHROPIC_API_KEY=$ANTHROPIC_API_KEY kelly-jomo-agent
```

### Cloud (Vercel / Railway / Heroku)
```bash
git push origin claude-agent-deployment
# CI/CD triggers deployment
```

---

## 📖 Example Output

```
==========================================
Starting Kelly JOMO autonomous cycle...
BTC Price: $47,284.30 | Market Bias: 0.68
✅ PROTECTED SIGNAL | Dir: 1 | Size: $2,400 | Conf: 0.82
Claude decision:
{
  "action": "trade",
  "direction": 1,
  "size_usd": 2400,
  "confidence": 0.82,
  "reasoning": "K-crossing validated. Coherence delta 0.35 > threshold 0.28. Kelly sizing 2.4% of equity. BTC bullish bias 0.68 aligns with directional signal."
}
✅ ORDER EXECUTED: {"order_id": "sim_1717422710.23", "status": "simulated", ...}
Cycle complete | Equity: $47,412.50
```

---

## 🧠 How Claude Makes Decisions

The agent sends Claude:
1. **Current market state** (BTC price, Polymarket bias, signal from cascade)
2. **Bot's equity + recent PnL**
3. **Topological metrics** (coherence, braid complexity)

Claude evaluates:
- ✅ Is the cascade protected? (K-crossing validated)
- ✅ Is confidence > 0.75?
- ✅ Does Kelly sizing respect equity constraints?
- ⚠️ Are there risk flags?

Claude responds with JSON decision: `trade`, `idle`, or `rebalance`.

---

## 🔐 Security & Risk Management

- **Position limit**: Kelly cap (default 50% per trade)
- **Equity floor**: No trades if equity < $100
- **Cascade validation**: Only execute on protected K-crossings
- **Claude supervision**: LLM reviews every decision
- **Simulation mode**: All orders are simulated until POLYMARKET_API_KEY is set
- **Rate limiting**: 1 cycle = 5 min default (prevent over-trading)

---

## 📚 References

**Principia Orthogona Ch. 8**: [The Axiomatic Turn](https://github.com/TOTOGT/geometry/blob/main/ch8-axiomatic.html)

**AXLE Lean 4 Proofs**: [github.com/TOTOGT/AXLE](https://github.com/TOTOGT/AXLE)

**Topological Trading**: Anyon braiding as protection against regime shifts.

---

## ⚠️ Disclaimer

This agent is **experimental**. It uses simulated orders by default. For real trading:
1. Set `POLYMARKET_API_KEY` 
2. Set `SIMULATION_MODE=false`
3. Start with minimal equity
4. Monitor logs constantly
5. Use small position sizes

**No guarantees of profitability. Past performance ≠ future results.**

---

## 🤝 Contributing

- Bug reports / feature requests: GitHub Issues
- Improvements to Claude prompts: Pull requests welcome
- Dashboard enhancements: `dashboard/` directory
- New data adapters: `agents/` directory

---

**G6 LLC · Newark, NJ · 2026**
