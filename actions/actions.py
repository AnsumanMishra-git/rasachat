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
        res = requests.get(API_URL + "?apikey=" + API_KEY + "&offset=0")
        if res.status_code == 200:
            result = res.json()
            num = random.randint(0, len(result['data']) - 1) - 1
            out_message = "Here some cricket quick info:\n1.The match between {} and {} was recently held and {} .".format(
                result['data'][num]['teams'][0], result['data'][num]['teams'][1], result['data'][num]['status'])

            dispatcher.utter_message(out_message)

            out_message = "2.The next match was between {} and {} was recently held and {} .".format(
                result['data'][num + 1]['teams'][0], result['data'][num + 1]['teams'][1],
                result['data'][num + 1]['status'])

            dispatcher.utter_message(out_message)

        return []

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
