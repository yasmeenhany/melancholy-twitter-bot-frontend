import tweepy
import logging
import os
import time
import datetime

logger = logging.getLogger()

def main():
    now = datetime.datetime.now().time()
    print(now.hour == 22 and now.minute==7)
    auth = tweepy.OAuthHandler(os.environ['TWITTER_CONSUMER_KEY'], os.environ['TWITTER_CONSUMER_SECRET'])
    auth.set_access_token(os.environ['ACCESS_KEY'], os.environ['ACCESS_SECRET'])

    # Create API object
    api = tweepy.API(auth)
    since_id = 2
    while True:
        now = datetime.datetime.now().time()
        if (now.hour == 22 and now.minute == 12) or (now.hour == 4 and now.minute == 0):
            api.update_status("Hi " + now)
            since_id = since_id+1
            logger.info("Waiting...")

if __name__ == "__main__":
    main()