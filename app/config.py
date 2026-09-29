from __future__ import annotations

from functools import lru_cache
from pathlib import Path
from typing import Any

import yaml
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_env: str = "development"
    log_level: str = "INFO"
    telegram_bot_token: str = ""
    database_url: str = "sqlite+aiosqlite:///./data/quant.db"
    redis_url: str = "redis://localhost:6379/0"
    market_data_api_key: str = ""
    news_api_key: str = ""
    fundamental_api_key: str = ""
    macro_api_key: str = ""
    ai_api_key: str = ""
    admin_user_ids: str = ""
    default_timezone: str = "Europe/Istanbul"
    risk_per_trade: float = Field(default=0.005, ge=0, le=1)
    max_position_pct: float = Field(default=0.10, ge=0, le=1)
    max_sector_exposure: float = Field(default=0.30, ge=0, le=1)
    max_portfolio_heat: float = Field(default=0.10, ge=0, le=1)
    slippage_bps: float = Field(default=5, ge=0)
    commission_bps: float = Field(default=1, ge=0)
    news_refresh_minutes: int = Field(default=15, ge=1)
    technical_refresh_minutes: int = Field(default=5, ge=1)
    model_config = SettingsConfigDict(env_file=".env", extra="ignore", case_sensitive=False)

    @property
    def admin_ids(self) -> set[int]:
        return {int(x.strip()) for x in self.admin_user_ids.split(",") if x.strip().isdigit()}


@lru_cache
def get_settings() -> Settings:
    return Settings()


def load_yaml_config(path: str = "config.yaml") -> dict[str, Any]:
    p = Path(path)
    if not p.exists():
        return {}
    return yaml.safe_load(p.read_text(encoding="utf-8")) or {}
