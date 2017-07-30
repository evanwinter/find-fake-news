import pandas
import json

# gets only the urls from domains.csv and stores them in domains.txt
# eventually this should be moved to another script and automated
def get_urls():
    data = pandas.read_csv("domains.csv")
    urls = list(data['Site name'].values)
    with open('domains.txt', 'w') as outfile:
        outfile.write(json.dumps(urls))

get_urls()