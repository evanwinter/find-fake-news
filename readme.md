# finding fake news 

### From Politifact: "To help you better sort out fact from fiction on the Internet we created this list of websites where we've found *deliberately false or fake stories. This is by no means a complete list of offenders. Nor does it mean every post on these websites is fake. But in most cases, these sites work hard to fool readers*, and you should take that into consideration if should you see a link being shared from one. This list is up to date as of May 16, 2017."

## objectives

* collect list of problem domains (http://www.politifact.com/punditfact/article/2017/apr/20/politifacts-guide-fake-news-websites-and-what-they/)
* watch for tweets that link to articles on these domains
* using NLP, determine whether or not the tweets are saying 'i agree with/believe this' or if they're saying 'this is dumb/fake'
* on a map, show where these tweets are coming from
* incorporate capacity to 'learn' new problem domains, add them to list of domains to watch for

## usage

* install python
* create config.py file and enter your Twitter API Credentials
* run `python3 links.py`