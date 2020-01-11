from flask import Flask, render_template,request,url_for,Markup
from flask_bootstrap import Bootstrap 
import numpy as np
from twitter import *
import pandas as pd 
import datetime
import plotly.graph_objects as go
import plotly.io as pio
from textblob import TextBlob,Word 
import random 
import time
import Credentials 
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
		token = Credentials.token
		token_secret = Credentials.token_secret
		consumer_key = Credentials.consumer_key
		consumer_secret = Credentials.consumer_secret

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
		#tw_list_id = []
		tw_list_polarity = []
		for element in m_dict:
			tw_list_date.append(element['created_at'])
			tw_list_screen_name.append(element['user']['screen_name'])
			tw_list_text.append(element['full_text'])
			tw_list_retweet.append(element['retweet_count'])
			tw_list_likes.append(element['favorite_count'])
			#tw_list_id.append(element['id'])
			analysis = TextBlob(element['full_text'])
			tw_list_polarity.append(analysis.sentiment.polarity)

		tw_df = pd.DataFrame(list(zip(tw_list_date, tw_list_screen_name, tw_list_text, tw_list_retweet, tw_list_likes, tw_list_polarity)), columns =['Date', 'Handle', 'Text', 'No_of_retweets', 'No_of_likes', 'Polarity'])
		sentiment_list = [] 
		for value in tw_df["Polarity"]: 
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
			
		tw_df['Sentiment'] = sentiment_list
		tw_html = tw_df.to_html()
		tw_html2 = tw_html.replace('\n', '')

		scatter = go.Figure(go.Scatter(tw_df, x="No_of_likes", y="Polarity", size="No_of_likes", color="Sentiment",
           hover_name="Handle", log_x=True, size_max=60))
		pio.write_html(scatter, file='scatter.html', auto_open=True)

		return render_template('index.html',tw_html=tw_html2,scatter=scatter)

		# scatter = go.Figure(go.Scatter(tw_df, x="No_of_likes", y="Polarity", size="No_of_likes", color="Sentiment",
        #    hover_name="Handle", log_x=True, size_max=60))
		# pio.write_html(scatter, file='scatter.html', auto_open=True)

		# return render_template('scatter.html')
	else:
		rawtext = request.form['rawtext']
		token = Credentials.token
		token_secret = Credentials.token_secret
		consumer_key = Credentials.consumer_key
		consumer_secret = Credentials.consumer_secret

		t = Twitter(auth=OAuth(token, token_secret, consumer_key, consumer_secret))
		tweets= t.statuses.user_timeline(screen_name=f'{rawtext}', count=100, include_rts=False, tweet_mode = 'extended')

	#Get the tweet text (tw1) and and the sentiment (tw2), appened them to lists
	#Also counted how many elements there are in each list to make sure they match
		tw_list_date = []
		tw_list_screen_name = []
		tw_list_text = []
		tw_list_retweet = []
		tw_list_likes = []
		#tw_list_id = []
		tw_list_polarity = []
		for element in tweets:
			tw_list_date.append(element['created_at'])
			tw_list_screen_name.append(element['user']['screen_name'])
			tw_list_text.append(element['full_text'])
			tw_list_retweet.append(element['retweet_count'])
			tw_list_likes.append(element['favorite_count'])
			#tw_list_id.append(element['id'])
			analysis = TextBlob(element['full_text'])
			tw_list_polarity.append(analysis.sentiment.polarity)

		tw_df = pd.DataFrame(list(zip(tw_list_date, tw_list_screen_name, tw_list_text, tw_list_retweet, tw_list_likes, tw_list_polarity)), columns =['Date', 'Handle', 'Text', 'No_of_retweets', 'No_of_likes', 'Polarity'])
		sentiment_list = [] 
		for value in tw_df["Polarity"]: 
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
			
		tw_df['Sentiment'] = sentiment_list
		tw_html = tw_df.to_html()
		tw_html2 = tw_html.replace('\n', '')

		return render_template('index.html',tw_html=tw_html2)

		# scatter = go.Figure(go.Scatter(tw_df, x="No_of_likes", y="Polarity", size="No_of_likes", color="Sentiment",
        #    hover_name="Handle", log_x=True, size_max=60))
		# pio.write_html(scatter, file='scatter.html', auto_open=True)

		# return render_template('scatter.html')
		
	#redered to display on page
	return render_template('index.html',tw1=tw1,tw2=tw2,count_tw1=count_tw1,count_tw2=count_tw2)






if __name__ == '__main__':
	app.run(debug=True)