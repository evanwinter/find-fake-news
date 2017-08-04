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
    print("Can't authenticate")
    sys.exit(-1)




topic = input("Enter in the topic: ")
print("\nGetting tweets with links about "+topic)

# stream
class MyListener(StreamListener):
    # called for each new tweet
    def on_data(self, tweet):

        try:
            with open(topic.replace(' ', '')+'.json', 'a') as f:

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
                        f.write(json.dumps(tweetdict, indent=4, sort_keys=True) + '\n')

                        print('\nTweet stored.')
                        print(full_url)

                    else:
                        pass
                else:
                    pass

                return True

        except BaseException as e:
            print("Error on_data: %s\n" % str(e))
            return True  # don't kill stream

    def on_error(self, tweet):
        print(tweet)
        return True  # don't kill stream


twitter_stream = Stream(auth, MyListener())
twitter_stream.filter(track=[''+topic+''])