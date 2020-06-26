import tweepy
import logging
import os
import time
import datetime
import requests
import re
from http.client import IncompleteRead

logger = logging.getLogger()

# Comment if testing ONLY
auth = tweepy.OAuthHandler(os.environ['TWITTER_CONSUMER_KEY'], os.environ['TWITTER_CONSUMER_SECRET'])
auth.set_access_token(os.environ['ACCESS_KEY'], os.environ['ACCESS_SECRET'])

# Global Variables
api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)
# Comment if testing ONLY
baseURL = 'https://a7zan-bot.herokuapp.com/'

class MyStreamListener(tweepy.StreamListener):

    def on_error(self, status_code):
        if status_code == '420':
            print(status_code)
            time.sleep(900)
            return False

    def on_status(self, tweet):
        self.api = api
        text = tweet.text
        # Comment if testing ONLY
        textRegex = re.compile(re.escape('@a7zanbot '), re.IGNORECASE)
        text = textRegex.sub('', text)
        if re.match(
                " *[wW][oO][uU][lL][dD] [yY][oO][uU] [kK][iI][nN][dD][lL][yY] [pP][lL][aA][yY] .* [bB][yY] .*",
                text):
            m = re.search('[pP][lL][aA][yY] (.*) [bB][yY]', text)
            m2 = re.search('[bB][yY] (.*)', text)
            if m and m2:
                song_name = m.group(1)
                artist = m2.group(1)
                song_name.replace(' ', '%20')
                artist.replace(' ', '%20')
            requests.post(baseURL + 'updateAPI')
            payload = {'query': song_name, 'artistName': artist}
            resp = requests.get(baseURL + 'getSongByArtist', params=payload)
            if resp.status_code == 200:
                data = resp.json()
                link = data['url']
                artist = data['artist']
                name = data['title']
                reply_text = "Requested By: @" + tweet.user.screen_name + " " + link
                tweetResponse = self.api.update_status(reply_text)
                self.api.create_favorite(tweet.id)
                payload = {'query': name.replace('%2520', '%20'), 'artistName': artist.replace('%2520', '%20')}
                spotifyUrl = requests.get(baseURL + 'getSongByArtistSpotify', params=payload)
                if spotifyUrl.status_code == 200:
                    spotifyData = spotifyUrl.json()
                    self.api.update_status(status=spotifyData['songUrl'], in_reply_to_status_id=tweetResponse.id)
                songID = link.split('/song/')[1]
                playlist_payload = {'songID': songID, 'songURI': spotifyData['uri'] }
                requests.get(baseURL + 'updateAccumulatorPlaylist',params= playlist_payload )

            else:
                reply_text = '@' + tweet.user.screen_name + " The song you asked for was not found, please try another song"
                self.api.update_status(
                    status=reply_text,
                    in_reply_to_status_id=tweet.id
                )
        else:
            reply_text = '@' + tweet.user.screen_name + ' Please use the following format when you request a song: Would you ' \
                                                        'kindly play {song name} by {artist}'
            self.api.update_status(
                status=reply_text,
                in_reply_to_status_id=tweet.id
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

def get_build_message(api):
    try:
        resp = requests.get(baseURL + 'getBuildStatus')
        if resp.status_code == 200:
            data = resp.json()
            available = data['available']
            if not available:
                return
            else:
                announcement = data['text']
                data['available'] = False
                data['text'] = ''
                api.update_status(announcement)
                requests.post(url=baseURL + 'updateBuildStatus', json=data)
    except tweepy.RateLimitError:
        print('sleep 15 minutes')
        time.sleep(900)
    except tweepy.TweepError as e:
        print(e)
    except Exception as e:
        print(e)


def timed_tweets(api):
    now = datetime.datetime.now().time()
    if (now.hour == 21 and now.minute == 00) or (now.hour == 14 and now.minute == 0):
        try:
            requests.post(baseURL + 'updateAPI')
            resp = requests.get(baseURL + 'latestSong')
            if resp.status_code == 200:
                data = resp.json()
                link = data['url']
                artist = data['artist']
                name = data['title']
                tweetResponse = api.update_status(link + " #" + ''.join(e for e in artist if e.isalnum()))
                resp = requests.post(baseURL + 'updateIndex')
                payload = {'query': name.replace('%2520', '%20'), 'artistName': artist.replace('%2520', '%20')}
                spotifyUrl = requests.get(baseURL + 'getSongByArtistSpotify', params=payload)
                if spotifyUrl.status_code == 200:
                    spotifyData = spotifyUrl.json()
                    api.update_status(status=spotifyData['songUrl'], in_reply_to_status_id=tweetResponse.id)

                songID = link.split('/song/')[1]
                playlist_payload = {'songID': songID, 'songURI': spotifyData['uri'] }
                requests.get(baseURL + 'updateAccumulatorPlaylist',params= playlist_payload )

        except tweepy.RateLimitError:
            print('sleep 15 minutes')
            time.sleep(900)
        except tweepy.TweepError as e:
            print(e)
        except Exception as e:
            print(e)
        else:
            pass

        time.sleep(62)


def main():
    # tweepy.debug(True)
    myStreamListener = MyStreamListener(api)
    myStream = tweepy.Stream(auth=auth, listener=myStreamListener)
    get_build_message(api)

    while True:
        timed_tweets(api)
        try:
            if not myStream.running:
                print("Stream is up")
               # Comment if testing ONLY 
                myStream.filter(track=['@a7zanbot would you kindly play'], is_async=True, filter_level='low',
                            stall_warnings=True)
        except KeyboardInterrupt as e:
            print("Stopped.")
            myStream.disconnect()
        except IncompleteRead as e:
            print('Stream down, restarting...')
            continue
        except Exception as e:
            print(e)
            continue


if __name__ == "__main__":
    main()
