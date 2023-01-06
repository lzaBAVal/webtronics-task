from pydantic import BaseSettings


class DbConfig(BaseSettings):
    db_user: str = 'admin'
    db_pass: str = ''
    db_host: str = 'localhost'
    db_port: str = '5432'
    db_name: str = 'webtronics'
    
    class Config:
            env_prefix = 'WT'
            case_sensitive = False


def get_url(conf: DbConfig) -> str:
    return "postgresql+pyscopg2://" + conf.db_user + ":" + conf.db_pass + "@" + conf.db_host + ":" + conf.db_port + "/" + conf.db_name


class Config(BaseSettings):
    server_host: str = '127.0.0.1'
    server_port: str = '8000'
    database_url: DbConfig = get_url(DbConfig())

    class Config:
        env_prefix = 'WT'
        case_sensitive = False


config = Config(
    _env_file='.env',
    _env_file_encoding='utf-8',
)