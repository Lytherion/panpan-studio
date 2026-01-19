from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str = "sqlite+aiosqlite:///./panpan.db"
    SECRET_KEY: str = "change-this-secret-key"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    ADMIN_USERNAME: str = "admin"
    ADMIN_PASSWORD: str = "admin123"
    UPLOAD_DIR: str = "./uploads"
    MAX_FILE_SIZE: int = 10485760
    SHIPPING_FEE: float = 10.0

    class Config:
        env_file = ".env"

settings = Settings()
