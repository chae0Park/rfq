import os

from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    OPENAI_API_KEY: str
    OPENAI_MODEL: str = "gpt-4.1-mini"
    DATABASE_URL: str

    COMPANY_NAME: str = os.getenv("COMPANY_NAME", "PromptOps Research")
    SENDER_NAME: str = os.getenv("SENDER_NAME", "Chaeyoung Park") 
    # gmail연동후에 바뀌어야 함 

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


settings = Settings()

print(settings.model_dump())
print(repr(settings.DATABASE_URL))