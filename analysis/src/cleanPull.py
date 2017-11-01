import redis
import json

client = redis.StrictRedis(decode_responses=True)

# for key in client.scan_iter("*qTest*"):
def main():
    for key in client.scan_iter():
        print('keyBef', key)
        if key=="qTest:Alex" or 'p:' in key or 'data:' in key:
            continue
        client.delete(key)
        # print ('key', key)
    for key in client.scan_iter():
        print('keyAft', key)

if __name__ == "__main__":
    main()

# Delete single client
# client.delete('p:testfafs')
