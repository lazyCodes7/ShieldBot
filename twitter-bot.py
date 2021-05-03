import tweepy
import os
import json
from dotenv import load_dotenv
load_dotenv()

auth = tweepy.OAuthHandler(os.environ.get(
    "CONSUMER_KEY"), os.environ.get("CONSUMER_SECRET"))
auth.set_access_token(os.environ.get("ACCESS_TOKEN"),
                      os.environ.get("ACCESS_TOKEN_SECRET"))

api = tweepy.API(auth)

try:
    api.verify_credentials()
    print("Authentication OK")
except:
    print("Error during authentication")
