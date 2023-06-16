import redis

client = redis.Redis(host="192.168.13.175", port=6379)

client.flushall()
