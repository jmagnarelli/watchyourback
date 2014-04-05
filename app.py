import tweepy
import json
import pymongo

from secrets import *

BALTIMORE_PD_ID = '22197119'

class TestListener(tweepy.StreamListener):
    
    def __init__(self, db):
        super(TestListener, self).__init__()
        self.db = db

    def on_data(self, data):
        # Figure out what to do with the tweet, do it.
        # TODO (jmagnarelli): write this
        decoded = json.loads(data)

        # Also, we convert UTF-8 to ASCII ignoring all bad characters sent by users
        print('@{0}: {1}'.format(decoded['user']['screen_name'], decoded['text'].encode('ascii', 'ignore')))

    def on_error(self, status):
        print('AHHHHHHHHHHH {0}'.format(status))

def _main():
    db = pymongo.MongoClient().user_data
    listener = TestListener(db)
    auth = tweepy.OAuthHandler(twit_api_key, twit_api_secret)
    auth.set_access_token(twit_oauth_token, twit_oauth_secret)

    stream = tweepy.Stream(auth, listener)
    stream.filter(follow=[BALTIMORE_PD_ID])


if __name__ == '__main__':
    _main()