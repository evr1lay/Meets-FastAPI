from dataclasses import dataclass

@dataclass
class Settings:
    DATABASE_URL: str
    cors_allowed_origins: list[str]
    
def get_settings() -> Settings:
    return Settings(
        DATABASE_URL="sqlite:///forms.db",
        cors_allowed_origins=["http://localhost:5500", "http://127.0.0.1:5500"]
    )