from pydantic import BaseModel
import os


class Settings(BaseModel):
    env: str = os.getenv("ENV", "dev")
    log_level: str = os.getenv("LOG_LEVEL", "INFO")
    cors_origins: str = os.getenv("CORS_ORIGINS", "*")
    rate_limit_rpm: int = int(os.getenv("RATE_LIMIT_RPM", "60"))
    cache_ttl_days: int = int(os.getenv("CACHE_TTL_DAYS", "30"))
    redis_url: str | None = os.getenv("REDIS_URL")
    disable_llm: bool = os.getenv("DISABLE_LLM", "true").lower() == "true"


settings = Settings()


