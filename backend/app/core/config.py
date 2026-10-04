"""Application configuration settings for RakshaScan Backend."""

import os
from typing import List


class Settings:
    PROJECT_NAME: str = os.getenv("PROJECT_NAME", "RakshaScan Analysis Engine")
    VERSION: str = "0.2.0"
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "development")
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    API_V1_PREFIX: str = "/api/v1"

    # SSRF & Networking Limits (aligned with SECURITY.md)
    MAX_RESPONSE_BYTES: int = int(os.getenv("MAX_RESPONSE_BYTES", str(5 * 1024 * 1024)))  # 5 MB
    CONNECT_TIMEOUT_SECONDS: float = float(os.getenv("CONNECT_TIMEOUT_SECONDS", "3.0"))
    READ_TIMEOUT_SECONDS: float = float(os.getenv("READ_TIMEOUT_SECONDS", "7.0"))
    TOTAL_TIMEOUT_SECONDS: float = float(os.getenv("TOTAL_TIMEOUT_SECONDS", "10.0"))
    MAX_REDIRECTS: int = int(os.getenv("MAX_REDIRECTS", "3"))

    # Payload & Size Limits
    MAX_URL_LENGTH: int = int(os.getenv("MAX_URL_LENGTH", "2048"))
    MAX_MESSAGE_CHARACTERS: int = int(os.getenv("MAX_MESSAGE_CHARACTERS", "15000"))
    MAX_IMAGE_BYTES: int = int(os.getenv("MAX_IMAGE_BYTES", str(10 * 1024 * 1024)))  # 10 MB
    MAX_IMAGE_DIMENSION: int = int(os.getenv("MAX_IMAGE_DIMENSION", "8000"))  # 8000x8000

    # Rate Limiting Configuration
    RATE_LIMITING_ENABLED: bool = os.getenv("RATE_LIMITING_ENABLED", "True").lower() in ("true", "1", "yes")
    RATE_LIMIT_URL_PER_MINUTE: int = int(os.getenv("RATE_LIMIT_URL_PER_MINUTE", "30"))
    RATE_LIMIT_MESSAGE_PER_MINUTE: int = int(os.getenv("RATE_LIMIT_MESSAGE_PER_MINUTE", "30"))
    RATE_LIMIT_SCREENSHOT_PER_MINUTE: int = int(os.getenv("RATE_LIMIT_SCREENSHOT_PER_MINUTE", "15"))

    # Bot identification
    USER_AGENT: str = (
        "RakshaScan-Analysis-Bot/0.2.0 "
        "(+https://github.com/sangyan/rakshascan; evidence-based research analyzer)"
    )

    # Allowed CORS Origins
    @property
    def CORS_ORIGINS(self) -> List[str]:
        raw_origins = os.getenv("CORS_ORIGINS", "")
        if raw_origins:
            return [origin.strip() for origin in raw_origins.split(",") if origin.strip()]
        return [
            "http://localhost:3000",
            "http://127.0.0.1:3000",
            "http://10.59.84.80:3000",
        ]

    # Safe test & fictional domains for demonstration & unit testing
    # RFC 2606 reserved domains
    FICTIONAL_TEST_DOMAINS: List[str] = [
        "example-finance.test",
        "example.test",
        "demo-finance.test",
    ]


settings = Settings()

