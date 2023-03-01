# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List
from rasa_sdk.events import SlotSet, EventType,Restarted
from rasa_sdk import Action, Tracker,FormValidationAction
from rasa_sdk.types import DomainDict
from rasa_sdk.executor import CollectingDispatcher
import logging
import requests
import json
from datetime import datetime
import random


API_URL = "https://api.cricapi.com/v1/currentMatches"
API_KEY = "d0b73bf4-e8fc-4d3b-a9d8-8b8b6467c36b"

#This action is to signal that the assistant should get orderid from user and give order status .

class ActionRestart(Action):

  def name(self) -> Text:
      return "action_restart"

  async def run(
      self, dispatcher, tracker: Tracker, domain: Dict[Text, Any]
  ) -> List[Dict[Text, Any]]:

      # custom behavior
      return [Restarted()]
  
class ActionGetStatus(Action):

    def name(self)-> Text:
        return "action_get_status"
    
    def run(self, dispatcher, tracker, domain):
        id = tracker.get_slot('tenant_id')
        dom = tracker.get_slot('tenant_domain')
        key = tracker.get_slot('key')
        data={
            "SoldToCustomerID": "562764278",
            "ReceivedFromCustomerID": "247856287",
            "PurchaseOrderId": "34745546",
            "TenantID": id,
            "TenantDomain": dom,
            "Devices": [{
            "ProductKey":key
            }]
        }
        print("id is " +id+" , domain is "+dom+" , key is "+key)
        response="""Registration Successful"""
        dispatcher.utter_message(response)
        return [SlotSet('check', None),SlotSet('key', None),SlotSet('service_tag', None),SlotSet('tenant_id', None),SlotSet('tenant_domain', None)]

class ActionCheckTag(Action):
    def name(self)-> Text:
        return "action_check_tag"
    
    def run(self, dispatcher, tracker, domain):

        tag = tracker.get_slot('service_tag')
        data = {
            "tag": tag
        }
        res = requests.get('http://localhost:3000/check',json=data).json()
        prod_key="234532"
        print(res)
        response="""Thank You."""
        if(res==False):
            response = """No product key available for the given service tag"""
        dispatcher.utter_message(response)
        return [SlotSet('check', res),SlotSet('key', prod_key)]
    
#This action is to signal that the assistant should get email id from user and give response if email is updated successfully or not.
# class ActionUpdateEmail(Action):

#     def name(self)-> Text:
#         return "action_update_email"
    
#     def run(self, dispatcher, tracker, domain):

#         eid = tracker.get_slot('empid')
#         mail = tracker.get_slot('email')
#         res = requests.post('http://localhost:3000/update/{}/editmail/{}'.format(eid,mail)).json()
#         print(res)
#         response = """Your new email {} has been set.""".format(mail)
#         dispatcher.utter_message(response)
#         return [SlotSet('email', None)]


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
    
# class AuthenticatedAction(Action):
#     def name(self) -> Text:
#         return "action_authenticated"

#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]
#             ) -> List[Dict[Text, Any]]:

#             token = tracker.get_slot("token")
#             if token is not None:
#                 dispatcher.utter_message(text="utter_greet")
#             else:
#                 dispatcher.utter_message("The token did not match . Please try again .")
#             return []


# class ValidateAuthFormAction(FormValidationAction):
#     def name(self) -> Text:
#         return "validate_auth_form"

#     def validate_token(
#         self,
#         slot_value: Any,
#         dispatcher: CollectingDispatcher,
#         tracker: Tracker,
#         domain: DomainDict,
#     ) -> Dict[Text, Any]:

#         if slot_value is not None and (slot_value=="admin123"):
#             return {"token": slot_value}
#         else:
#             return {"token": None}

# class ActionHelloWorld(Action):

#     def name(self) -> Text:
#         return "action_hello_world"

#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

#         dispatcher.utter_message(text="Hello World!")

#         return []
