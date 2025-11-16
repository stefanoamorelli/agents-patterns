import os
from pathlib import Path

from dotenv import load_dotenv

env_path = Path(__file__).parent.parent.parent / ".env"
if env_path.exists():
    load_dotenv(dotenv_path=env_path)


class Config:
    ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
    FRED_API_KEY = os.getenv("FRED_API_KEY")
    SEC_EDGAR_USER_AGENT = os.getenv("SEC_EDGAR_USER_AGENT")
    SEC_EDGAR_MCP_URL = os.getenv("SEC_EDGAR_MCP_URL", "http://127.0.0.1:9000")
    FRED_MCP_URL = os.getenv("FRED_MCP_URL", "http://127.0.0.1:9001")

    @classmethod
    def validate(cls) -> None:
        if not cls.ANTHROPIC_API_KEY:
            raise ValueError(
                "ANTHROPIC_API_KEY not found. Make sure it's exported in your shell environment"
            )
        if not cls.FRED_API_KEY:
            raise ValueError(
                "FRED_API_KEY is required. Get one from https://fred.stlouisfed.org/docs/api/api_key.html"
            )
        if not cls.SEC_EDGAR_USER_AGENT:
            raise ValueError(
                "SEC_EDGAR_USER_AGENT is required (format: 'Your Name (email@example.com)')"
            )
