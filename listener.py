import tweepy
import json
import logging
import pymongo
import re
from twilio.rest import TwilioRestClient

from secrets import *


# Build this stuff up in advance because it makes things easier

logging.basicConfig(level=logging.DEBUG)
# Define emergency service uids here
BALTIMORE_PD_ID = 22197119
BALTIMORE_FIRE_ID = 46669448

# For determining what to listen to given a region
REGIONS_TO_UIDS = {'Baltimore': [BALTIMORE_PD_ID, BALTIMORE_FIRE_ID]}

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
        text = tweet['text']
        CRIME_KEYWORDS = ("shooting", "crime", "suspect", "gun", "custody", "silver", "alert", "on the scene", "working fire")
        for word in CRIME_KEYWORDS:
            if word in text:
                logging.info("Tweet with id {0} was criminal activity".format(tweet['id']))
                return True

        return False

class MessageSender(object):
    """Handles sending tweets through twilio"""

    def __init__(self, db):
        self.twilio_client = TwilioRestClient(twilio_key, twilio_secret)
        self.db = db

    def send_tweet(self, tweet):
        cur_region = UIDS_TO_REGIONS[tweet['user']['id']]
        recipients = self.db.users.find({'region': cur_region})
        for recipient in recipients: 
            dest_phone = recipient['phone_number']
            logging.info("Sending SMS message to {0}".format(dest_phone))
            message = self.twilio_client.sms.messages.create(body="WOOOO BITCAMP", to=dest_phone, from_="+17813281143")


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
    logging.info("Beginning stream...")
    stream.filter(follow=['2429573322'])#str(BALTIMORE_PD_ID), str(BALTIMORE_FIRE_ID)])


if __name__ == '__main__':
    _main()