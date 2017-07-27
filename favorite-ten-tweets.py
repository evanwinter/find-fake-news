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