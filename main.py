import tweepy
from tweepy import Stream
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
import config
import json
import sys

auth = OAuthHandler(config.consumer_key, config.consumer_secret)
auth.set_access_token(config.access_token, config.access_secret)
 
api = tweepy.API(auth)

# make sure we authenticate
if (not api):
	print ("Can't authenticate")
	sys.exit(-1)

# start getting tweets
print("\nGetting flu-related tweets...\n")

class MyListener(StreamListener):
 
    # def on_status(self, tweet):
    #     try:
    #         with open('tweets.txt', 'a') as f:
    #             f.write(tweet.text+'\n')
    #             print("Tweet Stored:\n"+tweet.text+"\n")
    #             return True
    #     except BaseException as e:
    #         print("Error on_status: %s\n" % str(e))
    #     return True # don't kill stream

    def on_data(self, tweet):
        try:
            with open('tweets.json', 'a') as f:
            	f.write(json.dumps(json.loads(tweet), indent=4, sort_keys=True))
            	# print("Tweet Stored:\n"+tweet.text+"\n")
            	return True
        except BaseException as e:
            print("Error on_status: %s\n" % str(e))
        return True # don't kill stream
 
    def on_error(self, tweet):
        print(tweet)
        return True	# don't kill stream
 
twitter_stream = Stream(auth, MyListener())
twitter_stream.filter(track=['flu'])