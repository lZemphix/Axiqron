# AGENTS.md

## Project overview

`trade_bot` is a Python 3.13 trading-bot prototype managed with `uv`.

- `bot/core/exchanges/` contains exchange adapters. `Bybit` wraps
  `pybit.unified_trading.HTTP` and converts API payloads into local dataclasses.
- `bot/strategies/` contains strategy implementations and their local JSON
  configuration.
- `bot/core/events/indicators/` exposes RSI and MACD calculations via native
  shared libraries; the C sources live in `_uncompile/cfiles/`.
- `common/` contains settings, shared configuration, models, and registries.
- `database/` contains the asynchronous PostgreSQL helper.
- `services/` and `interface/` are currently scaffolds.
- `tests/` holds pytest tests, currently focused on the Bybit adapter.

## Setup and commands

Use `uv`; do not add a second dependency-management workflow.

```bash
uv sync --group dev
uv run pytest -v
uv run ruff format --check .
uv run ruff check .
```

`precommit.sh` currently runs pytest followed by `ruff format .` and
`ruff check --fix`; it changes files, so use it only when formatting/fixing the
working tree is intended.

## Change guidelines

- Preserve the existing package layout and absolute imports from the repository
  root (for example, `from common.utils.types import Kline`). `pytest.ini` sets
  `pythonpath = .` for this purpose.
- Keep external exchange payload handling inside the adapter. Return the shared
  `Kline` and `Order` dataclasses rather than exposing raw API dictionaries.
- For adapter changes, test both a successful response and non-zero `retCode`.
  Tests should inject a fake connection and must not call a real exchange.
- Maintain Bybit kline ordering: the adapter reverses the API response so
  callers receive chronological data.
- Strategy-specific settings belong in that strategy directory (for example,
  `bot/strategies/lines/config.json`); global bot settings belong in
  `common/configs/bot_config.json`.
- Do not edit generated native `.so` files. If indicator behavior needs to
  change, update the Python wrapper and/or the corresponding C source, and
  document any required build step.
- Follow Ruff formatting. Add type hints to new or changed public functions;
  use `pathlib.Path` for repository-relative file access.

## Secrets and trading safety

- `.env` contains credentials and is intentionally ignored. Never read, print,
  commit, or add actual API keys, database passwords, or bot tokens to source,
  tests, or documentation. Keep `.env.example` limited to placeholders.
- Treat `place_buy_order` and `place_sell_order` as production-impacting code.
  Do not run code that can place orders. Keep testnet/demo selection explicit
  and cover order request payloads with fakes.
- Do not change committed trading configuration values unless the task
  explicitly asks for it.

## Before handing off changes

Run the smallest relevant test set first, then the full suite when practical:

```bash
uv run pytest tests/test_bybit.py -v
uv run pytest -v
uv run ruff format --check .
uv run ruff check .
```

Report commands that could not run and why. Do not overwrite unrelated
uncommitted work.
