from enum import Enum
from functools import lru_cache
from pydantic import BaseSettings


class DbConfig(BaseSettings):
    scheme: str = 'postgresql+asyncpg'
    user: str = 'admin'
    password: str = 'strongpass'
    host: str = 'localhost'
    port: str = '5432'
    name: str = 'webtronics'

    class Config:
        env_prefix = "db_"

    
    def get_url(self) -> str:
        return self.scheme + "://" + self.user + ":" + self.password + "@" + self.host + ":" + self.port + "/" + self.name


class JWTConfig(BaseSettings):
    algorithm: str = 'HS256'
    expires_sec: int = 60 * 10
    refresh_expires_sec: int = 60 * 60
    secret: str = '38c7c584daac3afdabcf71eb3218ce3ce4027c5e5716d801f0c89ca5710aae28'

    class Config:
        env_prefix = "jwt_"
        env_file_encoding = 'utf-8'



class RedisConfig(BaseSettings):
    host: str = 'localhost'
    port: str = '6379'

    class Config:
        env_prefix = "redis_"


class Config(BaseSettings):
    db: DbConfig = DbConfig()
    jwt: JWTConfig = JWTConfig()
    redis: RedisConfig = RedisConfig()


@lru_cache()
def get_config(**kwargs):

    db = DbConfig(**kwargs)
    jwt = JWTConfig(**kwargs)
    redis = RedisConfig(**kwargs)

    config = Config(**kwargs)

    config.jwt = jwt
    config.db = db
    config.redis = redis

    return config