import redis
from datetime import timedelta
import os
from dotenv import load_dotenv


load_dotenv()

REDIS_DEFAULT_TTL = os.getenv("REDIS_DEFAULT_TTL")
REDIS_PORT = os.getenv("REDIS_PORT")
REDIS_HOST = os.getenv("REDIS_HOST")

class cache():
    def __init__(self, db_id=0, rport=REDIS_PORT, rhost=REDIS_HOST, key_ttl=REDIS_DEFAULT_TTL) -> None:
        self.client = redis.Redis(host=rhost, port=rport, db=db_id)
        self.mttl = int(key_ttl)
        pass

    def insert(self, key, value):
        self.client.setex(key, timedelta(seconds=self.mttl), value)
        return

    def getKey(self, key):
        v = self.client.get(key)
        if v:
            return v.decode("utf-8")
        return None





# app_cache = cache(db_id=0)
# url_cache = cache(db_id=1)

# url_cache.insert('key1', "value")
# print(url_cache.getKey('key1'))
# u = url_cache.getKey('key')
# print(u)
# app_cache.insert('key1', "value")
# print(app_cache.getKey('key1'))
