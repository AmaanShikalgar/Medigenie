import redis
import os
from dotenv import load_dotenv
load_dotenv()
import json

class Redis:
    def __init__(self):
        self.client = redis.StrictRedis(
                            host=os.getenv('REDIS_HOST'), 
                            port=os.getenv('REDIS_PORT'), 
                            db=os.getenv('REDIS_DB')
                        )

    def set(self, key, value, expiry=None):
        key = str(key)
        value = json.dumps(value)
        self.client.set(key, value)
        if expiry:
            self.client.expire(key, time=int(expiry))
        else:
            self.client.expire(key, time=int(os.getenv('REDIS_EXPIRY_TIME')))

    def get(self, key):
        return json.loads(self.client.get(key))
    
    def keys(self):
        return self.client.keys()
    
    def flush(self):
        self.client.flushall()
    
    def exists(self, key):
        return self.client.exists(key)
    
    def expire(self, key, time):
        self.client.expire(key, time)
    
    def time_to_live(self, key):
        return self.client.ttl(key)
    


cache = Redis()