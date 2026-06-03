# Kelly JOMO Agent Deployment — Quick Reference

## 🚀 Deploy in 60 seconds

### Step 1: Clone & Setup (30s)
```bash
git clone https://github.com/TOTOGT/geometry.git
cd geometry
git checkout claude-agent-deployment
bash setup.sh
```

### Step 2: Configure (15s)
```bash
nano .env
# Add: ANTHROPIC_API_KEY=sk-ant-[your-key]
# Save & exit
```

### Step 3: Run (15s)
```bash
source venv/bin/activate
python agents/kelly_jomo_agent.py
```

---

## 📊 Monitor Live

In new terminal:
```bash
streamlit run dashboard/kelly_jomo_dashboard.py
```

Open browser → `http://localhost:8501`

---

## 🧪 Test with Backtest

```bash
python tests/backtest.py
```

Shows: win rate, Sharpe ratio, drawdown, equity curve

---

## 🔑 Get API Key (FREE)

1. Visit: https://console.anthropic.com
2. Sign up → create API key
3. Copy to `.env`
4. Go!

---

## 🐳 Docker (prod)

```bash
docker build -t kelly-jomo .
docker run -e ANTHROPIC_API_KEY=$KEY kelly-jomo
```

---

## 📈 What You Get

✅ Autonomous trading with Claude reasoning  
✅ Topological protection (K-crossing validation)  
✅ Kelly criterion position sizing  
✅ Real-time equity + PnL tracking  
✅ Braid visualization (trade history)  
✅ Live Streamlit dashboard  
✅ GitHub Actions CI/CD  
✅ Backtesting suite  

---

## ⚠️ Important

- **Simulation mode by default** (no real money risked)
- Set `POLYMARKET_API_KEY` for live trading
- Start small — test thoroughly
- Monitor logs constantly
- No guarantees — experimental research

---

## 📚 Learn More

- **Ch. 8**: https://github.com/TOTOGT/geometry/blob/main/ch8-axiomatic.html
- **Principia Orthogona**: Full pedagogical series
- **AXLE**: Lean 4 formal proofs (github.com/TOTOGT/AXLE)

---

**Questions?** Create an issue on GitHub or email brodananda@gmail.com

---

*G6 LLC · Newark, NJ · 2026*
