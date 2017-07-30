import tweepy
from tweepy import Stream
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from lib import config
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

twitter_stream = Stream(auth, MyListener())

# right now this array is copy/pasted output of domains.py -- temporary solution until we better understand filter()
# why are the periods removed from domains? => last paragraph under "track" https://dev.twitter.com/streaming/overview/request-parameters 
twitter_stream.filter(track=[
    '16WMPO com', '24online news', '24wpn com', '247NewsMedia com', 'ABCNews com co', 'actualidadpanamericana com', 'AlabamaObserver com', 'AmericanFlavor news', 'AmericanPeopleNetwork com', 'AmericanPoliticNews co', 'AmericanPresident co', 'AMPosts com', 'ANews24 org/', 'AngryPatriotMovement com', 'Anonjekloy tk', 'AssociatedMediaCoverage com', 'Aurora-News us', 'BB4SP com', 'BeforeItsNews com', 'BlackInsuranceNews com', 'BlueVision news', 'BlueVisionPost com', 'BostonLeader com', 'BostonTribune com', 'BuzzFeedUSA com', 'CannaSOS com', 'Channel18News com', 'ChristianTimesNewspaper com', 'ChristianToday info', 'CivicTribune com', 'CivicTribune com', 'ClashDaily com', 'CNNews3 com', 'Coed com', 'ConservativeDailyPost com', 'ConservativeFlashNews com', 'ConservativeInfoCorner com', 'ConservativeSpirit com', 'DailyInfoBox com', 'DailyNews10 com', 'DailyNews5 com', 'DailyNewsPosts info', 'DailySnark com', 'DailySurge com', 'DailyUSAUpdate com', 'DamnLeaks com', 'DemocraticMoms com', 'DenverInquirer com', 'DepartedMedia com', 'Disclose tv', 'DIYHours net', 'DonaldTrumpPOTUS45 com', 'EmpireHerald com', 'EmpireNews net', 'EmpireSports co', 'En-Volve com', 'ENHLive com', 'FederalistTribune com', 'FedsAlert com', 'FirstPost com', 'FlashNewsCorner com', 'FloridaSunPost com', 'FocusNews info', 'Fox-News24 com', 'FreedomDaily com', 'FreedomCrossroads us', 'FreedomsFinalStand com', 'FreeWoodPost com', 'FreshDailyReport com', 'GiveMeLiberty01 com', 'GlobalPoliticsNow com', 'GummyPost com', 'HealthyCareAndBeauty com', 'HealthyWorldHouse com', 'HoustonChronicle-TV com', 'ILoveNativeAmericans us', 'InterestingDailyNews com', 'IsThatLegit com', 'JewsNews co il', 'KMT11 com', 'Konkonsagh biz', 'KY12News com', 'LadyLibertysNews com', 'LastDeplorables com', 'LearnProgress org', 'Liberty-Courier com', 'LiberalPlug com', 'LibertyAlliance com', 'Local31News com', 'MadWorldNews com', 'MajorThoughts com', 'Mentor2day com', 'MetropolitanWorlds com', 'MIssissippiHerald com', 'NationalReport net', 'NativeAmericans us', 'NBC com co', 'NeonNettle com', 'Nephef com', 'NewPoliticsToday com', 'News4KTLA com', 'NewsBreaksHere com', 'NewsBreakingsPipe com', 'NewsBySquad com', 'NewsDaily12 com', 'NewsExaminer net', 'NewsLeak co', 'Newslo com', 'NewsJustForYou1 blogspot com', 'NewzMagazine com', 'NotAllowedTo com', 'Now8News com', 'OccupyDemocrats com', 'OnePoliticalPlaza com', 'OpenMagazines com', 'Politicalo com', 'Politicass com', 'Politicono com', 'Politicops com', 'Politicot com', 'PoliticsUSANews com', 'President45DonaldTrump com', 'Prntly com', 'ProudLeader com', 'ReadConservatives news', 'RealNewsRightNow com', 'RedCountry us', 'RedInfo us', 'RedRockTribune com', 'Religionlo com', 'ReligionMind com', 'Rogue-Nation3 com', 'RumorJournal com', 'SatiraTribune com', 'Smag31 com', 'SocialEverythings com', 'SouthernConservativeExtra com', 'Spinzon com', 'States-TV com', 'Success-Street com', 'SupremePatriot com', 'TDTAlliance com', 'TeaParty org', 'ThatViralFeed net', 'The-Insider co', 'ThePremiumNews com', 'The-Postillon com', 'TheBigRiddle com', 'TheInternetPost net', 'TheLastLineOfDefense org', 'TheMoralOfTheStory us', 'TheNationalMarijuanaNews com', 'TheNet24h com', 'TheNewYorkEvening com', 'ThePoliticalInsider com', 'TheRightists com', 'TheSeattleTribune com', 'TheTrumpMedia com', 'TheUSA-News com', 'TheUSAConservative com', 'TheWashingtonPress com', 'Times com mx', 'TMZWorldNews com', 'TrueAmericans me', 'TrueTrumpers com', 'UndergroundNewsReport com', 'UniversePolitics com', 'UrbanImageMagazine com', 'USA-Radio com', 'USA-Television com', 'USADailyInfo com', 'USADailyPost us', 'USADailyTime com', 'USADoseNews com', 'USAFirstInformation com', 'USANews4U us', 'USANewsToday com', 'USAPoliticsNow com', 'USAPolitics24hrs com', 'USAPoliticsToday com', 'USAPoliticsZone com', 'USASnich com', 'USATodayNews me', 'USAWorldBox com', 'USHealthyAdvisor com', 'USHealthyLife com', 'USHerald com', 'USInfoNews com', 'USANewsHome com', 'USPOLN com', 'USPostman com', 'ViralActions com', 'VoxTribune com', 'WashingtonEvening com', 'WashingtonFeed com', 'WashingtonPost com co', 'WeConservative com', 'WeLoveNative com', 'WorldNewsDailyReport com', 'WorldPoliticsNow com'
])