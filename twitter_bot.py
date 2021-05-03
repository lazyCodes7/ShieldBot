import re
import io
import csv
import tweepy
import logging
import time
from googlesearch import search
from bs4 import BeautifulSoup
from credentials import *
from tweepy import OAuthHandler
from dotenv import load_dotenv
import os
load_dotenv()
import requests, json


# Authenticate to Twitter
auth = tweepy.OAuthHandler(os.environ['CONSUMER_KEY'], os.environ['CONSUMER_SECRET'])
auth.set_access_token(os.environ['ACCESS_TOKEN'], os.environ['ACCESS_TOKEN_SECRET'])
api = tweepy.API(auth, wait_on_rate_limit=True)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

def return_hospitals(query):
    api_key=os.environ['API_KEY']
    return_text="These are the 5 hospitals near you\n"
    url = "https://maps.googleapis.com/maps/api/place/textsearch/json?"
    r = requests.get(url + 'query=' + query +'&key=' + api_key)
    x = r.json()
    y = x['results']
    for i in range(5):
        return_text+="{}.{}\n".format(i+1,y[i]['name'])
    return return_text
def check_mentions(api, keywords, since_id,counter):
    intro_text = "Hi I am ShieldBot. Please note that this DM here will not be attended to.\nInstructions for using the bot:\n1. Click on the feather icon on twitter for tweeting.\n2. Follow the pattern - @ShieldBot1 find <category> <city>(<city> can be replaced by <pincode> for hospitals)strictly\n3. Current Categories are:\n- beds\n- plasma\n- icu\n- food\n- oxygen\n- vaccine\n- hospitals\n4. City Names.\n Try keeping the city names as single word i.e New Delhi can be written as Delhi instead\n5. Response\n- Make sure to turn on dm from anyone in setting please\n- A DM would be then sent based on the request from the user tweet\n- If the first point was not done, a short reply would be sent instead\n"
    text = 'Please tell us what do you need help with.'
    options = [
            {
              "label": "Home ICU",
              "metadata": "external_id_1"
            },
            {
              "label": "Vaccination",
              "metadata": "external_id_2"
            },
            {
              "label": "Ambulance",
              "metadata": "external_id_3"
            },
            {
              "label": "Oxygen Concentrator",
              "metadata": "external_id_4"
            },
            {
              "label": "Ventilator",
              "metadata": "external_id_5"
            },
            {
              "label": "Beds",
              "metadata": "external_id_6"
            }
     ]
    logger.info("Retrieving mentions")
    new_since_id = since_id
    for tweet in tweepy.Cursor(api.mentions_timeline,
        since_id=since_id).items():
        new_since_id = max(tweet.id, new_since_id)
        if tweet.in_reply_to_status_id is not None:
            continue
        if any(keyword in tweet.text.lower() for keyword in keywords):
            logger.info(f"Answering to {tweet.user.name}")

            if not tweet.user.following:
                tweet.user.follow()

            id = tweet.user.screen_name
            print(id)
            text_arr = tweet.text.split()
            condition = text_arr[2]
            city = text_arr[3]
            prepare_text="Links for verified resources in {}".format(city)
            if(condition=="beds"):
                print(condition)
                try:
                    try:
                        api.update_status(

                            status="Sending dm for beds in {}!".format(city),
                            in_reply_to_status_id=tweet.id,
                            auto_populate_reply_metadata=True

                        )
                    except Exception as e2:
                        print(e2)
                        break
                    prepare_text="Hi {}. We hope that your situation is ok!. These are some curated resources that we have found in case the below link doesn't work.\n".format(id)
                    query = "verified covid resources {}".format(city)
                    i=0
                    for url in search(query):
                        i += 1
                        prepare_text+="{}.<{}>\n".format(i,url)
                        if(i==5):
    	                    break
                    link="verified%20beds%20-needed%20-requirement%20{}&f=live".format(city)
                    twitter_search="https://twitter.com/search?q={} ".format(link)
                    user_id = api.get_user(screen_name=id,include_entities=False)
                    try:
                        api.send_direct_message(recipient_id=user_id.id_str,text=intro_text)
                        api.send_direct_message(recipient_id=user_id.id_str,text=prepare_text)
                        api.send_direct_message(recipient_id=user_id.id_str,text="This is the link to find resources on twitter based on your city: {} ".format(twitter_search))
                    except Exception as err:
                        print(err)
                        api.update_status(
                            status="This is the link to find resources on twitter based on your city: {} . Please enable DM in settings for more!".format(twitter_search),
                            in_reply_to_status_id=tweet.id,
                            auto_populate_reply_metadata=True
                        )
                except Exception as e:
                    print(e)
                    print("Already updated before")
            elif(condition=="plasma"):
                print(condition)
                try:
                    try:
                        api.update_status(

                            status="Sending dm for plasma in {}!".format(city),
                            in_reply_to_status_id=tweet.id,
                            auto_populate_reply_metadata=True

                        )
                    except Exception as e2:
                        print(e2)
                        break
                    prepare_text="Hi {}. We hope that your situation is ok!. These are some curated resources that we have found in case the below link doesn't work.\n".format(id)
                    query = "verified covid resources {}".format(city)
                    i=0
                    for url in search(query):
                        i += 1
                        prepare_text+="{}.<{}>\n".format(i,url)
                        if(i==5):
    	                    break
                    link="verified%20{}%20Plasma%20-'not%20verified'%20-'un%20verified'%20-urgent%20-unverified%20-needed%20-required%20-need%20-needs%20-requirement&f=live".format(city)
                    twitter_search="https://twitter.com/search?q={}".format(link)

                    user_id = api.get_user(screen_name=id,include_entities=False)
                    try:
                        api.send_direct_message(recipient_id=user_id.id_str,text=intro_text)
                        api.send_direct_message(recipient_id=user_id.id_str,text=prepare_text)
                        api.send_direct_message(recipient_id=user_id.id_str,text="This is the link to find resources on twitter based on your city: {} ".format(twitter_search))
                    except Exception as err:
                        print(err)
                        api.update_status(
                            status="This is the link to find resources on twitter based on your city: {} . Please enable DM in settings for more!".format(twitter_search),
                            in_reply_to_status_id=tweet.id,
                            auto_populate_reply_metadata=True
                        )

                except Exception as e:
                    print(e)
                    print("Already updated before")
            elif(condition=="oxygen"):
                print(condition)
                try:
                    try:
                        api.update_status(

                            status="Sending dm for oxygen in {}!".format(city),
                            in_reply_to_status_id=tweet.id,
                            auto_populate_reply_metadata=True

                        )
                    except Exception as e2:
                        print(e2)
                        break

                    prepare_text="Hi {}. We hope that your situation is ok!. These are some curated resources that we have found in case the below link doesn't work.\n".format(id)
                    query = "verified covid resources {}".format(city)
                    i=0
                    for url in search(query):
                        i += 1
                        prepare_text+="{}.<{}>\n".format(i,url)
                        if(i==5):
    	                    break
                    link="verified%20{}%20Oxygen%20-'not%20verified'%20-'un%20verified'%20-urgent%20-unverified%20-needed%20-required%20-need%20-needs%20-requirement&f=live".format(city)


                    twitter_search="https://twitter.com/search?q={} ".format(link)
                    user_id = api.get_user(screen_name=id,include_entities=False)
                    try:
                        api.send_direct_message(recipient_id=user_id.id_str,text=intro_text)
                        api.send_direct_message(recipient_id=user_id.id_str,text=prepare_text)
                        api.send_direct_message(recipient_id=user_id.id_str,text="This is the link to find resources on twitter based on your city: {} ".format(twitter_search))
                    except Exception as err:
                        print(err)
                        api.update_status(
                            status="This is the link to find resources on twitter based on your city: {} . Please enable DM in settings for more!".format(twitter_search),
                            in_reply_to_status_id=tweet.id,
                            auto_populate_reply_metadata=True
                        )
                except Exception as e:
                    print(e)
                    print("Already updated before")
            elif(condition=="food"):
                print(condition)
                try:
                    try:
                        api.update_status(

                            status="Sending dm for food in {}!".format(city),
                            in_reply_to_status_id=tweet.id,
                            auto_populate_reply_metadata=True

                        )
                    except Exception as e2:
                        print(e2)
                        break                    
                    prepare_text="Hi {}. We hope that your situation is ok!. These are some curated resources that we have found in case the below link doesn't work.\n".format(id)
                    query = "verified covid resources {}".format(city)
                    i=0
                    for url in search(query):
                        i += 1
                        prepare_text+="{}.<{}>\n".format(i,url)
                        if(i==5):
    	                    break
                    link="verified%20{}%20food%20-'not%20verified'%20-'un%20verified'%20-urgent%20-unverified%20-needed%20-required%20-need%20-needs%20-requirement&f=live".format(city)


                    twitter_search="https://twitter.com/search?q={} ".format(link)
                    user_id = api.get_user(screen_name=id,include_entities=False)
                    try:
                        api.send_direct_message(recipient_id=user_id.id_str,text=intro_text)
                        api.send_direct_message(recipient_id=user_id.id_str,text=prepare_text)
                        api.send_direct_message(recipient_id=user_id.id_str,text="This is the link to find resources on twitter based on your city: {} ".format(twitter_search))
                    except Exception as err:
                        print(err)
                        api.update_status(
                            status="This is the link to find resources on twitter based on your city: {} . Please enable DM in settings for more!".format(twitter_search),
                            in_reply_to_status_id=tweet.id,
                            auto_populate_reply_metadata=True
                        )
                except Exception as e:
                    print(e)
                    print("Already updated before")
            elif(condition=="icu"):
                print(condition)
                try:
                    try:
                        api.update_status(

                            status="Sending dm for icu in {}!".format(city),
                            in_reply_to_status_id=tweet.id,
                            auto_populate_reply_metadata=True

                        )
                    except Exception as e2:
                        print(e2)
                        break
                    prepare_text="Hi {}. We hope that your situation is ok!. These are some curated resources that we have found in case the below link doesn't work.\n".format(id)
                    query = "verified covid resources {}".format(city)
                    i=0
                    for url in search(query):
                        i += 1
                        prepare_text+="{}.<{}>\n".format(i,url)
                        if(i==5):
    	                    break
                    link="verified%20{}%20icu%20-'not%20verified'%20-'un%20verified'%20-urgent%20-unverified%20-needed%20-required%20-need%20-needs%20-requirement&f=live".format(city)


                    twitter_search="https://twitter.com/search?q={} ".format(link)
                    user_id = api.get_user(screen_name=id,include_entities=False)
                    try:
                        api.send_direct_message(recipient_id=user_id.id_str,text=intro_text)
                        api.send_direct_message(recipient_id=user_id.id_str,text=prepare_text)
                        api.send_direct_message(recipient_id=user_id.id_str,text="This is the link to find resources on twitter based on your city: {} ".format(twitter_search))
                    except Exception as err:
                        print(err)
                        api.update_status(
                            status="This is the link to find resources on twitter based on your city: {} . Please enable DM in settings for more!".format(twitter_search),
                            in_reply_to_status_id=tweet.id,
                            auto_populate_reply_metadata=True
                        )
                except Exception as e:
                    print(e)
                    print("Already updated before")
            elif(condition=="vaccine"):
                print(condition)
                try:
                    try:
                        api.update_status(

                            status="Sending dm for vaccine info in {}!".format(city),
                            in_reply_to_status_id=tweet.id,
                            auto_populate_reply_metadata=True

                        )
                    except Exception as e2:
                        print(e2)
                        break
                    prepare_text="Hi {}. We hope that your situation is ok!. These are some curated resources that we have found in case the below link doesn't work.\n".format(id)
                    query = "verified covid resources {}".format(city)
                    i=0
                    for url in search(query):
                        i += 1
                        prepare_text+="{}.<{}>\n".format(i,url)
                        if(i==5):
    	                    break
                    link="verified%20{}%20vaccine%20-'not%20verified'%20-'un%20verified'%20-urgent%20-unverified%20-needed%20-required%20-need%20-needs%20-requirement&f=live".format(city)


                    twitter_search="https://twitter.com/search?q={} ".format(link)
                    user_id = api.get_user(screen_name=id,include_entities=False)
                    try:
                        api.send_direct_message(recipient_id=user_id.id_str,text=intro_text)
                        api.send_direct_message(recipient_id=user_id.id_str,text=prepare_text)
                        api.send_direct_message(recipient_id=user_id.id_str,text="This is the link to find resources on twitter based on your city: {} ".format(twitter_search))
                    except Exception as err:
                        print(err)
                        api.update_status(
                            status="This is the link to find resources on twitter based on your city: {} . Please enable DM in settings for more!".format(twitter_search),
                            in_reply_to_status_id=tweet.id,
                            auto_populate_reply_metadata=True
                        )
                except Exception as e:
                    print(e)
                    print("Already updated before")
            elif(condition=="hospitals"):
                print(condition)
                try:
                    try:
                        api.update_status(

                            status="Sending info for hospitals near {}!".format(city),
                            in_reply_to_status_id=tweet.id,
                            auto_populate_reply_metadata=True

                        )
                    except Exception as e2:
                        print(e2)
                        break
                    query = "hospitals near {}".format(city)
                    return_text = return_hospitals(query)
                    user_id = api.get_user(screen_name=id,include_entities=False)
                    try:
                        api.send_direct_message(recipient_id=user_id.id_str,text=intro_text)
                        api.send_direct_message(recipient_id=user_id.id_str,text=return_text)
                    except Exception as err:
                        print(err)
                        api.update_status(
                            status="Please enable DM in settings!",
                            in_reply_to_status_id=tweet.id,
                            auto_populate_reply_metadata=True
                        )
                except Exception as e:
                    print(e)
                    print("Already updated before")
                    
            


    return new_since_id
def handle_dms(api):
    our_id = ""
    options = [
            {
              "label": "Home ICU",
              "metadata": "external_id_1"
            },
            {
              "label": "Vaccination",
              "metadata": "external_id_2"
            },
            {
              "label": "Ambulance",
              "metadata": "external_id_3"
            },
            {
              "label": "Oxygen Concentrator",
              "metadata": "external_id_4"
            },
            {
              "label": "Ventilator",
              "metadata": "external_id_5"
            },
            {
              "label": "Beds",
              "metadata": "external_id_6"
            }
    ]

    user_msg = api.list_direct_messages(count=2)
    recipient_id = user_msg[-1].message_create['target']['recipient_id']
    print(int(recipient_id)==our_id)
    sender_id = user_msg[-1].message_create['sender_id']
    text = user_msg[1].message_create['message_data']['text']
    print(text)
    if(our_id==int(recipient_id)): 
        if(text=="help"):
            api.send_direct_message(recipient_id=sender_id, text="Please tell us what do you need help with",quick_reply_options=options)
        elif(text=="Beds"):
            api.send_direct_message(recipient_id=sender_id,text="Text me your city name")
    else:
        city="Nagpur"
        query = "verified bed OR beds -unverified -un verified -needed -required -need -needs -requirement {} since:2021-4-28".format(city)
        link="https://twitter.com/search?q={}".format(query)
        send_link = "Please visit this link for the resources.{}".format(link)
        api.send_direct_message(recipient_id=recipient_id,text=send_link)






def main(api):
    since_id=1
    counter = 6
    while True:
        counter+=1
        since_id = check_mentions(api, ["find", "beds","@ShieldBot1","Oxygen","Oxygen(Concentrator)","Plasma"], since_id,counter)
        time.sleep(900)


if __name__ == "__main__":
    main(api)
