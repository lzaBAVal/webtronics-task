from pydantic import BaseSettings

class MainSettings:
    class Config:
        case_sensitive = False
        env_file = '.enc', 'env.prod'

class DbConfig(MainSettings):
    scheme: str = 'postgresql+asyncpg'
    user: str = 'admin'
    password: str = 'strongpass'
    host: str = 'localhost'
    port: str = '5432'
    name: str = 'webtronics'

    class Config:
        env_prefix = "db"

    
    def get_url(self) -> str:
        return self.scheme + "://" + self.user + ":" + self.password + "@" + self.host + ":" + self.port + "/" + self.name


class JWTConfig(MainSettings):
    algorithm: str = 'HS256'
    expires_sec: int = 60 * 10
    refresh_expires_sec: int = 60 * 60
    secret: str = '38c7c584daac3afdabcf71eb3218ce3ce4027c5e5716d801f0c89ca5710aae28'

    class Config:
        env_prefix = "jwt"


class RedisConfig(MainSettings):
    host: str = 'localhost'
    port: str = '6379'

    class Config:
        env_prefix = "redis"


class Config(MainSettings):
    server_host: str = '127.0.0.1'
    server_port: str = '8000'
    database_url: str = DbConfig().get_url()
    jwt: JWTConfig = JWTConfig()
    redis: RedisConfig = RedisConfig()


config = Config()