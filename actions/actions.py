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
from dotenv import load_dotenv
import os #provides ways to access the Operating System and allows us to read the environment variables



load_dotenv()

API_URL = "https://api.cricapi.com/v1/currentMatches"
API_KEY =  os.getenv("API_KEY")

#This action is to signal that the assistant should get orderid from user and give order status .

class ActionRestart(Action):

  def name(self) -> Text:
      return "action_restart"

  async def run(
      self, dispatcher, tracker: Tracker, domain: Dict[Text, Any]
  ) -> List[Dict[Text, Any]]:

      # custom behavior
      return [Restarted()]
  
def get_new_token(access_token_url,client_id,client_secret,verify):
    try:
        token_req_payload = {'grant_type': 'client_credentials'}
        token_response = requests.post(access_token_url,
                                data=token_req_payload, 
                                verify=verify, 
                                allow_redirects=False,
                                auth=(client_id, client_secret))

        if token_response.status_code !=200:
            print("Failed to obtain token from the OAuth 2.0 server")
        else:
            print("Successfuly obtained a new token")

        tokens = json.loads(token_response.text)
        return [token_response.status_code,tokens['access_token']]
    except:
        print("Connection Failed. Please check your VPN or try again later")
        return [404,""]

class ActionGetStatus(Action):

    def name(self)-> Text:
        return "action_get_status"

    def run(self, dispatcher, tracker, domain):
        id = tracker.get_slot('tenant_id')
        dom = tracker.get_slot('tenant_domain')
        key = tracker.get_slot('key')
        
        body={
            "SoldToCustomerID": "0000002811",
            "ReceivedFromCustomerID": "0000002811",
            "PurchaseOrderId": "646466464",
            "TenantID": id,
            "TenantDomain": dom,
            "Devices": [{
                "ProductKey": key
            }]
        }

        CBR_url_1 = "https://apigtwob.us.dell.com/PROD/computerbuildreport/royd/v1/autopilot"

        access_token_url = os.getenv("access_token_url_2")
        client_id = os.getenv("client_id_2")
        client_secret = os.getenv("client_secret_2")

        token_response = get_new_token(access_token_url,client_id,client_secret,True)
        token=token_response[1]
        token_status_code=token_response[0]
        # token="55963ed0-0f5e-4565-8cbc-a27d0e5ee95e"
        
        if token_status_code==200:
            print(token)
            ##   call the API with the token
            api_call_headers = {'Authorization': 'Bearer ' + token}
            api_call_response = requests.post(CBR_url_1, headers=api_call_headers,json=body)
            response_json=api_call_response.json()

            if	api_call_response.status_code in [401,400] :
                text="Failed to obtain the batchId . Please check your VPN connectivity or try again later."
            else:
                BatchID=str(response_json['BatchId'])

                print("batch id is " +BatchID+" tenant id is " +id+" , tenant domain is "+dom+" , product key is "+str(key))
            
                CBR_url_2 = "https://apigtwob.us.dell.com/PROD/computerbuildreport/royd/v1/autopilot?BatchID="+BatchID

                print(CBR_url_2)

                api_call_headers = {'Authorization': 'Bearer ' + token}
                api_call_response = requests.get(CBR_url_2, headers=api_call_headers,json=body)
                response_json=api_call_response.json()
                print(response_json)
                text=""
                if	api_call_response.status_code in [401,400] :
                    text = "Registration Process Failed . Please check your VPN connectivity or try again later."
                elif response_json['Devices'][0]['DeviceStatusName'] == "Error":
                    text="Registration Process Failed. Reason for failure : "+ response_json['Devices'][0]['DeviceErrorName']
                else:
                    text="Registration Successful . Your RegistrationID is : "+response_json['Devices'][0]['RegistrationId']
        else:
            text="Please check your VPN connectivity or try again later."
        dispatcher.utter_message(text)
        return [SlotSet('check', None),SlotSet('key', None),SlotSet('service_tag', None),SlotSet('tenant_id', None),SlotSet('tenant_domain', None)]

class ActionCheckTag(Action):
    def name(self)-> Text:
        return "action_check_tag"
    
    def run(self, dispatcher, tracker, domain):

        tag = tracker.get_slot('service_tag')
        body = {
                "messageHeader": {
                    "version": "11",
                    "messageType": "1",
                    "messageId": "1",
                    "correlationId": "1",
                    "processDateTime": "3/08/2021 9:38:06 AM",
                    "messageNotes": "1"
                },
                "messagePayload": {
                    "servicetags": [
                        {
                            "servicetag": tag
                        }
                    ]
                }
            }
        api_url = "https://computerbuildreportinfo.delpprov.delltechnologies.com/api/validate"

        access_token_url = os.getenv("access_token_url_1")
        client_id = os.getenv("client_id_1")
        client_secret = os.getenv("client_secret_1")

        token_response = get_new_token(access_token_url,client_id,client_secret,False)
        token=token_response[1]
        token_status_code=token_response[0]
        # token="55963ed0-0f5e-4565-8cbc-a27d0e5ee95e"
        is_valid=False
        pk_id=""
        if token_status_code==200:
            print(token)

            api_call_headers = {'Authorization': 'Bearer ' + token}
            api_call_response = requests.post(api_url, headers=api_call_headers,verify=False, json=body)
            response_json=api_call_response.json()
            pk_id=response_json['messagePayload']['response']['validationResults'][0]['productKey']
            is_valid=True

            if	api_call_response.status_code in [401,400] :
                is_valid=False
                response="Failed to obtain the Product Key . Please check your VPN connectivity or try again later."
            else:
                response="""Thank You."""
                if(pk_id==""):
                    is_valid=False
                    response = """No product key available for the given service tag"""
        else:
            response="Please check your VPN connectivity or try again later."
        dispatcher.utter_message(response)
        return [SlotSet('check', is_valid),SlotSet('key', pk_id)]
    
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