from flask import Flask, send_from_directory
from flask_restful import Resource, Api
from video_processing.twitter_video_API import tweets2image2video_process
from video_processing import twitter_Image_Video as TIV
import queue
import os
import time



app = Flask(__name__)
api = Api(app)

q1 = queue.Queue(maxsize=4)
twitter = TIV.status("keys")

class tweets(Resource):
  def get(self, twitter_id): 
      q1.put(twitter_id)
      path = os.path.join(app.root_path, 'video_processing/twitter_video/')     
      file_path = f'{path}{twitter_id}better.mp4'

      ## if mp4 and avi exist then delet
      if os.path.exists(file_path):
          os.remove(file_path)
          os.remove(f'{path}{twitter_id}normal.avi')

      tweets2image2video_process(q1,twitter)  
         
      for _ in range(4):
        if os.path.exists(file_path):
          return True
        time.sleep(2)
      return False


class download_video(Resource):
  def get(self, twitter_id):
      path = os.path.join(app.root_path, 'video_processing/twitter_video/') 
      filename = f'{twitter_id}better.mp4'   
      try :    
        return send_from_directory(directory= path, filename= filename, as_attachment= True)  
      except Exception as e:
        return str(e)


api.add_resource(tweets, '/search/<twitter_id>')
api.add_resource(download_video, '/download/<twitter_id>')

if __name__ == '__main__':
    app.run(debug=True)