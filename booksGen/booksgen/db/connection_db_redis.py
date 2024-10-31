"""
Aqui estará a conectivadade com o 
redis, sera retornado o sessionRedis
"""

import redis

from booksgen.settings import Settings

redis_client = redis.Redis(
    host=Settings().HOST_REDIS, 
    port=Settings().PORT_REDIS,
    db=0,
    decode_responses=True
)

class ConnectionRedis:
    @staticmethod
    def get_session_redis():
        """with redis_client.pipeline() as pipeline:
            return pipeline"""
        return redis_client