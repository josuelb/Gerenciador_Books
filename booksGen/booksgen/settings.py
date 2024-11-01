"""

Aqui sera o arquivo de leitura do .env,
ou seja, uma ponte pra ter acesso as
configurações necessárias.

"""

import os

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=os.path.join(os.path.dirname(__file__), '../.env'),
        env_file_encoding='utf-8'
    )

    DATABASE_URI:str
    DATABASE_TESTS_URI: str
    PORT_REDIS: int
    HOST_REDIS: str
    ALGORITHM: str
    SECRET_KEY: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    ZONE_INFO_HOUR: str