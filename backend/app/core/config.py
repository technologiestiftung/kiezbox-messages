from pydantic import BaseSettings

class Settings(BaseSettings):
    API_STR: str = "/api"
    PROJECT_NAME: str = "kiezbox-backend"
    SQLALCHEMY_DATABASE_URL = "sqlite:///./backend.db"

    class Config:
        case_sensitive = True


settings = Settings()
