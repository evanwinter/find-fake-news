import tweepy
from tweepy import Stream
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
import config
import json
import sys
import domains

# authenticate with twitter
auth = OAuthHandler(config.consumer_key, config.consumer_secret)
auth.set_access_token(config.access_token, config.access_secret)

api = tweepy.API(auth)

if (not api):
	print ("Can't authenticate")
	sys.exit(-1)

print("\nGetting tweets with links with problem domains...")

# stream
class MyListener(StreamListener):

    # called for each new tweet
    def on_data(self, tweet):
        
        try:
            with open('tweets.json', 'a') as f:
                
                # make it a dictionary
                tweetdict = json.loads(tweet)

                is_quote_status = tweetdict['is_quote_status']
                tweet_urls = ''

                # if this is not a "quote retweet" (nesting/embedding another users tweet in your tweet)
                if (is_quote_status == False):
                    # look for this status's list of urls
                    tweet_urls = tweetdict['entities']['urls']
                else:
                    # look for quote status's list of urls
                    tweet_urls = tweetdict['quoted_status']['entities']['urls']


                # if list of urls actually has urls in it
                if (len(tweet_urls) > 0):
                    # get the full (expanded) url
                    full_url = tweet_urls[0]['expanded_url']

                    if (full_url is not None):

                        # write the full tweet data to tweets.json
                        f.write(json.dumps(tweetdict, indent=4, sort_keys=True)+'\n')

                        print('\nTweet stored.')
                        print(full_url)

                    else:
                        pass
                else:
                    pass

                return True

        except BaseException as e:
            print("Error on_data: %s\n" % str(e))
            return True # don't kill stream

    def on_error(self, tweet):
        print(tweet)
        return True	# don't kill stream

# Process domain data
try:
    with open('domains.txt') as domainListFile:
        domains=domainListFile.read().split(' ')
        domains=[domain.replace(".", " ") for domain in domains] #Remove periods
        domains=[domain.replace("com co", "com.co") for domain in domains] #keep com.co 's

except BaseException as e:
    print("Error on_data: %s\n" % str(e))


twitter_stream = Stream(auth, MyListener())

# right now this array is copy/pasted output of domains.py -- temporary solution until we better understand filter()
# why are the periods removed from domains? => last paragraph under "track" https://dev.twitter.com/streaming/overview/request-parameters
twitter_stream.filter(track=domains)