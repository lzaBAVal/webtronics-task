import aioredis

from internal.config.config import get_config


config = get_config()
redis = aioredis.from_url('redis://' + config.redis.host + ":" + config.redis.port, encoding='utf-8', decode_responses=True)


async def get_redis_session():
    return redis