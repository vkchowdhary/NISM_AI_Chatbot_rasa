# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List
#
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from portfolio_CNN_LSTM_analyzer import *
from scipy.optimize import minimize, Bounds
from Live_quote import *
from tensorflow import keras
from urllib.request import urlopen

import pandas as pd
import numpy as np
import datetime
import scipy


# import model
#model = keras.models.load_model('/content/cov_cnn_lstm.h5')
#model = keras.models.load_model('models/covar_model/cov_cnn_lstm.h5')


#
#
class ActionHelloWorld(Action):
#
    def name(self) -> Text:
          return "action_hello_world"
#          return "action_portfolio_analyzer"
     
        
    def run(self, dispatcher: CollectingDispatcher,
              tracker: Tracker,
              domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

          dispatcher.utter_message(text="Hello World! from Viaan")

          return []


   
class ActionLiveQuote(Action):
#
    def name(self) -> Text:
          return "action_live_quote"          
     
        
    def run(self, dispatcher: CollectingDispatcher,
              tracker: Tracker,
              domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

          dispatcher.utter_message(text=get_Live_quote())

          return [] 

class ActionPortfolioAnalyzer(Action):
#
    def name(self) -> Text:
         return "action_portfolio_analyzer" 
     
    def run(self, dispatcher: CollectingDispatcher,
         tracker: Tracker,
         domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:


       #portfolio = ['Reliance', 'SBIN', 'TCS', 'ACC', 'ADANIPORTS']
       portfolio = ['ADANIENT', 'ADANIPORTS', 'APOLLOHOSP', 'ASIANPAINT',
                     'AXISBANK', 'BAJAJ-AUTO', 'BAJFINANCE', 'BAJAJFINSV',
                     'BPCL', 'BHARTIARTL', 'BRITANNIA', 'CIPLA', 'COALINDIA',
                     'DIVISLAB', 'DRREDDY', 'EICHERMOT', 'GRASIM', 'HCLTECH',
                     'HDFCBANK', 'HDFCLIFE', 'HEROMOTOCO', 'HINDALCO', 'HINDUNILVR',
                     'HDFC', 'ICICIBANK', 'ITC', 'INDUSINDBK', 'INFY', 'JSWSTEEL',
                     'KOTAKBANK', 'LT', 'M&M', 'MARUTI', 'NTPC', 'NESTLEIND',
                     'ONGC', 'POWERGRID', 'RELIANCE', 'SBILIFE', 'SBIN', 'SUNPHARMA',
                     'TCS', 'TATACONSUM', 'TATAMOTORS', 'TATASTEEL', 'TECHM',
                     'TITAN', 'UPL', 'ULTRACEMCO', 'WIPRO']
       
       df = optimal_portfolio(portfolio, portfolio_size=15)
#         
       print(df)
       stock_list = df.to_string()
       print (stock_list)
       message =' Stock recommendation for you is\n{}'.format(stock_list)
     
       dispatcher.utter_message(text='Market analyzed')
       dispatcher.utter_message(text=message)
       dispatcher.utter_message(text='Please note, recommendation is based on modern portfolio theory')
       dispatcher.utter_message(text='Investment is subject to market risk, please take study the stock recommendation before your invest')
       return []       
   
## plan - full plan - fut 
## how to use the chat bot - Arch, NN, learn data, io, info m, manual,   
class ActionLiveNews(Action):
#
    def name(self) -> Text:
          return "action_live_news"          
     
        
    def run(self, dispatcher: CollectingDispatcher,
              tracker: Tracker,
              domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

          dispatcher.utter_message(text=get_Live_news())

          return [] 