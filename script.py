import tweepy
import logging
import os
import time
import datetime
import requests
import re
logger = logging.getLogger()
# def check_mentions(baseURL, api, keywords, since_id):
#     logger.info("Retrieving mentions")
#     new_since_id = since_id
#     for tweet in tweepy.Cursor(api.mentions_timeline,
#         since_id=since_id).items():
#         new_since_id = max(tweet.id, new_since_id)
#         if tweet.in_reply_to_status_id is not None:
#             continue
#         if any(keyword in tweet.text.lower() for keyword in keywords):
#             logger.info(f"Answering to {tweet.user.name}")

#             if not tweet.user.following:
#                 tweet.user.follow()

#             text = tweet.full_text
#             if re.match(r"[wW][oO][uU][lL][dD] [yY][oO][uU] [kK][iI][nN][dD][lL][yY] [pP][lL][aA][yY] .* [bB][yY] .*", text):
#                 m = re.search('[pP][lL][aA][yY] (.*) [bB][yY]', text)
#                 m2 = re.search('[bB][yY] (.*)', text)
#                 if m and m2:
#                     song_name = m.group(1)
#                     artist = m2.group(1)
#                 payload = {'query': song_name , 'artistName': artist}
#                 resp = requests.get(baseURL + 'getSongByArtist', params = payload)
#                 if resp.status_code == 200:
#                     data = resp.json()
#                     link = data['url']
#                     reply_text = link
#             else:
#                 reply_text = ""


#             api.update_status(
#                 status=reply_text,
#                 in_reply_to_status_id=tweet.id,
#             )
#     return new_since_id
def main():
    auth = tweepy.OAuthHandler(os.environ['TWITTER_CONSUMER_KEY'], os.environ['TWITTER_CONSUMER_SECRET'])
    auth.set_access_token(os.environ['ACCESS_KEY'], os.environ['ACCESS_SECRET'])

    # Create API object
    api = tweepy.API(auth)
    baseURL = 'https://a7zan-bot.herokuapp.com/'
    while True:
        now = datetime.datetime.now().time()
        if (now.hour == 20 and now.minute == 0) or (now.hour == 14 and now.minute == 0):
            try:
                resp = requests.get(baseURL + 'latestSong')
                if resp.status_code == 200:
                    data = resp.json()
                    link = data['url']
                    api.update_status(link)
            except tweepy.RateLimitError:
               print('sleep 15 minutes')
               time.sleep(900)
               continue
            except tweepy.TweepError as e:
               print(e)
            except Exception as e: 
                print(e)
            else: 
                pass
                resp = requests.post(baseURL + 'updateIndex')

            time.sleep(62)
                

if __name__ == "__main__":
    main()