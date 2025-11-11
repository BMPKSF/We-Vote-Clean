import os
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

env_path = os.path.join(os.path.dirname(__file__), "../.env")
load_dotenv(dotenv_path=env_path)

class Settings(BaseSettings):
    database_url: str   # <— lowercase
    jwt_secret: str
    supabase_url: str
    supabase_key: str

settings = Settings()

