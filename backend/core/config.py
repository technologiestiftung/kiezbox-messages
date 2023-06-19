from pydantic import BaseSettings

class Settings(BaseSettings):
    API_STR: str = "/api"
    PROJECT_NAME: str = "kiezbox-backend"

    class Config:
        case_sensitive = True


settings = Settings()
