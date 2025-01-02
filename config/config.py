from dotenv import load_dotenv
import os
from pydantic_settings import BaseSettings

load_dotenv()


class Config(BaseSettings):
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY")
    OPENAI_API_BASEURL: str = os.getenv("OPENAI_API_BASEURL")
    CHAT_MODEL_ID: str = os.getenv("CHAT_MODEL_ID")
    EMBEDDING_MODEL_ID: str = os.getenv("EMBEDDING_MODEL_ID")
    LOG_LEVEL: str = os.getenv("LOG_LEVEL")
    NEO4J_DB_NAME: str = os.getenv("NEO4J_DB_NAME")
    NEO4J_USER: str = os.getenv("NEO4J_USER")
    NEO4J_PASSWORD: str = os.getenv("NEO4J_PASSWORD")
    NEO4J_URI: str = os.getenv("NEO4J_URI")


config = Config()
