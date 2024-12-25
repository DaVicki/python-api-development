
from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path

# Define the path to the .env file
env_file_path = Path(__file__).parent / ".env"

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=env_file_path, env_file_encoding='utf-8') 

    database_hostname: str
    database_port: str
    database_password: str
    database_name: str
    database_username: str
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int


settings = Settings()