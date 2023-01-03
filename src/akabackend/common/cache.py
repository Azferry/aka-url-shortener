import redis
from datetime import timedelta
import os
from dotenv import load_dotenv

load_dotenv()

REDIS_DEFAULT_TTL = os.getenv("REDIS_DEFAULT_TTL",8000)
REDIS_PORT = os.getenv("REDIS_PORT",6380)
REDIS_HOST = os.getenv("REDIS_HOST","localhost")
REDIS_PASS = os.getenv("REDIS_PASS")

class cache():
    def __init__(self, db_id=0, rport=REDIS_PORT, rhost=REDIS_HOST, key_ttl=REDIS_DEFAULT_TTL, rpass=REDIS_PASS) -> None:
        # self.client = redis.Redis(host=rhost, port=rport, db=db_id) # Conn to container
        
        self.client = redis.StrictRedis(host=rhost, port=rport, password=rpass, ssl=True,db=db_id)
        self.kttl = int(key_ttl)
        pass

    def insert(self, key, value):
        self.client.setex(key, timedelta(seconds=self.kttl), value)
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
