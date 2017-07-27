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

                print()
                
                # make it a dictionary
                tweetdict = json.loads(tweet)

                tweet_urls = tweetdict['entities']['urls']

                # if tweet has urls
                if (len(tweet_urls) > 0):
                    
                    print('has urls')
                    
                    # and if urls list has a full url
                    if (tweet_urls[0]['expanded_url'] is not None):
                        
                        full_url = tweet_urls[0]['expanded_url']
                        
                        # store the link
                        # f.write(json.dumps(full_url, indent=4, sort_keys=True)+'\n')

                        # store the whole tweet data
                        f.write(json.dumps(tweetdict, indent=4, sort_keys=True))
                        
                        print('** tweet stored **')

                    else:
                        print('no expanded url')
                        pass

                else:
                    print("no urls")
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