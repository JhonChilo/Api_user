from pydantic import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    # Configuración de la base de datos
    DB_HOST: str = "localhost"
    DB_PORT: int = 3306
    DB_NAME: str = "your_database_name"
    DB_USER: str = "your_username"
    DB_PASSWORD: str = "your_password"

    # Configuración de JWT
    SECRET_KEY: str = "a_really_secret_key"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30  # Expiración en minutos

    # Otros parámetros de configuración
    DEBUG: bool = True
    LOG_LEVEL: str = "info"

    # Este método permite cargar la configuración desde un archivo .env
    class Config:
        env_file = ".env"

# Instancia de configuración
settings = Settings()
