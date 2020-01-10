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
		tweets= t.search.tweets(q=f'{str(select)}{rawtext}', include_rts=False, tweet_mode='extended',count=100)

	#Get the tweet text (tw1) and and the sentiment (tw2), appened them to lists
	#Also counted how many elements there are in each list to make sure they match
		m_dict = tweets['statuses']

		tw_list_date = []
		tw_list_screen_name = []
		tw_list_text = []
		tw_list_retweet = []
		tw_list_likes = []
		tw_list_id = []
		tw_list_polarity = []
		for element in m_dict:
			tw_list_date.append(element['created_at'])
			tw_list_screen_name.append(element['user']['screen_name'])
			tw_list_text.append(element['full_text'])
			tw_list_retweet.append(element['retweet_count'])
			tw_list_likes.append(element['favorite_count'])
			tw_list_id.append(element['id'])
			analysis = TextBlob(element['full_text'])
			tw_list_polarity.append(analysis.sentiment.polarity)

		tw_df = pd.DataFrame(list(zip(tw_list_date, tw_list_screen_name, tw_list_text, tw_list_retweet, tw_list_likes, tw_list_id, tw_list_polarity)), columns =['created_date', 'handle', 'text', 'retweet_count', 'likes_count', 'tweet_id', 'polarity'])
		sentiment_list = [] 
		for value in tw_df["polarity"]: 
			if value == -1: 
				sentiment_list.append("Negative") 
			elif value > -1 and value < 0: 
				sentiment_list.append("Somewhat Negative")
			elif value == 0:
				sentiment_list.append('Neutral')
			elif value >= 0.1 and value <= 0.5:
				sentiment_list.append('Somewhat Postive')
			else: 
				sentiment_list.append("Positive") 
			
		tw_df['sentiment'] = sentiment_list
		tw_html = tw_df.to_html()
		tw_html2 = tw_html.replace('\n', '')

		return render_template('index.html',tw_html=tw_html2)




	else:
		rawtext = request.form['rawtext']
		token = '1212463191910842368-l00ryMICeXQXXawl8w2zazEoFS7xDf'
		token_secret = 'hbzjFRq1r2ygkydPXfrwrhm5zTa54F3mYEm2wi7Q09DgA'
		consumer_key = 'g8V7jnF3dqMfg4LRhtobYB4Pl'
		consumer_secret = 'Y0SHSL0H9X9gCtuy07mJ3cp144DS2JhwX4Uvgda2ph8NvIUswJ'

		t = Twitter(auth=OAuth(token, token_secret, consumer_key, consumer_secret))
		tweets= t.statuses.user_timeline(screen_name=f'{rawtext}', count=100, include_rts=False, tweet_mode = 'extended')

	#Get the tweet text (tw1) and and the sentiment (tw2), appened them to lists
	#Also counted how many elements there are in each list to make sure they match
		tw_list_date = []
		tw_list_screen_name = []
		tw_list_text = []
		tw_list_retweet = []
		tw_list_likes = []
		tw_list_id = []
		tw_list_polarity = []
		for element in tweets:
			tw_list_date.append(element['created_at'])
			tw_list_screen_name.append(element['user']['screen_name'])
			tw_list_text.append(element['full_text'])
			tw_list_retweet.append(element['retweet_count'])
			tw_list_likes.append(element['favorite_count'])
			tw_list_id.append(element['id'])
			analysis = TextBlob(element['full_text'])
			tw_list_polarity.append(analysis.sentiment.polarity)

		tw_df = pd.DataFrame(list(zip(tw_list_date, tw_list_screen_name, tw_list_text, tw_list_retweet, tw_list_likes, tw_list_id, tw_list_polarity)), columns =['created_date', 'handle', 'text', 'retweet_count', 'likes_count', 'tweet_id', 'polarity'])
		sentiment_list = [] 
		for value in tw_df["polarity"]: 
			if value == -1: 
				sentiment_list.append("Negative") 
			elif value > -1 and value < 0: 
				sentiment_list.append("Somewhat Negative")
			elif value == 0:
				sentiment_list.append('Neutral')
			elif value >= 0.1 and value <= 0.5:
				sentiment_list.append('Somewhat Postive')
			else: 
				sentiment_list.append("Positive") 
			
		tw_df['sentiment'] = sentiment_list
		tw_html = tw_df.to_html()
		tw_html2 = tw_html.replace('\n', '')

		return render_template('index.html',tw_html=tw_html2)

		
	#redered to display on page
	return render_template('index.html',tw1=tw1,tw2=tw2,count_tw1=count_tw1,count_tw2=count_tw2)






if __name__ == '__main__':
	app.run(debug=True)