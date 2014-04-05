import tweepy
import json

from secrets import *


class TestListener(tweepy.StreamListener):
    
    def on_data(self, data):
        # Figure out what to do with the tweet, do it.
        # TODO (jmagnarelli): write this
        decoded = json.loads(data)

        # Also, we convert UTF-8 to ASCII ignoring all bad characters sent by users
        print('@{0}: {1}'.format(decoded['user']['screen_name'], decoded['text'].encode('ascii', 'ignore')))

    def on_error(self, status):
        print('AHHHHHHHHHHH {0}'.format(status))

if __name__ == '__main__':

    listener = TestListener()
    auth = tweepy.OAuthHandler(twit_api_key, twit_api_secret)
    auth.set_access_token(twit_oauth_token, twit_oauth_secret)

    stream = tweepy.Stream(auth, listener)
    stream.filter(follow=['22197119'])