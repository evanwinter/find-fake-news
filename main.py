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
print("\nGetting tweets...\n")

class MyListener(StreamListener):

    def on_data(self, tweet):
        try:
            with open('tweets.json', 'a') as f:
                tweetdict = json.loads(tweet)
                # only store data if it fits our criteria
                if ("fake news" in tweetdict['text'] and "RT" not in tweetdict['text']):
                    # write to json and make it pretty
                    f.write(json.dumps(tweetdict, indent=4, sort_keys=True))

                    # log it
                    print("Tweet stored.")
                    print(tweetdict['text'])
                    print()

                else:
                    # print("Tweet not stored")
                    pass
                return True
        except BaseException as e:
            print("Error on_status: %s\n" % str(e))
            return True # don't kill stream
    def on_error(self, tweet):
        print(tweet)
        return True	# don't kill stream
 
twitter_stream = Stream(auth, MyListener())
twitter_stream.filter(track=['fake news'])