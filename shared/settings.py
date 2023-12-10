from pydantic import Field, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class PostgresSettings(BaseSettings):
    user: str
    host: str
    password: SecretStr
    port: int
    database: str


class RedisSettings(BaseSettings):
    host: str
    password: SecretStr
    port: str


class SessionSettings(BaseSettings):
    key: SecretStr


class RabbitMQUser(BaseSettings):
    user: str
    password: SecretStr = Field(alias="pass")


class RabbitMQSettings(BaseSettings):
    default: RabbitMQUser


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        env_nested_delimiter="_",
        extra="ignore",
    )

    postgres: PostgresSettings
    redis: RedisSettings
    session: SessionSettings
    rabbitmq: RabbitMQSettings


settings = Settings()  # type: ignore
