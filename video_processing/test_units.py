import pytest 
import configparser 
import os
import twitter_Image_Video as TIV
import tweepy as tp 

def test_files():
  assert os.path.exists('keys')
  assert os.path.exists('main.py')
  assert os.path.exists('twitter_Image_Video.py')
  assert os.path.exists('ImageToVideo.py')
  assert os.path.exists('twitter_video/')
  assert os.path.exists('twitter_images/')
  assert os.path.exists('character_type/arial.ttf')

def test_api_keys():
  config = configparser.ConfigParser()
  config.read('keys')

  auth = tp.OAuthHandler(config.get('auth', 'consumer_key').strip(), 
                          config.get('auth', 'consumer_secret').strip())
  auth.set_access_token = (config.get('auth', 'access_token').strip(),
                           config.get('auth', 'access_secret').strip()) 
  api = tp.API(auth)
  twitter = TIV.status("keys")

  try:
    profile_url = twitter.download_pro_url('BU')
    tweets = twitter.download_tweets('BU')
    TIV.Tweets2image('BU', profile_url, tweets)
    assert os.path.exists('twitter_images/BU_img1.png')
  except tp.error.TweepError:
    assert False

