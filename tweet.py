from __future__ import unicode_literals
import os
import tweepy
from tweepy import OAuthHandler
from selenium import webdriver
from bs4 import BeautifulSoup
from dotenv import load_dotenv
load_dotenv()

browser = webdriver.Chrome('/media/arungovindm/DATA1/twitter-bot/chromedriver')

url = "https://covidfightclub.org/"

browser.get(url)

get_source = browser.page_source

soup = BeautifulSoup(get_source, 'html.parser')
medicine_list = soup.find_all("div", {"class": ["info-tag badge badge-warning",
                                                "detail-row city", "detail-row contact-name", "detail-row medicine-name", "detail-row note", "detail-row phone"]})
browser.quit()
j = 0
l = []
for i in medicine_list:
    j += 1
    a = " ".join(i.text.split())
    l.append(a)
    if(j % 6 == 0):
        break

print(l)

badge = l[0]
city = l[1]
contactName = l[2]
requirement = l[3]
info = l[4]
phone = l[5]

auth = tweepy.OAuthHandler(os.environ.get(
    "CONSUMER_KEY"), os.environ.get("CONSUMER_SECRET"))
auth.set_access_token(os.environ.get("ACCESS_TOKEN"),
                      os.environ.get("ACCESS_TOKEN_SECRET"))

api = tweepy.API(auth)

tweet = "This is a {} \nLocation: {} \nName: {} \nRequirement: {} \nInfo: {} \nContact No: {}".format(
    l[0], l[1], l[2], l[3], l[4], l[5])

# api.update_status(status=tweet)
print("DONE")
