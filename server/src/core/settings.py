from pydantic import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: str
    MONGO_DATABASE: str

    DEFAULT_OPENAI_REQUEST_TIMEOUT_SECONDS: float = 90

    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = 15
    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str = "HS256"

    GITHUB_ENV: str | None
    GITHUB_SHA: str | None

    class Config:
        env_file = "./.env"


settings = Settings.parse_obj({})


# TODO: create a settings getter, use it with Depends in endpoints and decorate with @lru_cache
