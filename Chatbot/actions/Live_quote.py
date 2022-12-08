# -*- coding: utf-8 -*-
"""
Created on Sat Nov 26 15:35:12 2022

@author: Admin
"""

def get_Live_quote():

      from nsetools import Nse 
      nse = Nse() 
    
      India_vix        = nse.get_index_quote('INDIA VIX')
      Nifty_50         = nse.get_index_quote('NIFTY 50')
      Nifty_Bank       = nse.get_index_quote('NIFTY Bank')
      Nifty_Midcap_100 = nse.get_index_quote('NIFTY MIDCAP 100')
      Nifty_smlcap_100 = nse.get_index_quote('NIFTY SMLCAP 100')
      Nifty_IT         = nse.get_index_quote('NIFTY IT')
      Nifty_AUTO       = nse.get_index_quote('NIFTY AUTO')
      Nifty_FMCG       = nse.get_index_quote('NIFTY FMCG')
      Nifty_PHARMA     = nse.get_index_quote('NIFTY PHARMA')
      Nifty_METAL      = nse.get_index_quote('NIFTY METAL')
    
      Live_News ="""Live Market\n
                    {0}           {1}  {2}%\n
                    {3}          {4}  {5}%\n
                    {6}       {7}  {8}%\n
                    {9}  {10}  {11}%\n
                    {12}     {13}  {14}%\n
                    {15}         {16}  {17}%\n
                    {18}         {19}  {20}%\n
                    {21}         {22}  {23}%\n
                    {24}       {25}  {26}%\n
                    {27}        {28}  {29}%\n"""
      
      strLive = Live_News.format(India_vix['name'], India_vix['lastPrice'], India_vix['pChange'],
                                 Nifty_50['name'],  Nifty_50['lastPrice'],  Nifty_50['pChange'],
                                 Nifty_Bank['name'], Nifty_Bank['lastPrice'], Nifty_Bank['pChange'],
                                 Nifty_Midcap_100['name'], Nifty_Midcap_100['lastPrice'], Nifty_Midcap_100['pChange'],
                                 Nifty_smlcap_100['name'], Nifty_smlcap_100['lastPrice'], Nifty_smlcap_100['pChange'],
                                 Nifty_IT['name'], Nifty_IT['lastPrice'], Nifty_IT['pChange'],
                                 Nifty_AUTO['name'], Nifty_AUTO['lastPrice'], Nifty_AUTO['pChange'],
                                 Nifty_FMCG['name'], Nifty_FMCG['lastPrice'], Nifty_FMCG['pChange'],
                                 Nifty_PHARMA['name'], Nifty_PHARMA['lastPrice'], Nifty_PHARMA['pChange'],
                                 Nifty_METAL['name'], Nifty_METAL['lastPrice'], Nifty_METAL['pChange'],
                               )
      
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



def get_Finance_data(stock_df):
  import yfinance as yahooFinance
  import pandas as pd 
  fin_stat_master = pd.DataFrame()

  for symbol in stock_df.index:
    stock = symbol+'.NS'
    GetInformation = yahooFinance.Ticker(stock)
    fin_stat_master = fin_stat_master.append([GetInformation.info],ignore_index=True)
    fin_stat_master = fin_stat_master[['symbol', 'sector','totalRevenue', 'ebitda', 'grossProfits', 'profitMargins',
                  'bookValue', 'pegRatio','beta','currentPrice','fiftyTwoWeekHigh','fiftyTwoWeekLow','lastDividendValue' ]]

  return fin_stat_master