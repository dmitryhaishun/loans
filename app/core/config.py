from typing import Any, Dict

from pydantic import BaseSettings, KafkaDsn, PostgresDsn, RedisDsn, validator


class Settings(BaseSettings):
    DB_HOST: str
    DB_USER: str
    DB_PASSWORD: str
    DB_NAME_LOANS: str
    DB_NAME_TEST: str

    REDIS_LOANS_HOST: str
    REDIS_LOANS_PORT: str

    KAFKA_HOST: str
    KAFKA_PORT: str

    SQLALCHEMY_DATABASE_URI: PostgresDsn | None = None
    SQLALCHEMY_TEST_DATABASE_URI: PostgresDsn | None = None

    REDIS_URI: RedisDsn | None = None

    KAFKA_URI: KafkaDsn | None = None

    @validator("SQLALCHEMY_DATABASE_URI", pre=True)
    def assemble_db_connection(cls, v: str | None, values: Dict[str, Any]) -> Any:
        if isinstance(v, str):
            return v
        return PostgresDsn.build(
            scheme="postgresql+asyncpg",
            user=values.get("DB_USER"),
            password=values.get("DB_PASSWORD"),
            host=values.get("DB_HOST"),
            path=f"/{values.get('DB_NAME_LOANS')}",
        )

    @validator("SQLALCHEMY_TEST_DATABASE_URI", pre=True)
    def assemble_test_db_connection(cls, v: str | None, values: Dict[str, Any]) -> Any:
        if isinstance(v, str):
            return v
        return PostgresDsn.build(
            scheme="postgresql+asyncpg",
            user=values.get("DB_USER"),
            password=values.get("DB_PASSWORD"),
            host=values.get("DB_HOST"),
            path=f"/{values.get('DB_NAME_TEST')}",
        )

    @validator("REDIS_URI", pre=True)
    def redis_connection(cls, c: str | None, values: Dict[str, Any]) -> Any:
        if isinstance(c, str):
            return c
        return RedisDsn.build(
            scheme="redis",
            host=values.get("REDIS_LOANS_HOST"),
            port=values.get("REDIS_LOANS_PORT"),
        )

    @validator("KAFKA_URI", pre=True)
    def assemble_kafka_connection(cls, v: str | None, values: Dict[str, Any]) -> Any:
        if isinstance(v, str):
            return v
        return KafkaDsn.build(
            scheme="kafka",
            host=values.get("KAFKA_HOST"),
            port=values.get("KAFKA_PORT"),
        )

    class Config:
        case_sensitive = True
        env_file = ".env"


settings = Settings()
