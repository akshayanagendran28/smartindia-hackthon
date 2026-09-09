import os
from pydantic_settings import BaseSettings
from typing import List

class Settings(BaseSettings):
    PROJECT_NAME: str = "SCHEME SATHI API"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api"
    SECRET_KEY: str = os.getenv("SECRET_KEY", "scheme-sathi-sih26092-super-secret-key-2026")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7 days
    
    # SQLite local zero-config default, easily overridden with Postgres / PostGIS
    _BASE_DIR: str = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    _DEFAULT_DB: str = os.path.join(_BASE_DIR, "scheme_sathi.db").replace("\\", "/")
    DATABASE_URL: str = os.getenv("DATABASE_URL", f"sqlite:///{_DEFAULT_DB}")
    
    BACKEND_CORS_ORIGINS: List[str] = [
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "*"
    ]
    
    UPLOAD_DIR: str = os.getenv("UPLOAD_DIR", "./uploads")
    MAX_UPLOAD_SIZE_MB: int = 15
    API_KEY: str = os.getenv("API_KEY", "cb1_32xx_1_666070a703fded60fc5a5162")
    CHATBOT_API_KEY: str = os.getenv("CHATBOT_API_KEY", "cb1_32xx_1_666070a703fded60fc5a5162")
    CHATBASE_API_KEY: str = os.getenv("CHATBASE_API_KEY", "cb1_32xx_1_666070a703fded60fc5a5162")
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "cb1_32xx_1_666070a703fded60fc5a5162")
    
    # Ollama Local LLM Settings (Qwen)
    OLLAMA_BASE_URL: str = os.getenv("OLLAMA_BASE_URL", "http://127.0.0.1:11434")
    OLLAMA_MODEL: str = os.getenv("OLLAMA_MODEL", "qwen3:4b")
    OLLAMA_TIMEOUT_SECONDS: int = int(os.getenv("OLLAMA_TIMEOUT_SECONDS", "15"))

    class Config:
        case_sensitive = True

settings = Settings()
