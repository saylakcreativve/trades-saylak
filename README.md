# Professional Quant Investment Intelligence Platform

Decision-support and quant-research platform with Telegram as the first UI. It is designed around measurement, reproducibility, risk controls, paper trading, and explicit uncertainty. It does **not** promise returns or treat model scores as probabilities.

## Current implementation status

### Working in this bootstrap
- Python 3.12+ project structure
- Pydantic environment configuration
- SQLite development database with SQLAlchemy async support
- PostgreSQL + Redis Docker services
- Provider abstraction with Yahoo Finance implementation
- OHLCV normalization and validation
- Technical indicators: SMA/EMA, RSI, MACD, ATR, Bollinger Bands, relative volume, OBV, historical volatility
- Basic technical/fundamental scoring
- Ensemble decision guardrail
- ATR stop + 2R target + risk-based position sizing
- Telegram `/start`, `/help`, `/analiz`, `/grafik`, `/firsatlar`, `/status`
- Daily chart generation
- RSS news ingestion and basic geopolitical event classification
- Basic EMA crossover backtest function
- Basic time-series logistic regression research module
- Paper broker abstraction
- Prediction record structure
- Unit tests for core risk/scoring/indicator logic
- Dockerfile and docker-compose

### Not yet production-complete
The full specification contains a much larger research platform. The following are intentionally not represented as finished: multi-provider failover, full macro database ingestion, institutional news verification, event-study database, complete portfolio optimizer, calibrated production probabilities, drift monitoring, champion/challenger promotion, full scheduler/worker topology, comprehensive Telegram watchlists/alerts, and broker execution. The current commands expose only implemented behavior.

## Installation

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -e '.[dev]'
cp .env.example .env
```

Set `TELEGRAM_BOT_TOKEN` in `.env`. Never commit `.env`.

## Telegram bot setup

1. Open Telegram and talk to BotFather.
2. Create a bot and copy its token.
3. Put the token into `.env` as `TELEGRAM_BOT_TOKEN=...`.
4. Start the bot:

```bash
python -m app.main
```

## Commands

- `/start`
- `/help`
- `/analiz NVDA`
- `/grafik NVDA`
- `/firsatlar`
- `/status`

Some advanced command names are reserved in the architecture but intentionally return status until their underlying engine is implemented. This prevents fake functionality, because apparently software also needs an honesty policy.

## Data freshness

Yahoo Finance data can be delayed or provider-dependent. Every market snapshot is labeled `DELAYED` in the current implementation. The system does not pretend that delayed data is live.

## Risk model

Default risk per trade is 0.5% of reference capital, with a configurable maximum position percentage. Stop distance determines quantity. This is a calculation aid, not a guarantee or personalized investment instruction.

## Backtesting

The current research module includes a basic EMA crossover backtest with configurable fee and slippage assumptions. It is not yet the full walk-forward/event-study engine described in the target architecture.

## ML

The initial ML research model is time-ordered logistic regression using technical features. It does not randomly split the time series. Production probability calibration and champion/challenger promotion are not yet enabled.

## Database

Development defaults to SQLite. Production should use PostgreSQL by setting `DATABASE_URL`, for example:

`postgresql+asyncpg://quant:password@postgres:5432/quant`

Alembic configuration should be added before production schema evolution. The bootstrap uses SQLAlchemy metadata initialization for local development.

## Docker

```bash
cp .env.example .env
# Set TELEGRAM_BOT_TOKEN and change database secrets before production use.
docker compose up --build -d
```

## Testing

```bash
pytest -q
```

## Architecture principle

`DATA -> VALIDATE -> FEATURES -> ANALYSIS -> QUANT/ML -> RISK -> DECISION -> RECORD -> MEASURE -> RESEARCH -> VALIDATE -> PAPER TRADE -> PROMOTE`

No future information should enter a prediction's feature snapshot. Predictions are recorded separately from later outcomes so historical performance can be measured without rewriting the original prediction.

## Production roadmap

1. Multi-provider market data and failover
2. Provider freshness/latency registry
3. Full news/entity deduplication and source verification
4. Macro time-series ingestion
5. Geopolitical event database and event studies
6. Full backtest engine with walk-forward/OOS testing
7. Paper trading tracker with T+1/T+3/T+7/T+14/T+30 evaluation
8. Probability calibration and reliability curves
9. Model drift monitoring
10. Champion/challenger registry and promotion gates
11. Portfolio/correlation/risk dashboards
12. Telegram alerts, watchlists, reports
13. Worker/scheduler separation
14. Observability and health metrics
15. Broker abstraction with real trading disabled by default

## 24/7 Deployment

### Railway (recommended for the Telegram worker)

Railway treats persistent services as continuously running services and can build directly from this repository's Dockerfile. The included `railway.toml` starts the bot with `python -m app.main` and configures restart/health-check behavior. Railway can also provision PostgreSQL as a separate service and expose service variables to the bot.

1. Push this repository to GitHub.
2. Create a Railway project.
3. Add a service from the GitHub repository.
4. Add PostgreSQL from Railway's database options.
5. Set the required variables from `.env.example`, especially `TELEGRAM_BOT_TOKEN` and `DATABASE_URL`.
6. Deploy the service.
7. Check logs for `SYSTEM READY`.

Do not commit `.env`. Secrets belong in Railway Variables.

### Render

The included `render.yaml` defines a Docker Background Worker. Render supports continuously running background workers and Docker-based services. A managed Postgres/Key Value service can be used instead of local SQLite/Redis. Background workers are a paid service type, so check the current Render plan/pricing before deployment.

### Vercel

Vercel is not used for the Telegram polling worker. Its function model is designed for request-driven/serverless execution rather than a permanently running polling process. If a future web dashboard is added, Vercel can host that frontend separately while Railway/Render runs the bot and workers.
