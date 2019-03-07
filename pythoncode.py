import pandas as pd
import numpy as np
import tweepy
import sys
import csv 
import json
# For plotting and visualization:
from IPython.display import display
import matplotlib.pyplot as plt
import seaborn as sns

#%matplotlib inline

arg1 = sys.argv[1]
# Twitter App access keys for @user

# Consume:
CONSUMER_KEY    = 'lR9oj5YrkuIh856ZUkmDFKeb3'
CONSUMER_SECRET = '8GSD5C2UNTidabat7VU5wyC64fsL9Y78xxMxoC0zyqb0fYgnDM'

# Access:
ACCESS_TOKEN  = '166222763-481zjE8eP7bgZMQXfLx9v2oijV5QKxYpLPSl9n8f'
ACCESS_SECRET = '3GPbSHU5LWOa4w3V8xZIjbicMjo7QXwlj1tF3tI14zGtR'

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)

auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)

api = tweepy.API(auth)

#for tweet in sys.argv[1]
tweets = api.search(sys.argv[1])
#tweets = api.search("\"Data Localization\"")

#for tweet in tweets:
 #   print(tweet.text)
    
data = pd.DataFrame(data=[tweet.text for tweet in tweets], columns=['Tweets'])
# We add relevant data:
data['Name']  = np.array([tweet.user.name for tweet in tweets])
data['Screen Name']  = np.array([tweet.user.screen_name for tweet in tweets])
data['Location']  = np.array([tweet.user.location for tweet in tweets])
data['Place']  = np.array([tweet.place for tweet in tweets])
#data['Hashtags']  = np.array([tweet.entities.hashtags for tweet in tweets])
#data['URL']  = np.array([tweet.entities.urls.url for tweet in tweets])
#data['URL_Unwound']  = np.array([tweet.entities.urls.unwound.url for tweet in tweets])
#data['URL_Title']  = np.array([tweet.entities.urls.unwound.title for tweet in tweets])
#data['Mentions']  = np.array([tweet.user_mentions for tweet in tweets])
data['len']  = np.array([len(tweet.text) for tweet in tweets])
data['ID']   = np.array([tweet.id for tweet in tweets])
data['Date'] = np.array([tweet.created_at for tweet in tweets])
data['Source'] = np.array([tweet.source for tweet in tweets])
data['Likes']  = np.array([tweet.favorite_count for tweet in tweets])
data['RTs']    = np.array([tweet.retweet_count for tweet in tweets])
# We display the first 10 elements of the dataframe:
#display(data.head(10))
#data.to_csv("raw_tweets.csv", sep=',', encoding='utf-8')

from textblob import TextBlob
import re

def clean_tweet(tweet):
    return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split())

def analize_sentiment(tweet):
    analysis = TextBlob(clean_tweet(tweet))
    if analysis.sentiment.polarity > 0:
        return 1
    elif analysis.sentiment.polarity == 0:
        return 0
    else:
        return -1


# We create a column with the result of the analysis:
data['SA'] = np.array([ analize_sentiment(tweet) for tweet in data['Tweets'] ])
#display(data)
# We display the updated dataframe with the new column:
data.to_csv("Sentiment-analysis.csv", sep=',', encoding='utf-8')
#display(data)


xyz = data.values.tolist()
#display(xyz)


# We construct lists with classified tweets:




pos_tweets = [ tweet for index, tweet in enumerate(data['Tweets']) if data['SA'][index] > 0]
neu_tweets = [ tweet for index, tweet in enumerate(data['Tweets']) if data['SA'][index] == 0]
neg_tweets = [ tweet for index, tweet in enumerate(data['Tweets']) if data['SA'][index] < 0]

# # We print percentages:

#print("Percentage of positive tweets: {}%".format(len(pos_tweets)*100/len(data['Tweets'])))
# print("Percentage of neutral tweets: {}%".format(len(neu_tweets)*100/len(data['Tweets'])))
# print("Percentage de negative tweets: {}%".format(len(neg_tweets)*100/len(data['Tweets'])))
pos = (len(pos_tweets)*100/len(data['Tweets']))
neu = (len(neu_tweets)*100/len(data['Tweets']))
neg = (len(neg_tweets)*100/len(data['Tweets']))
#data = [{'Positive': pos , 'Negative': 0, 'Neutral' : 0},{'Positive': 0 , 'Negative': neg, 'Neutral' : 0}, {'Positive': 0 , 'Negative': 0, 'Neutral' : neu}]
df = pd.DataFrame(data = {'Positive':[pos], 'Negative':[neg], 'Neutral':[neu]})
j = df.to_json(orient='records')
display(j)


import mysql.connector
mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  passwd="password",
  database="test"
)

mycursor = mydb.cursor()

sql = "INSERT INTO twitter (Tweets , Name , ScreenName ,Location , Place, len , ID , Date, Source , Likes,  RTs, SA ) VALUES (%s, %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"

mycursor.executemany(sql, (xyz))
mydb.commit()

#display(mycursor.rowcount, "was inserted.")
