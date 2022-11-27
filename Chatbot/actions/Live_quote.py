# -*- coding: utf-8 -*-
"""
Created on Sat Nov 26 15:35:12 2022

@author: Admin
"""

def get_Live_quote():

      from nsetools import Nse 
      nse = Nse() 
    
      Ni50 = nse.get_index_quote('NIFTY 50')
      Nibk = nse.get_index_quote('NIFTY bank')
      vix = nse.get_index_quote('INDIA VIX')
    
      Live_News ="Live Market\n{0}    {1}  {2}%\n{3}  {4}  {5}%\n{6}   {7}  {8}%"
      strLive = Live_News.format(Ni50['name'],Ni50['lastPrice'],Ni50['pChange'],
                               Nibk['name'],Nibk['lastPrice'],Nibk['pChange'],
                               vix['name'],vix['lastPrice'],vix['pChange'],)
      
      return strLive
  
    

def get_Live_news():
      from bs4 import BeautifulSoup as BS
      import requests as req
      
      url = "https://www.businesstoday.in/latest/economy"
      news = ''
      webpage = req.get(url)
      trav = BS(webpage.content, "html.parser")
      M = 1
      for link in trav.find_all('a'):
        
          # PASTE THE CLASS TYPE THAT WE GET
          # FROM THE ABOVE CODE IN THIS AND
          # SET THE LIMIT GREATER THAN 35
          if(str(type(link.string)) == "<class 'bs4.element.NavigableString'>"
            and len(link.string.strip()) > 50):
                  
              strnew = '{0}  {1} \n'.format(str(M), link.string.strip())
              news += strnew
              M += 1
      return news