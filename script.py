import tweepy
import logging
import os
import time
import datetime
import requests
import re

logger = logging.getLogger()


class MyStreamListener(tweepy.StreamListener):

    def on_status(self, tweet):
        baseURL = 'https://a7zan-bot.herokuapp.com/'
        print(tweet.text)

        print(tweet.text)
        text = tweet.text
        textRegex = re.compile(re.escape('@a7zanbot'), re.IGNORECASE)
        text = textRegex.sub('', text)
        if re.match(
                "[wW][oO][uU][lL][dD] [yY][oO][uU] [kK][iI][nN][dD][lL][yY] [pP][lL][aA][yY] .* [bB][yY] .*",
                text):
            m = re.search('[pP][lL][aA][yY] (.*) [bB][yY]', text)
            m2 = re.search('[bB][yY] (.*)', text)
            if m and m2:
                song_name = m.group(1)
                artist = m2.group(1)
                song_name.replace(' ', '%')

            payload = {'query': song_name, 'artistName': artist}
            resp = requests.get(baseURL + 'getSongByArtist', params=payload)
            if resp.status_code == 200:
                data = resp.json()
                link = data['url']
                reply_text = link + " Requested By: @" + tweet.user.screen_name
                self.api.update_status(reply_text)
            else:
                reply_text = "The song you asked for was not found, please try another song"
                self.api.update_status(
                    status=reply_text,
                    in_reply_to_status_id=tweet.id,
                )
        else:
            reply_text = 'Please use the following format when you request a song: Would you ' \
                         'kindly play {song name} by {artist}'
            self.api.update_status(
                status=reply_text,
                in_reply_to_status_id=tweet.id,
            )


# def check_mentions(baseURL, api, since_id):
#     print(since_id)
#     logger.info("Retrieving mentions")
#     new_since_id = since_id
#     for tweet in tweepy.Cursor(api.mentions_timeline,
#                                since_id=since_id).items():
#         if tweet is None:
#             return since_id
#
#         new_since_id = max(int(tweet.id), int(new_since_id))
#
#         if tweet.in_reply_to_status_id is not None:
#             continue
#         else:
#             print(tweet.text)
#             if tweet is None:
#                 return since_id
#             text = tweet.text
#             text = text.split(' ', 1)[1]
#
#             if re.match("[wW][oO][uU][lL][dD] [yY][oO][uU] [kK][iI][nN][dD][lL][yY] [pP][lL][aA][yY] .* [bB][yY] .*",
#                         text):
#                 m = re.search('[pP][lL][aA][yY] (.*) [bB][yY]', text)
#                 m2 = re.search('[bB][yY] (.*)', text)
#                 if m and m2:
#                     song_name = m.group(1)
#                     artist = m2.group(1)
#                     song_name.replace(' ', '%')
#
#                 payload = {'query': song_name, 'artistName': artist}
#                 resp = requests.get(baseURL + 'getSongByArtist', params=payload)
#                 if resp.status_code == 200:
#                     data = resp.json()
#                     link = data['url']
#                     reply_text = link + " Requested By: @" + tweet.user.screen_name
#                 # api.update_status(reply_text)
#                 else:
#                     reply_text = "The song you asked for was not found, please try another song"
#                     # api.update_status(
#                     #   status=reply_text,
#                     #   in_reply_to_status_id=tweet.id,
#                     # )
#             else:
#                 reply_text = 'Please use the following format when you request a song: Would you ' \
#                              'kindly play {song name} by {artist}'
#             #  api.update_status(
#             #     status=reply_text,
#             #    in_reply_to_status_id=tweet.id,
#             # )
#
#             print(reply_text)
#     if new_since_id is None:
#         return since_id
#     else:
#         return new_since_id


def timed_tweets(baseURL, api):
    now = datetime.datetime.now().time()
    if (now.hour == 20 and now.minute == 00) or (now.hour == 14 and now.minute == 0):
        try:
            resp = requests.get(baseURL + 'latestSong')
            if resp.status_code == 200:
                data = resp.json()
                link = data['url']
                artist = data['artist']
                #print(link)
                api.update_status(link + " #" + ''.join(e for e in artist if e.isalnum()))
        except tweepy.RateLimitError:
            print('sleep 15 minutes')
            time.sleep(900)
        except tweepy.TweepError as e:
            print(e)
        except Exception as e:
            print(e)
        else:
            pass
            resp = requests.post(baseURL + 'updateIndex')

        time.sleep(62)


def main():
    auth = tweepy.OAuthHandler(os.environ['TWITTER_CONSUMER_KEY'], os.environ['TWITTER_CONSUMER_SECRET'])
    auth.set_access_token(os.environ['ACCESS_KEY'], os.environ['ACCESS_SECRET'])

    # Global Variables
    api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)
    baseURL = 'https://a7zan-bot.herokuapp.com/'
    #tweepy.debug(True)
    myStreamListener = MyStreamListener()
    myStream = tweepy.Stream(auth=api.auth, listener=myStreamListener)
    myStream.filter(track=['@a7zanbot'], is_async=True)
    while True:
        timed_tweets(baseURL, api)


if __name__ == "__main__":
    main()
