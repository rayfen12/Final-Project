from flask import Flask, render_template,request,url_for
from flask_bootstrap import Bootstrap 
import numpy as np
from twitter import *
import pandas as pd 
import datetime
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from textblob import TextBlob,Word 
import random 
import time
import plotly.express as px
import plotly as py
import plotly.graph_objs as go
from sklearn.feature_extraction.text import TfidfVectorizer
from collections import Counter
pd.set_option('display.max_colwidth', -1)



app = Flask(__name__)
Bootstrap(app)

@app.route('/')
def index():
	return render_template('index.html')


@app.route('/analyse',methods=['POST'])
def analyze():
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
		tweets= t.search.tweets(q=f'{str(select)}{rawtext}', include_rts=False, tweet_mode='extended',count=200)

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

		tw_df = pd.DataFrame(list(zip(tw_list_date, tw_list_screen_name, tw_list_text, tw_list_retweet, tw_list_likes, tw_list_polarity)), columns =['created_date', 'handle', 'text', 'retweet_count', 'likes_count', 'polarity'])
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
		# ================================================	
		tw_df['sentiment'] = sentiment_list
		tw_df1 = tw_df.loc[(tw_df['retweet_count'] >= 1) & (tw_df['retweet_count'] <= 70)]
		tw_html = tw_df1.to_html(classes=["table", "table-bordered", "table-striped", "table-hover"])
		tw_html2 = tw_html.replace('\n', '')
		# ================================================	
		average_sentiment = tw_df1["polarity"].mean()
		fig2 = go.Figure(go.Indicator(
			domain = {'x': [0, 1], 'y': [0, 1]},
			value = average_sentiment,
			mode = "gauge+number+delta",
			title = {'text': "Sentiment"},
			gauge = {'axis': {'range': [-1, 1]},
					'bar': {'color': "grey"},
					'steps' : [
						{'range': [-1, -0.5], 'color': "indianred"},
						{'range': [-0.5, 0], 'color': "red"},
						{'range': [0, 0.5], 'color': "lightgreen"},
						{'range': [0.5, 1], 'color': "green"}]}))
		fig3 = fig2.to_html()
		# ================================================	
		fig1 = px.scatter(tw_df1, x='retweet_count', y='polarity', hover_name="handle", color = 'sentiment')
		fig=fig1.to_html()
		# ================================================

		sorted_df= tw_df1.sort_values(by=['polarity'],ascending = False).head(1)
		# best_tweet = sorted_df[sorted_df['polarity'] == sorted_df['polarity'].max()].head(1)
		best_tweet = sorted_df
		filtered_best_tweet = best_tweet.drop(columns=['created_date', 'retweet_count', 'likes_count'])
		text1 = filtered_best_tweet.text.tolist()
		name1 = filtered_best_tweet.handle.tolist()
		pol1 = filtered_best_tweet.polarity.tolist()
		sorted_df1= tw_df1.sort_values(by=['polarity'],ascending = True).head(1)
		worst_tweet = sorted_df1
		# worst_tweet = sorted_df[sorted_df['polarity'] == sorted_df['polarity'].min()]
		filtered_worst_tweet = worst_tweet.drop(columns=['created_date', 'retweet_count', 'likes_count'])
		text2 = filtered_worst_tweet.text.tolist()
		name2 = filtered_worst_tweet.handle.tolist()
		pol2 = filtered_worst_tweet.polarity.tolist()
		return render_template('index.html',pol1 = pol1[0],pol2 = pol2[0],name2 = name2[0], text2 = text2[0],name1= name1[0],text1=text1[0],rawtext=rawtext,tw_html2=tw_html2,fig=fig,fig3 = fig3)




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

		tw_df = pd.DataFrame(list(zip(tw_list_date, tw_list_screen_name, tw_list_text, tw_list_retweet, tw_list_likes,  tw_list_polarity)), columns =['created_date', 'handle', 'text', 'retweet_count', 'likes_count', 'polarity'])
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
			
		# ================================================	
		tw_df['sentiment'] = sentiment_list
		tw_df1 = tw_df.loc[(tw_df['retweet_count'] >= 1) & (tw_df['retweet_count'] <= 50000)]
		tw_html = tw_df1.to_html(classes=["table", "table-bordered", "table-striped", "table-hover"])
		tw_html2 = tw_html.replace('\n', '')
		# ================================================	
		average_sentiment = tw_df1["polarity"].mean()
		fig2 = go.Figure(go.Indicator(
			domain = {'x': [0, 1], 'y': [0, 1]},
			value = average_sentiment,
			mode = "gauge+number+delta",
			title = {'text': "Sentiment"},
			gauge = {'axis': {'range': [-1, 1]},
					'bar': {'color': "grey"},
					'steps' : [
						{'range': [-1, -0.5], 'color': "indianred"},
						{'range': [-0.5, 0], 'color': "red"},
						{'range': [0, 0.5], 'color': "lightgreen"},
						{'range': [0.5, 1], 'color': "green"}]}))
		fig3 = fig2.to_html()
		# ================================================	
		fig1 = px.scatter(tw_df1, x='retweet_count', y='polarity', hover_name="handle", color = 'sentiment')
		fig=fig1.to_html()
		# ================================================
        
		vect = TfidfVectorizer(ngram_range=(2,5), stop_words='english')
		summaries = "".join(tw_df1['text'])
		ngrams_summaries = vect.build_analyzer()(summaries)
		word = Counter(ngrams_summaries).most_common(10)
		word_df = pd.DataFrame(word, columns=['common_words', 'word_count'])
		wordfig = px.bar(word_df,x='word_count',y='common_words', color = 'word_count',orientation = 'h',labels={'word_count':'Word Count', 'common_words': 'Common Words'}, height=400)
		wordfig1 = wordfig.to_html()

		# ========================================================
		sorted_df= tw_df1.sort_values(by=['polarity'],ascending = False).head(1)
		# best_tweet = sorted_df[sorted_df['polarity'] == sorted_df['polarity'].max()].head(1)
		best_tweet = sorted_df
		filtered_best_tweet = best_tweet.drop(columns=['created_date', 'retweet_count', 'likes_count'])
		text1 = filtered_best_tweet.text.tolist()
		name1 = filtered_best_tweet.handle.tolist()
		pol1 = filtered_best_tweet.polarity.tolist()
		sorted_df1= tw_df1.sort_values(by=['polarity'],ascending = True).head(1)
		worst_tweet = sorted_df1
		# worst_tweet = sorted_df[sorted_df['polarity'] == sorted_df['polarity'].min()]
		filtered_worst_tweet = worst_tweet.drop(columns=['created_date', 'retweet_count', 'likes_count'])
		text2 = filtered_worst_tweet.text.tolist()
		name2 = filtered_worst_tweet.handle.tolist()
		pol2 = filtered_worst_tweet.polarity.tolist()
		return render_template('index.html',pol1 = pol1[0],pol2 = pol2[0],name2 = name2[0], text2 = text2[0],name1= name1[0],text1=text1[0],wordfig1=wordfig1,rawtext=rawtext,tw_html2=tw_html2,fig=fig,fig3 = fig3)




if __name__ == '__main__':
	app.run(debug=True)