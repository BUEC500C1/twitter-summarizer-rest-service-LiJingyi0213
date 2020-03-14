from flask import Flask, send_from_directory,render_template, url_for, request, send_file,send_from_directory
from flask_restful import Resource, Api
from video_processing.twitter_video_API import tweets2image2video_process
from video_processing import twitter_Image_Video as TIV

from forms import RegistrationForm, LoginForm
import queue
import os
import time

app = Flask(__name__)
api = Api(app)
app.config['SECRET_KEY'] = '0bc62daa6ab42a07eec81ba61d8c2d96'
user_list = {
    'Nick' :{
                'user_id': 'Nick',
                'create_time':'Tue Aug  2 07:47:02 2016',
                'search_history':{},
                'twitter_id': { 'twitter_texts':[],
                                'twitter_images':[],
                                'twitter_videos':[]
                                }
                },
    'Jason': {
                'user_id': 'Jason',
                'create_time':'Tue Aug  5 07:47:02 2016',
                'search_history':{},
                'twitter_id': { 'twitter_texts':[],
                                'twitter_images':[],
                                'twitter_videos':[]
                                }
                }
}

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


@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html', title = 'tweets_video', 
                            user_list=user_list)


@app.route("/register")
def register():
    form = RegistrationForm()
    return render_template('register.html', title= 'register', 
                            form= form)

@app.route("/login")
def login():
    form = LoginForm()
    return render_template('login.html', title= 'login', 
                            form= form)

## search section 
# @app.route('/search')
# def search():
#     return render_template('search.html', title='search')

@app.route('/search')
@app.route("/search/<twitter_id>", methods= ['GET', 'POST'])
def get(twitter_id):
    return render_template('search.html', title= 'search', 
                                twitter_id= twitter_id) 


## return file for download
@app.route("/return-file/<filename>")
def return_files_tut(filename):
    path = os.path.join(app.root_path, 'video_processing/twitter_video')
    try:
        return send_from_directory(directory= path, filename= filename, 
                                    as_attachment=True)
    except Exception as e:
        return str(e)


if __name__ == '__main__':
    app.run(debug=True)