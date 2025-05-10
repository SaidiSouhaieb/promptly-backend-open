from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    PROJECT_NAME: str = "Promptly API"
    API_V1_STR: str = "/api/v1"

    # OPENAI_API_KEY: str
    # SECRET_KEY: str
    # ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    POSTGRES_USERNAME: str
    POSTGRES_DB: str
    POSTGRES_PORT: str
    POSTGRES_PASSWORD: str
    POSTGRES_HOST: str
    POSTGRES_URL: str

    class Config:
        env_file = ".env"


settings = Settings()
