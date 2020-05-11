import tweepy
import logging
import os
import time
import datetime

logger = logging.getLogger()

def main():
    auth = tweepy.OAuthHandler(os.environ['TWITTER_CONSUMER_KEY'], os.environ['TWITTER_CONSUMER_SECRET'])
    auth.set_access_token(os.environ['ACCESS_KEY'], os.environ['ACCESS_SECRET'])

    # Create API object
    api = tweepy.API(auth)

    while True:
        now = datetime.datetime.now().time()
        if (now.hour == 20 and now.minute == 59) or (now.hour == 14 and now.minute == 0):
            api.update_status("hi from " + str(now))
            time.sleep(62)

if __name__ == "__main__":
    main()