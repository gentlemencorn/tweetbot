import tweepy
from tweepy.streaming import StreamListener
import logging
import csv

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

# Use your credentials
auth_token = ''
auth_secret = ''
consumer_key = ''
consumer_secret = ''

#connecting to API
auth = tweepy.OAuthHandler(consumer_key=consumer_key,
                           consumer_secret=consumer_secret)
auth.set_access_token(auth_token, auth_secret)

api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

# File path for csv
file_path = ''


# Create stream class
class Listener(StreamListener):

    def on_status(self, status):
    ''' print streamed tweets in terminal (commented out by default), writes tweets to csv '''
        # print(status.author.screen_name, status.created_at, status.text.encode('utf-8'))
        with open(file_path, 'a') as file:
            writer = csv.writer(file)
            writer.writerow([status.author.screen_name, status.created_at, status.text.encode('utf-8')])

    def on_error(self, status_code):
        if status_code == 420:
            return False


# Write CSV headers
with open(file_path, 'w') as f:
    writer = csv.writer(f)
    writer.writerow(['Author', 'Date', 'Text'])

# Connect to streaming API 
streamingAPI = tweepy.streaming.Stream(auth, Listener())

# Streaming tweets, update track with desired tweet filters as a list of strings
try:
    print('Starting stream')
    streamingAPI.filter(track=[''])
except KeyboardInterrupt:
    print('Ending Stream')
finally:
    streamingAPI.disconnect()
    with open(file_path, 'r') as file:
        tweet_count = sum(1 for row in file)
    print(f'Done. Streamed {tweet_count - 1} tweets')
