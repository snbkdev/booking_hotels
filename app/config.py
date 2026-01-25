from pydantic_settings import BaseSettings
from pydantic import computed_field

class Settings(BaseSettings):
    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PASSWORD: str
    DB_NAME: str
    DB_DRIVER: str

    DB_MAX_OVERFLOW: int = 10
    DB_ECHO: bool = False
    DB_POOL_SIZE: int = 20

    SECRET_KEY: str
    ALGORITHM: str

    @computed_field
    @property
    def get_database_url(self) -> str:
        return f"postgresql+{self.DB_DRIVER}://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()

print(settings.get_database_url)
print(settings.DB_ECHO)