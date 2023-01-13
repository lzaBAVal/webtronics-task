from pydantic import BaseSettings


class DbConfig(BaseSettings):
    db_scheme: str = 'postgresql+asyncpg'
    db_user: str = 'admin'
    db_pass: str = 'strongpass'
    db_host: str = 'localhost'
    db_port: str = '5432'
    db_name: str = 'webtronics'
    
    class Config:
            env_prefix = 'WT'
            case_sensitive = False


def get_url(conf: DbConfig) -> str:
    return conf.db_scheme + "://" + conf.db_user + ":" + conf.db_pass + "@" + conf.db_host + ":" + conf.db_port + "/" + conf.db_name


class JWTConfig(BaseSettings):
    algorithm: str = 'HS256'
    expires_sec: int = 60
    refresh_expires_sec: int = 10
    secret: str = '38c7c584daac3afdabcf71eb3218ce3ce4027c5e5716d801f0c89ca5710aae28'


class RedisConfig(BaseSettings):
    host: str = 'localhost'
    port: str = '6379'


class Config(BaseSettings):
    server_host: str = '127.0.0.1'
    server_port: str = '8000'
    database_url: str = get_url(DbConfig())
    jwt: JWTConfig = JWTConfig()
    redis: RedisConfig = RedisConfig()

    class Config:
        env_prefix = 'WT'
        case_sensitive = False


config = Config()