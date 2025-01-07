from dotenv import load_dotenv
import os
from pydantic_settings import BaseSettings

load_dotenv()


class Config(BaseSettings):

    OPENAI_API_KEY: str | None = os.getenv("OPENAI_API_KEY")
    OPENAI_API_BASEURL: str | None = os.getenv("OPENAI_API_BASEURL")
    CHAT_MODEL_ID: str | None = os.getenv("CHAT_MODEL_ID")
    EMBEDDING_MODEL_ID: str | None = os.getenv("EMBEDDING_MODEL_ID")
    LOG_LEVEL: str | None = os.getenv("LOG_LEVEL")
    POSTGRES_DB: str = os.getenv("POSTGRES_DB", "graphmind")
    POSTGRES_USER: str = os.getenv("POSTGRES_USER", "postgres")
    POSTGRES_PASSWORD: str = os.getenv("POSTGRES_PASSWORD", "postgres")
    POSTGRES_HOST: str = os.getenv("POSTGRES_HOST", "localhost")
    POSTGRES_PORT: str = os.getenv("POSTGRES_PORT", "5432")

    @property
    def DATABASE_URL(self) -> str:
        return f"postgresql://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"


config = Config()
