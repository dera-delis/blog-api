from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    # Database
    database_url: str = "postgresql://postgres:password@localhost:5432/blog_api"
    
    # JWT
    secret_key: str = "your-secret-key-here-change-in-production"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    
    # Application
    debug: bool = True
    api_v1_str: str = "/api/v1"
    project_name: str = "Blog API"
    
    class Config:
        env_file = ".env"
        case_sensitive = False


settings = Settings()
