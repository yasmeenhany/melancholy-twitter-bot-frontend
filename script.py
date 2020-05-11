import tweepy
import logging
import os
import time

logger = logging.getLogger()

def main():
    auth = tweepy.OAuthHandler(os.environ['TWITTER_CONSUMER_KEY'], os.environ['TWITTER_CONSUMER_SECRET'])
    auth.set_access_token(os.environ['ACCESS_KEY'], os.environ['ACCESS_SECRET'])

    # Create API object
    api = tweepy.API(auth)
    since_id = 2
    while True:
        api.update_status("Hi " + str(since_id))
        since_id = since_id+1
        logger.info("Waiting...")
        time.sleep(60)

if __name__ == "__main__":
    main()