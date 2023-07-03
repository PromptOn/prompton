from pydantic import BaseSettings, SecretStr


class Settings(BaseSettings):
    DATABASE_URL: SecretStr
    MONGO_DATABASE: str

    DEFAULT_OPENAI_REQUEST_TIMEOUT_SECONDS: float = 90

    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    JWT_SECRET_KEY: SecretStr
    JWT_ALGORITHM: str = "HS256"

    GOOGLE_CLIENT_ID: SecretStr | None = None
    GOOGLE_CLIENT_SECRET: SecretStr | None = None
    STARLETTE_SESSION_SECRET: SecretStr | None = None

    GITHUB_ENV: str | None
    GITHUB_SHA: str | None

    class Config:
        env_file = "./.env"


settings = Settings.parse_obj({})


# TODO: create a settings getter, use it with Depends in endpoints and decorate with @lru_cache
