import redis
import json
import sys

client = redis.StrictRedis(decode_responses=True)

# for key in client.scan_iter("*qTest*"):
def main():
    # print(sys.argv[1:]) #if empty returns empty list
    for key in client.scan_iter():
        print('keyBef', key)
        if key in sys.argv[1:]:
            print('\ncaught: ', key, '\n')
    print ('\n')
    for key in client.scan_iter():
        print('keyAft', key)

if __name__ == "__main__":
    # sys.argv[1:]
    main()
