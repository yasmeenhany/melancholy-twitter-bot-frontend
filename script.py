import tweepy
import logging
import os
import time

logger = logging.getLogger()

def main():
    auth = tweepy.OAuthHandler("BDVShCnQXMk9wa2xM0AwV1KAK", "vbOj1ngtQs7keRMSXDCJfFDtPK2Eh20N8fhw5ollIxVuyr1oEE")
    auth.set_access_token("1222834478445408256-t7mcEiLMNa7w6Sw4wOKXrskDRlBiTo", "ftxdMWZKYZUGnp5ymbKe56JOYbO1yIu2jYS7sYeSssWLa")

    # Create API object
    api = tweepy.API(auth)
    since_id = 1
    while True:
        api.update_status("Hi " + str(since_id))
        since_id = since_id+1
        logger.info("Waiting...")
        time.sleep(180)

if __name__ == "__main__":
    main()