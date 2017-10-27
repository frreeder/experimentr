import redis
import json

client = redis.StrictRedis(decode_responses=True)

# for key in client.scan_iter("*qTest*"):
for key in client.scan_iter():
    print('keyB', key)
    if key=="qTest:Alex" or 'p:' in key or 'data:' in key:
        continue
    client.delete(key)
    print ('key', key)
