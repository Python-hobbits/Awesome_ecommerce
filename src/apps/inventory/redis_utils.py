import redis


class RedisConnection:
    _instance = None

    def __new__(cls, host="localhost", port=6379, db=0):
        if cls._instance is None:
            cls._instance = super(RedisConnection, cls).__new__(cls)
            cls._instance._connection = redis.StrictRedis(host=host, port=port, db=db)
        return cls._instance

    def get_connection(self):
        return self._connection
