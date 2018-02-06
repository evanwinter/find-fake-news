import config
import json

from py_ms_cognitive import PyMsCognitiveNewsSearch
from time import sleep

topic = input("Enter in the topic: ")
print("\nGathering news articles about "+topic)

#Search for articles using Bing's News Search API
search_service = PyMsCognitiveNewsSearch(config.bing_search_api_key, topic)
articles = search_service.search(limit=50,format='json') #first 50 articles


try:
        with open(topic.title().replace(' ', '')+'.json', 'a') as f:

            for article in articles:
                f.write(json.dumps(article.json, indent=4, sort_keys=True)+'\n')
                print("Saving article with title: " + article.name)
                sleep(0.2) # add a little delay for saucy complexity ;)

except BaseException as e:
        print("Error on_data: %s\n" % str(e))