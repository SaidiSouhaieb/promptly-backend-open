from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    PROJECT_NAME: str = "Promptly API"
    API_V1_STR: str = "/api/v1"

    POSTGRES_USER: str
    POSTGRES_DB: str
    POSTGRES_PORT: str
    POSTGRES_PASSWORD: str
    POSTGRES_HOST: str
    POSTGRES_URL: str

    class Config:
        env_file = ".env"
        extra="ignore"


settings = Settings()
