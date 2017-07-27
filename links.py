import tweepy
from tweepy import Stream
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
import config
import json
import sys

# create twitter app, store consumer key & secret, access token & secret in config.py
auth = OAuthHandler(config.consumer_key, config.consumer_secret)
auth.set_access_token(config.access_token, config.access_secret)

api = tweepy.API(auth)

if (not api):
	print ("Can't authenticate")
	sys.exit(-1)

# start getting tweets
print("\nGetting tweets with links...\n")

class MyListener(StreamListener):

    def on_data(self, tweet):
        
        try:
            with open('links.json', 'a') as f:
                
                # make it a dictionary
                tweetdict = json.loads(tweet)

                print(tweetdict['entities']['urls'])
                
                # if it has a url in it
                if (tweetdict['entities']['urls']):
                    full_url = tweetdict['entities']['urls'][0]['expanded_url']
                    print(full_url)
                    
                    # store the tweet and make it pretty
                    f.write(json.dumps(tweetdict, indent=4, sort_keys=True))

                    print("Tweet stored.")
                    print()

                else:
                    pass

                return True

        except BaseException as e:
            print("Error on_data: %s\n" % str(e))
            return True # don't kill stream

    def on_error(self, tweet):
        print(tweet)
        return True	# don't kill stream
 
twitter_stream = Stream(auth, MyListener())
twitter_stream.filter(track=['fake news'])