# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
import logging
import requests
import json
from datetime import datetime
import random
logger = logging.getLogger(__name__)

API_URL = "https://api.cricapi.com/v1/currentMatches"
API_KEY = "d0b73bf4-e8fc-4d3b-a9d8-8b8b6467c36b"

class ApiAction(Action):
	def name(self):
		return "action_match_news"
	

	def run(self, dispatcher, tracker, domain):
		res = requests.get(API_URL + "?apikey=" + API_KEY+"&offset=0")
		if res.status_code == 200:
			result = res.json()
			num = random.randint(0, len(result['data'])-1)-1
			out_message = "Here some cricket quick info:\n1.The match between {} and {} was recently held and {} .".format(result['data'][num]['teams'][0], result['data'][num]['teams'][1], result['data'][num]['status'])

			dispatcher.utter_message(out_message)

			out_message = "2.The next match was between {} and {} was recently held and {} .".format(result['data'][num+1]['teams'][0], result['data'][num+1]['teams'][1], result['data'][num+1]['status'])

			dispatcher.utter_message(out_message)

		return []

# # Load dataset to get movie titles
# df = pd.read_csv('C:/Users/hp/Desktop/rasabot/rasachat/ML/wiki_movie_plots_deduped.csv', sep=',', usecols = ['Release Year','Title','Plot']) # use the full path
# df = df[df['Release Year'] >= 2000]
# # Load ML model
# model = Doc2Vec.load('C:/Users/hp/Desktop/rasabot/rasachat/ML/movies_doc2vec') # use the full path


# class ActionMovieSearch(Action):

# 	def name(self) -> Text:
# 		return "action_movie_search"

# 	def run(self, dispatcher: CollectingDispatcher,
# 			tracker: Tracker,
# 			domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

# 		userMessage = tracker.latest_message['text']
# 		# use model to find the movie
# 		new_doc = preprocess_string(userMessage)
# 		test_doc_vector = model.infer_vector(new_doc)
# 		sims = model.dv.most_similar(positive = [test_doc_vector])		
# 		# Get first 5 matches
# 		movies = [df['Title'].iloc[s[0]] for s in sims[:5]]

# 		botResponse = f"I found the following movies: {movies}.".replace('[','').replace(']','')
# 		dispatcher.utter_message(text=botResponse)

# 		return []

# class ActionHelloWorld(Action):
#
#     def name(self) -> Text:
#         return "action_hello_world"
#
#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#
#         dispatcher.utter_message(text="Hello World!")
#
#         return []
