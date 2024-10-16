from redis import Redis
from redis.asyncio import Redis as AsyncRedis


class RedisDict(dict[str, object]):
    def __init__(self, redis: Redis | AsyncRedis, expiry: int = 3600):
        super().__init__()
        self.redis = redis
        self.expiry = expiry

    def __iter__(self):
        return iter(self.redis.keys())

    def __repr__(self):
        return f"<RedisDict {self.redis}>"

    def __len__(self):
        return self.redis.dbsize()

    def __getitem__(self, key):
        value = self.redis.get(key)
        if value is None:
            raise KeyError(key)
        return value

    def __setitem__(self, key, value):
        if self.expiry:
            self.redis.set(key, value, ex=self.expiry)
        self.redis.set(key, value)

    def __delitem__(self, key):
        if not self.redis.delete(key):
            raise KeyError(key)

    def __contains__(self, key: str):
        return self.redis.exists(key)

    def __del__(self):
        self.redis.close()
