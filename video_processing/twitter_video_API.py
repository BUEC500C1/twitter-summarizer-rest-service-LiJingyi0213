from video_processing import twitter_Image_Video as TIV
import threading
import time
import queue


def tweets2image2video_process(q,twitter):
  while not q.empty():  
    username = q.get()

    print("\ngrab "+username+" tweets is processing...")

    profile_url = twitter.download_pro_url(username)

    tweets = twitter.download_tweets(username)

    TIV.Tweets2image(username, profile_url, tweets)

    print("\n"+username+" image to video is processing...")

    TIV.imgToVideo(username) 

    print ("\n"+"done")

def Q_input(q1, twitter):
    count = 1
    while not q1.empty():  
        t_t2i = threading.Thread(name=r"tweets2image2video_process_{count}", 
                                  target=tweets2image2video_process, 
                                   args=(q1,twitter))
        t_t2i.start()  
        count = count+1




