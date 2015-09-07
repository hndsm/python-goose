import os, redis, json


class RedisCache(object):

    @classmethod
    def find_cached_value(self, key):
        redis_client = redis.from_url(os.environ['REDIS_URL'])
        try: 
            cached_rules = redis_client.get(key + '_' + os.environ['ENV'])

            if cached_rules:
                return json.loads(cached_rules)
        except Exception as error:
            return None

        return None

    @classmethod
    def cache_value(self, key, value, ttl=60 * 60 * 4):
        redis_client = redis.from_url(os.environ['REDIS_URL'])
        if ttl:
            redis_client.setex(key + '_' + os.environ['ENV'], json.dumps(value), ttl)
        else:
            redis_client.set(key + '_' + os.environ['ENV'], json.dumps(value))

    @classmethod
    def clear_value(self, key):
        redis_client = redis.from_url(os.environ['REDIS_URL'])
        redis_client.delete(key + '_' + os.environ['ENV'])
