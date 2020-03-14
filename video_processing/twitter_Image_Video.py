import subprocess
import requests
import textwrap
import requests
import configparser 
import tweepy as tp 
import os
import json
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont


class status():

    def __init__(self, path):
        # getting twitter api keys from keys configuration file
        config = configparser.ConfigParser()
        config.read(path)

        # auth
        consumer_key = config.get('auth', 'consumer_key').strip()
        consumer_secret = config.get('auth', 'consumer_secret').strip()
        access_token = config.get('auth', 'access_token').strip()
        access_secret = config.get('auth', 'access_secret').strip()
        
        auth = tp.OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token = (access_token, access_secret) 

        self.api = tp.API(auth)
   
# getting the user 
    def download_pro_url(self, username):
        try:
            u = self.api.get_user(username)
            print ("\n successfully grab"+ username+"profile_url")
            return u.profile_image_url_https
        except tp.error.TweepError:
            return ""

  
    def download_tweets(self, username):
          try:
              tweets = self.api.user_timeline(screen_name=username, count=20, include_rts=True, result_type="recent",
                                      include_entities=True,
                                      tweet_mode='extended',
                                      lang="en")
              print ("\n successfully grab"+ username+"tweets")
              return tweets
          except tp.error.TweepError:
              return ""

def Tweets2image(user_id, profile_url, tweets):
    count = 0;
    tweets_content =[]
    for tweet in tweets:
        try :
            txt = tweet.full_text
            tweets_content.append(txt)
        except AttributeError:
            return
        count = count +1
        font = ImageFont.truetype(r'video_processing/character_type/arial.ttf', 14)
    
        background = Image.new('RGBA', (1024, 768), (255, 255, 255, 255))
        response = requests.get(profile_url)
    
        img = Image.open(BytesIO(response.content))
    
        draw = ImageDraw.Draw(background)
    
        lines = textwrap.wrap(txt, width=120)
    
        x, y = 50, 225
        for line in lines:
            width, height = font.getsize(line)
            draw.text(((x), y), line, font=font, fill="black")
            y += 15
    
        draw.text((120, 170), user_id, font=font, fill="black")
    
        offset = (50, 150)
    
        background.paste(img, offset)
    
        background.save(r'video_processing/twitter_images/'+ user_id +'_''img'+str(count)+'.png')
    # Serializing json  
    json_object = json.dumps(tweets_content, indent = 4) 
      
    # Writing to sample.json 
    with open('video_processing/json/'+user_id+'.json', "w") as outfile: 
        outfile.write(json_object) 

    print ("\n successfully create"+ user_id+ str(count)+"twitter_images")

def imgToVideo(username):
  
  fileName =  'video_processing/twitter_images/'+username +'_'+'img' +'%d'+'.png'
  
  avi =  "video_processing/twitter_video/" + username + "normal.avi"
  
  mp4 =  "video_processing/twitter_video/" + username + "better.mp4"
  
  subprocess.call(['ffmpeg', '-framerate', '0.3', '-i', fileName, avi])
  
  subprocess.call(['ffmpeg', '-i', avi, '-c:a', 'copy', '-c:v', 'copy', '-r', '30', '-s', 'hd720', '-b:v', '2M', mp4])
  
  print ("\n successfully create"+ username+"tweets_video")