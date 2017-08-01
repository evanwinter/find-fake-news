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

print("\nGetting tweets with links...")

# stream
class MyListener(StreamListener):

    # called for each new tweet
    def on_data(self, tweet):
        
        try:
            with open('tweets.json', 'a') as f:
                
                # make it a dictionary
                tweetdict = json.loads(tweet)

                # find the list of urls in the tweet data
                tweet_urls = tweetdict['entities']['urls']

                if (len(tweet_urls) > 0):
                    
                    full_url = tweet_urls[0]['expanded_url']

                    if (full_url is not None):

                        # write the full tweet data
                        f.write(json.dumps(tweetdict, indent=4, sort_keys=True))

                        # or just the url
                        # f.write(json.dumps(full_url, indent=4, sort_keys=True)+'\n')

                        print('\nTweet stored.')
                        print(full_url)

                    else:
                        # print('Has no expanded URL')
                        # print('Tweet DISCARDED')
                        pass

                else:
                    # print('Has no URLs')
                    # print('Tweet DISCARDED')
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