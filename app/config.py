
from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path

# Define the path to the .env file
# env_file_path = Path(__file__).parent/ ".env"

# print(f'env file path: {env_file_path}')

class Settings(BaseSettings):
    # model_config = SettingsConfigDict(env_file=env_file_path, env_file_encoding='utf-8') 

    database_hostname: str = 'localhost'
    database_port: str = '5432'
    database_password: str = 'postgres'
    database_name: str = 'fastapi'
    database_username: str = 'postgres'
    database_schema: str = 'davicki'
    secret_key: str = '09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7'
    algorithm: str = 'HS256'
    access_token_expire_minutes: int = 30


settings = Settings()