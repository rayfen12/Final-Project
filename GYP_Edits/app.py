from flask import Flask, render_template,request,url_for
from flask_bootstrap import Bootstrap 
import numpy as np
from twitter import *
import pandas as pd 
import datetime


from textblob import TextBlob,Word 
import random 
import time

app = Flask(__name__)
Bootstrap(app)

@app.route('/')
def index():
	return render_template('index.html')


@app.route('/analyse',methods=['POST'])
def analyze():
	start = time.time()
	select = request.form.get('comp_select')
	#get the raw text from the input box
	if request.method == 'POST' and select != "hdl":	
		rawtext = request.form['rawtext']
		

	#Twitter API tokens	
		token = '1212463191910842368-l00ryMICeXQXXawl8w2zazEoFS7xDf'
		token_secret = 'hbzjFRq1r2ygkydPXfrwrhm5zTa54F3mYEm2wi7Q09DgA'
		consumer_key = 'g8V7jnF3dqMfg4LRhtobYB4Pl'
		consumer_secret = 'Y0SHSL0H9X9gCtuy07mJ3cp144DS2JhwX4Uvgda2ph8NvIUswJ'

	#Call Twitter API to request tweets with the $rawtext (using the $ for now for testing)
		t = Twitter(auth=OAuth(token, token_secret, consumer_key, consumer_secret))
		tweets= t.search.tweets(q=f'{str(select)}{rawtext}', include_rts=False, tweet_mode='extended')

	#Get the tweet text (tw1) and and the sentiment (tw2), appened them to lists
	#Also counted how many elements there are in each list to make sure they match
		tweet_list = tweets['statuses']
		tw1=[]
		tw2=[]
		for i in tweet_list:
			tw1.append(i['full_text'])
			analysis = TextBlob(i['full_text'])
			tw2.append(analysis.sentiment.polarity)
		count_tw1 = len(tw1)
		count_tw2 = len(tw2)

	else:
		rawtext = request.form['rawtext']
		token = '1212463191910842368-l00ryMICeXQXXawl8w2zazEoFS7xDf'
		token_secret = 'hbzjFRq1r2ygkydPXfrwrhm5zTa54F3mYEm2wi7Q09DgA'
		consumer_key = 'g8V7jnF3dqMfg4LRhtobYB4Pl'
		consumer_secret = 'Y0SHSL0H9X9gCtuy07mJ3cp144DS2JhwX4Uvgda2ph8NvIUswJ'

		t = Twitter(auth=OAuth(token, token_secret, consumer_key, consumer_secret))
		tweets= t.statuses.user_timeline(screen_name=f'{rawtext}', count=20, include_rts=False, tweet_mode = 'extended')

	#Get the tweet text (tw1) and and the sentiment (tw2), appened them to lists
	#Also counted how many elements there are in each list to make sure they match
		tw1 = []
		tw2 = []
		for x in tweets:
			tw1.append(x['full_text'])
			analysis = TextBlob(x['full_text'])
			tw2.append(analysis.sentiment.polarity)
		count_tw1 = len(tw1)
		count_tw2 = len(tw2)
		
	#redered to display on page
	return render_template('index.html',tw1=tw1,tw2=tw2,count_tw1=count_tw1,count_tw2=count_tw2)






if __name__ == '__main__':
	app.run(debug=True)