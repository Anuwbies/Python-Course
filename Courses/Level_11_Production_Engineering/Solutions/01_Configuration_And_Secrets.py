from dataclasses import dataclass, field

@dataclass(frozen=True)
class Settings:
    database_url: str = field(repr=False)
    token_ttl_seconds: int

def load_settings(mapping):
    database_url = mapping.get("DATABASE_URL", "").strip()
    if not database_url:
        raise ValueError("DATABASE_URL is required")
    try:
        ttl = int(mapping.get("TOKEN_TTL_SECONDS", ""))
    except ValueError as error:
        raise ValueError("TOKEN_TTL_SECONDS must be an integer") from error
    if not 1 <= ttl <= 3600:
        raise ValueError("TOKEN_TTL_SECONDS out of range")
    return Settings(database_url, ttl)

settings = load_settings({"DATABASE_URL": "sqlite:///example.sqlite", "TOKEN_TTL_SECONDS": "300"})
print(settings.token_ttl_seconds)
try:
    load_settings({"DATABASE_URL": "sqlite:///example.sqlite", "TOKEN_TTL_SECONDS": "0"})
except ValueError:
    print("Rejected")
