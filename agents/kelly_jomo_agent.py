#!/usr/bin/env python3
"""
kelly_jomo_agent.py
G6 LLC · Pablo Nogueira Grossi · Newark NJ · 2026

JOMO trading agent for Polymarket.
Kelly sizing with hard fraction cap.
The bot runs. You live.

Usage:
    python agents/kelly_jomo_agent.py --dry-run
    python agents/kelly_jomo_agent.py --live
"""

import os
import json
import time
import logging
import argparse
import requests
from datetime import datetime, timezone
from dataclasses import dataclass, field
from typing import Optional

# ── Logging ────────────────────────────────────────────────────────────────
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s | %(levelname)s | %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
log = logging.getLogger('kelly_jomo')

# ── Config ─────────────────────────────────────────────────────────────────
ANTHROPIC_API_KEY  = os.environ.get('ANTHROPIC_API_KEY', '')
POLYMARKET_API_KEY = os.environ.get('POLYMARKET_API_KEY', '')
POLYMARKET_BASE    = 'https://clob.polymarket.com'

# Kelly parameters — conservative by design
KELLY_MAX_FRACTION = 0.20   # never bet more than 20% of bankroll on any position
KELLY_SCALE        = 0.25   # fractional Kelly: use 1/4 Kelly for safety
MIN_EDGE           = 0.04   # minimum edge required to enter (4%)
MIN_LIQUIDITY      = 500    # minimum market liquidity in USDC
MAX_POSITIONS      = 5      # maximum simultaneous open positions
SLEEP_BETWEEN_CYCLES = 300  # 5 minutes between cycles — JOMO not FOMO

# ── Data structures ────────────────────────────────────────────────────────
@dataclass
class Market:
    id: str
    question: str
    yes_price: float
    no_price: float
    volume: float
    end_date: str

@dataclass
class Position:
    market_id: str
    side: str          # 'YES' or 'NO'
    size: float        # USDC
    entry_price: float
    opened_at: str

@dataclass
class AgentState:
    bankroll: float = 1000.0
    positions: list = field(default_factory=list)
    trade_log: list = field(default_factory=list)
    cycle: int = 0

# ── Kelly sizing ───────────────────────────────────────────────────────────
def kelly_fraction(p_win: float, odds: float) -> float:
    """
    Kelly criterion: f = (p*b - q) / b
    where b = net odds (1/price - 1), p = win probability, q = 1 - p

    Hard cap at KELLY_MAX_FRACTION * KELLY_SCALE.
    Thin Polymarket markets require conservative sizing.
    A blown bankroll is not ocio.
    """
    if p_win <= 0 or p_win >= 1 or odds <= 0:
        return 0.0
    b = (1.0 / odds) - 1.0
    if b <= 0:
        return 0.0
    q = 1.0 - p_win
    f_raw = (p_win * b - q) / b
    f_fractional = f_raw * KELLY_SCALE
    f_capped = min(f_fractional, KELLY_MAX_FRACTION)
    return max(0.0, f_capped)

def bet_size(bankroll: float, fraction: float) -> float:
    """Convert Kelly fraction to USDC bet size. Floor at $1."""
    return max(1.0, round(bankroll * fraction, 2))

# ── Claude edge estimation ─────────────────────────────────────────────────
def estimate_edge(market: Market) -> dict:
    """
    Ask Claude to estimate the true probability of YES resolution.
    Returns {'p_yes': float, 'confidence': str, 'reasoning': str}
    Falls back to market price (zero edge) on any failure.
    """
    if not ANTHROPIC_API_KEY:
        log.warning('No ANTHROPIC_API_KEY — using market price as fair value')
        return {'p_yes': market.yes_price, 'confidence': 'none', 'reasoning': 'no API key'}

    prompt = f"""You are a prediction market analyst. Estimate the true probability of YES for this market.

Market: {market.question}
Current YES price: {market.yes_price:.3f}
Current NO price:  {market.no_price:.3f}
End date: {market.end_date}
Volume: ${market.volume:,.0f}

Respond ONLY with valid JSON, no other text:
{{"p_yes": <float 0-1>, "confidence": "<low|medium|high>", "reasoning": "<one sentence>"}}"""

    try:
        resp = requests.post(
            'https://api.anthropic.com/v1/messages',
            headers={
                'x-api-key': ANTHROPIC_API_KEY,
                'anthropic-version': '2023-06-01',
                'content-type': 'application/json',
            },
            json={
                'model': 'claude-sonnet-4-20250514',
                'max_tokens': 200,
                'messages': [{'role': 'user', 'content': prompt}]
            },
            timeout=15
        )
        resp.raise_for_status()
        text = resp.json()['content'][0]['text'].strip()
        result = json.loads(text)
        p = float(result['p_yes'])
        if not 0 < p < 1:
            raise ValueError(f'p_yes out of range: {p}')
        return result
    except Exception as e:
        log.error(f'Claude estimation failed: {e}')
        return {'p_yes': market.yes_price, 'confidence': 'none', 'reasoning': str(e)}

# ── Polymarket API ─────────────────────────────────────────────────────────
def fetch_markets(limit: int = 20) -> list[Market]:
    """Fetch active markets from Polymarket CLOB."""
    try:
        resp = requests.get(
            f'{POLYMARKET_BASE}/markets',
            params={'active': 'true', 'limit': limit},
            timeout=10
        )
        resp.raise_for_status()
        data = resp.json().get('data', [])
        markets = []
        for m in data:
            tokens = m.get('tokens', [])
            if len(tokens) < 2:
                continue
            yes_tok = next((t for t in tokens if t.get('outcome') == 'Yes'), None)
            no_tok  = next((t for t in tokens if t.get('outcome') == 'No'),  None)
            if not yes_tok or not no_tok:
                continue
            yes_p = float(yes_tok.get('price', 0.5))
            no_p  = float(no_tok.get('price',  0.5))
            vol   = float(m.get('volume', 0))
            if vol < MIN_LIQUIDITY:
                continue
            markets.append(Market(
                id=m['condition_id'],
                question=m.get('question', ''),
                yes_price=yes_p,
                no_price=no_p,
                volume=vol,
                end_date=m.get('end_date_iso', ''),
            ))
        log.info(f'Fetched {len(markets)} liquid markets')
        return markets
    except Exception as e:
        log.error(f'Market fetch failed: {e}')
        return []

def place_order(market_id: str, side: str, size: float, price: float, dry_run: bool) -> bool:
    """Place a limit order. Dry run just logs."""
    if dry_run:
        log.info(f'DRY RUN | {side} {size:.2f} USDC @ {price:.3f} | market {market_id[:8]}...')
        return True
    if not POLYMARKET_API_KEY:
        log.warning('No POLYMARKET_API_KEY — cannot place live order')
        return False
    # Live order placement — implement with py-clob-client when ready
    log.warning('Live order placement not yet implemented — add py-clob-client')
    return False

# ── Core cycle ─────────────────────────────────────────────────────────────
def run_cycle(state: AgentState, dry_run: bool) -> AgentState:
    state.cycle += 1
    log.info(f'── Cycle {state.cycle} | Bankroll: ${state.bankroll:.2f} | Positions: {len(state.positions)} ──')

    if len(state.positions) >= MAX_POSITIONS:
        log.info('Max positions held — resting. This is ocio.')
        return state

    markets = fetch_markets()
    if not markets:
        log.info('No markets available')
        return state

    for market in markets:
        if len(state.positions) >= MAX_POSITIONS:
            break
        if any(p.market_id == market.id for p in state.positions):
            continue

        estimate = estimate_edge(market)
        p_yes = estimate['p_yes']
        confidence = estimate['confidence']

        # Check YES edge
        yes_edge = p_yes - market.yes_price
        no_edge  = (1 - p_yes) - market.no_price

        best_edge = max(yes_edge, no_edge)
        best_side = 'YES' if yes_edge >= no_edge else 'NO'
        best_price = market.yes_price if best_side == 'YES' else market.no_price
        best_p = p_yes if best_side == 'YES' else (1 - p_yes)

        if best_edge < MIN_EDGE:
            log.info(f'No edge ({best_edge:.3f}) on: {market.question[:60]}')
            continue

        if confidence == 'low':
            log.info(f'Low confidence — skipping: {market.question[:60]}')
            continue

        f = kelly_fraction(best_p, best_price)
        size = bet_size(state.bankroll, f)

        log.info(
            f'SIGNAL | {best_side} | edge={best_edge:.3f} | '
            f'kelly={f:.3f} | size=${size:.2f} | '
            f'{market.question[:50]}'
        )

        placed = place_order(market.id, best_side, size, best_price, dry_run)
        if placed:
            pos = Position(
                market_id=market.id,
                side=best_side,
                size=size,
                entry_price=best_price,
                opened_at=datetime.now(timezone.utc).isoformat()
            )
            state.positions.append(pos)
            state.bankroll -= size
            state.trade_log.append({
                'cycle': state.cycle,
                'market': market.question[:80],
                'side': best_side,
                'size': size,
                'price': best_price,
                'edge': best_edge,
                'kelly_f': f,
                'time': pos.opened_at,
            })

    return state

# ── Main ───────────────────────────────────────────────────────────────────
def main():
    parser = argparse.ArgumentParser(description='Kelly JOMO Agent — G6 LLC')
    parser.add_argument('--dry-run', action='store_true', default=True,
                        help='Dry run (default: True — no real orders)')
    parser.add_argument('--live', action='store_true',
                        help='Place real orders (requires POLYMARKET_API_KEY)')
    parser.add_argument('--bankroll', type=float, default=1000.0,
                        help='Starting bankroll in USDC (default: 1000)')
    parser.add_argument('--cycles', type=int, default=0,
                        help='Number of cycles (0 = run forever)')
    args = parser.parse_args()

    dry_run = not args.live
    if dry_run:
        log.info('Running in DRY RUN mode — no real orders will be placed')
    else:
        log.info('Running in LIVE mode — real orders will be placed')
        if not POLYMARKET_API_KEY:
            log.error('LIVE mode requires POLYMARKET_API_KEY')
            return

    state = AgentState(bankroll=args.bankroll)
    log.info(f'Kelly JOMO Agent started | bankroll=${state.bankroll:.2f}')
    log.info(f'Kelly cap: {KELLY_MAX_FRACTION} | Scale: {KELLY_SCALE} | Min edge: {MIN_EDGE}')
    log.info(f'Cycle interval: {SLEEP_BETWEEN_CYCLES}s — the bot runs, you live')

    cycle_count = 0
    try:
        while True:
            state = run_cycle(state, dry_run)
            cycle_count += 1
            if args.cycles and cycle_count >= args.cycles:
                break
            log.info(f'Sleeping {SLEEP_BETWEEN_CYCLES}s — ocio')
            time.sleep(SLEEP_BETWEEN_CYCLES)
    except KeyboardInterrupt:
        log.info('Agent stopped by user')

    log.info(f'Final bankroll: ${state.bankroll:.2f}')
    log.info(f'Trades placed: {len(state.trade_log)}')
    if state.trade_log:
        print(json.dumps(state.trade_log, indent=2))

if __name__ == '__main__':
    main()
