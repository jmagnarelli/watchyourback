import tweepy
import json
import pymongo
from twilio.rest import TwilioRestClient

from secrets import *


# Build this stuff up in advance because it makes things easier

# Define pd uids here
BALTIMORE_PD_ID = 22197119

# For determining what to listen to given a region
REGIONS_TO_UIDS = {'baltimore': [BALTIMORE_PD_ID]}

# For lookup when we receive a tweet and all we have is a uid
UIDS_TO_REGIONS = {}
for k, v in REGIONS_TO_UIDS.iteritems():
    for uid in v:
        UIDS_TO_REGIONS[uid] = k


class TweetAnalyzer(object):
    """Encapsulates all of the tweet analysis logic"""

    @staticmethod
    def is_criminal(tweet):
        """Return whether the tweet is evidence of criminal activity or not"""
        # TODO (jmagnarelli): write this
        return True

class MessageSender(object):
    """Handles sending tweets through twilio"""

    def __init__(self, db):
        self.twilio_client = TwilioRestClient(twilio_key, twilio_secret)


    def send_tweet(self, tweet):
        cur_region = UIDS_TO_REGIONS[tweet['user']['id']]
        recipients = db.users.find({'region': cur_region})
        for recipient in recipients: 
            message = self.twilio_client.sms.messages.create(body="WOOOO BITCAMP", to=recipient, from_="+17813281143")

class TestListener(tweepy.StreamListener):
    
    def __init__(self, db, sender):
        super(TestListener, self).__init__()
        self.db = db
        self.sender = sender

    def on_data(self, data):
        # Figure out what to do with the tweet, do it.
        # TODO (jmagnarelli): write this
        decoded = json.loads(data)

        # Also, we convert UTF-8 to ASCII ignoring all bad characters sent by users
        print('@{0}: {1}'.format(decoded['user']['screen_name'], decoded['text'].encode('ascii', 'ignore')))

        if TweetAnalyzer.is_criminal(decoded):
            self.sender.send_tweet(decoded)

    def on_error(self, status):
        print('AHHHHHHHHHHH {0}'.format(status))

def _main():



    db = pymongo.MongoClient().user_data
    sender = MessageSender(db)

    listener = TestListener(db, sender)
    auth = tweepy.OAuthHandler(twit_api_key, twit_api_secret)
    auth.set_access_token(twit_oauth_token, twit_oauth_secret)

    stream = tweepy.Stream(auth, listener)
    stream.filter(follow=[str(BALTIMORE_PD_ID)])


if __name__ == '__main__':
    _main()