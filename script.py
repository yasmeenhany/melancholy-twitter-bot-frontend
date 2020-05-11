import tweepy
import logging
import os
import time
import datetime

logger = logging.getLogger()

def main():
    now = datetime.datetime.now().time()
    print((now.hour == 22 and now.minute == 17) or (now.hour == 4 and now.minute == 0))
    auth = tweepy.OAuthHandler(os.environ['TWITTER_CONSUMER_KEY'], os.environ['TWITTER_CONSUMER_SECRET'])
    auth.set_access_token(os.environ['ACCESS_KEY'], os.environ['ACCESS_SECRET'])

    # Create API object
    api = tweepy.API(auth)
    while True:
        now = datetime.datetime.now().time()
        if (now.hour == 22 and now.minute == 25) or (now.hour == 16 and now.minute == 0):
            api.update_status("hi from " + str(now))
        print(str(now.hour) + "," + str(now.minute))

if __name__ == "__main__":
    main()