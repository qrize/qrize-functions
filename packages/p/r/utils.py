import os
import redis

def get_redis_host():
    print(redis)
    return os.getenv('REDIS_HOST')