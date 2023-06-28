import os, json, tweepy, time
import configparser

# Initialising settings file
config = configparser.ConfigParser()
config.read("settings")
settings = config['BotSettings']

# Getting Twitter API Keys
consumer_key = settings["consumer_key"]
consumer_secret = settings["consumer_secret"]
access_token = settings["access_token"]
access_token_secret = settings["access_token_secret"]

# Initialising Twitter API Client v2
Client = tweepy.Client(consumer_key=consumer_key,
                        consumer_secret=consumer_secret,
                        access_token=access_token,
                        access_token_secret=access_token_secret)
time.sleep(1)

# Twitter API v1 for media upload
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

# Function for choosing screencap & sub
def get_content(lines):
    screencaps_path = settings["screencaps_path"]
    images_list = os.listdir(screencaps_path)
    subsjson_raw = open("titanic-subs.json", 'r', encoding="utf-8")
    subsjson = json.load(subsjson_raw)
    last_ID = int(lines[-1].split("= ")[-1].split('\n')[0])
    content = subsjson[last_ID+1]
    current_ID = content['ID']
    timestamp = content['timestamp']
    seconds = content['seconds']
    subs = content['subs']
    cap_time = int(int(seconds) * 23.97)
    while True:
        found = False
        for image in images_list:
            if int(image.split("_")[1].split(".")[0]) == cap_time:
                found = True
                screencap = os.path.join(screencaps_path, image)
                break
        if found:
            break
        else:
            cap_time-=1
    return current_ID,timestamp,subs,screencap

with open("settings", 'r', encoding="utf-8") as settings_file:
    lines = settings_file.readlines()
id,timestamp,sub,screencap = get_content(lines)
tweet_text = f'\U000027A1 {timestamp}\n{sub}'

media = api.media_upload(screencap)
media_id = media.media_id
tweet = Client.create_tweet(media_ids=[media_id], text=tweet_text)
tweet_id = tweet[0]["id"]
print(f'ID: {id}\nPosted: {sub}\nTweetID: {tweet_id}')
lines[-1] = "last_tweet_id = " + str(id)    
with open("settings", 'w', encoding="utf-8") as settings_file:
    settings_file.writelines(lines)
