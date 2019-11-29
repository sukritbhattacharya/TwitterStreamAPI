from flask import Flask, render_template, request, send_file, flash, redirect, session, abort, url_for, jsonify
import json
import requests
import tweepy
from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
import pandas as pd

app = Flask(__name__)

app.config['SECRET_KEY'] = 'cbddedf099deb363e9fc1d8ad4b186c4'

#Twitter Keys
custkey = 'EfyNZGFazzEgjgWklcQX9pVtL'
custsecret = 'OISER7tJh7QwPo1Zx1NYDnxA6tFDD02qpuF4RUoKa0a6PORJIv'
accessToken = '2997451130-Bb1S123zoGGLkDg8hwGn6JksLf8Esmzy63A2Per'
accessSecret = 'yolh5Ss32yyyS7iT1I073MVsJ8uMDzoojaMvBtomD4XpS'


@app.route('/', methods=['POST','GET'])
def home():
    tweets = []
    if request.method == 'POST':
        if request.form['submit'] == 'SEARCH':
            payload = {'keyword' : request.form.get('search')}
            print(payload)
            getTweet(payload['keyword'])

            # .txt to json array list
            tweets = []
            i = 0
            filename = 'tweets.txt'
            for line in open(filename, 'r'):
                line1 = json.loads(line)
                print(type(line1))
                print("-----------")
                tweets.append(line1)
                i = i + 1

            for i in tweets:
                print(i['id'])

            return render_template('home.html', tweet = tweets)

    return render_template('home.html', tweet = tweets)



def getTweet(keyword):


    print("Tweets Loading up!!")

    class listener(StreamListener):
        def __init__(self, api=None):
            super(listener, self).__init__()
            self.num_tweets = 0
            self.file = open("tweets.txt", "w+")

        def on_status(self, status):
            tweet = status._json

            self.file.write( json.dumps(tweet) + '\n' )

            self.num_tweets += 1
            if self.num_tweets < 10:
                return True
            else:
                return False
            self.file.close()

        def on_error(self, status):
            print(status)


    auth = OAuthHandler(custkey, custsecret)
    auth.set_access_token(accessToken, accessSecret)
    twitterStream = Stream(auth,listener())
    twitterStream.filter(track=[keyword])


@app.route('/notifications')
def about():
    return render_template('notifications.html', title = 'About')


if __name__ == '__main__':
    app.run(port =6002 , debug = True)
