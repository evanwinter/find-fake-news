import tweepy
from tweepy import Stream
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
import config
import json
import simplejson
import sys

consumer_key = 'Yp9yjcxSIehmTCYjSDlHvNdeo'
consumer_secret = 'gsQ1cwmNJ6oUyN4q4N7C7aWivbpRIjCqG88mgEuWO037AgpNL5'
access_token = '879877809367392256-RbB41RJgmETZ6i7XnSHlC9orRsEenAR'
access_secret = '37NBYefr0BGarM4P2febFecG06kZOAa5h6gvoFdXXp6mn'

auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)
 
api = tweepy.API(auth)

# make sure we authenticate
if (not api):
	print ("Can't authenticate")
	sys.exit(-1)

# start getting tweets
print("\nGetting flu-related tweets...\n")

class MyListener(StreamListener):
 
    def on_data(self, tweet):
        try:
            with open('tweets.json', 'a') as f:
                f.write(simplejson.dumps(simplejson.loads(tweet), indent=4, sort_keys=True))
                print("tweet stored\n")
                return True
        except BaseException as e:
            print("Error on_data: %s" % str(e))
        return True # don't kill stream
 
    def on_error(self, tweet):
        print(tweet)
        return True	# don't kill stream
 
twitter_stream = Stream(auth, MyListener())
twitter_stream.filter(track=['the flu'])
