import tweepy
from tweepy import Stream
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
import config
import json
import simplejson
import sys

auth = OAuthHandler(config.consumer_key, config.consumer_secret)
auth.set_access_token(config.access_token, config.access_secret)
 
api = tweepy.API(auth)

# make sure we authenticate
if (not api):
	print ("Can't authenticate")
	sys.exit(-1)

def favorite_ten_tweets():
	for tweet in tweepy.Cursor(api.home_timeline).items(10):
		# print the tweet
	    print("\n"+tweet.text)

	    # store the tweet data
	    process_or_store(tweet._json)

	    # add tweet to favorites
	    add_to_favorites(tweet)

def process_or_store(tweet):
	with open('data.txt', 'a') as outfile:
		json.dump(tweet, outfile, sort_keys = True, indent = 4,
		               ensure_ascii = False)

def add_to_favorites(tweet):
	if not tweet.favorited:
		try:
			api.create_favorite(tweet.id)
			print("Added to favorites.")
		except tweepy.TweepError:
			sys.exit("Tweep Error")
		except Exception as e:
			print(e)
			pass
	else:
		print("You already favorited this tweet.")
		pass


# start getting tweets
print("Getting flu-related tweets...\n")

# favorite and store ten most recent tweets from timeline
# favorite_ten_tweets()

class MyListener(StreamListener):
 
    def on_data(self, data):
        try:
            with open('tweets.json', 'a') as f:
                f.write(simplejson.dumps(simplejson.loads(data), indent=4, sort_keys=True))
                print("------------------\n-- tweet stored --\n------------------\n")
                return True
        except BaseException as e:
            print("Error on_data: %s" % str(e))
        return True
 
    def on_error(self, tweet):
        print(tweet)
        return True
 
twitter_stream = Stream(auth, MyListener())
twitter_stream.filter(track=['the flu'])
