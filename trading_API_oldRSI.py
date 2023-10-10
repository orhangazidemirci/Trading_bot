# -*- coding: utf-8 -*-
"""
Created on Sun Aug 14 02:52:11 2022

@author: orhan
"""
import pandas as pd
# from binance import Client
import datetime as dt
# # client old
# user_key = '5568aacad0f78ae807b1605fa507a3c13fe4a67854b4afd3dcf58bed3fdc0cb0' 
# secret_key = '6b2a5cf803d6b8a0caa43f9eb77b631fafa57eee09de5c92b7de3dae5e76d5b7'

# # REAL API
# # user_key = 'gxcc8A1XSDzLzPb7cgLGydDGYsH24ptVZB4Vqz2e1PxMXoIVVSO1dyDiLEapifR7' 
# user_key = 'QMoAvtNmDBRJVL2CRcEH6Yzygl7gWXrJ3MMseZZp6imW56ZrO8o3UEBC0SdLiTaH' 
# # secret_key = 'JdFFNVeTZWPSbSIWCG0yVp8ZGsenFhsZkXW9U1xiWeeftn9OxnLPKA7PyvxTtw09'
# secret_key = 'BuhUBOi2L8k6yKwVigyxHoRvquZ2KY0LlZ6ofRvfjimlWjF49tDmfB6HGs3fwo21'
# # client new


# # REAL FUTURE API
user_key = 'XIMA4QelIpNHrJFf7asqTyBNK3QvKB8RsIsmlfMd6qGmpLulJ60wxQIF29L9jORd'
secret_key = 'v2ALlxqwfMqnWKRDWwgZxS937TsT0s4KQitaNxL6bnq2ReA4rFEdhs5l7KVwWPmE'

# # # REAL FUTURE API-2
# user_key = 'kC11Mo7mdJDnqLCgiY98O58M0at5D5jPB77zPDve7HdDuIg9gWFrBHjB7wGZ8OG7'
# secret_key = 'b3h0STeqXx6AJvGeaFipPos8ZGNgK8dvOIHR0kMlH4cxhxfuKHyvFwFUbHk1io6r'

# user_key = '304fd8c8a02810703fc4238551808b7d0e987d4b048c49af376270b99e3b656e' 
# secret_key = 'f28db410ce965f98e8babcebbeeaa54c2b5bbddddd6eb62aa8a6402aee754d0c'
import ccxt

exchange = ccxt.binance({
"apiKey": user_key,
"secret": secret_key,

'options': {
'defaultType': 'future'
},
'enableRateLimit': True
})

# exchange.set_sandbox_mode(True) # activates testnet mode
TIME_PERIOD='15m'
symbol_name='LTC'
symbol=symbol_name+'USDT'
newSymbol=symbol_name+'/USDT'
leverage=5
exchange.setLeverage (leverage, symbol = symbol, params = {})

prices=exchange.fetch_ohlcv(newSymbol, timeframe=TIME_PERIOD, limit=30) # open-high-low-close

data = pd.DataFrame(prices)
#format columns name
data.columns = ['datetime', 'open', 'high', 'low', 'close', 'volume']
data.index = [dt.datetime.fromtimestamp(x/1000.0) for x in data.datetime]
data=data.astype(float)

data=data.values[:,4]
import numpy as np

import smtplib
from email.message import EmailMessage

def email_alert(subject,body,to):
    msg= EmailMessage()
    msg.set_content(body)
    msg['subject']=subject
    msg['to']=to
    
    user="wmi1orhan@gmail.com"
    # password="cawvvjqipwykcijy"
    msg['from']=user
    password="obdcyunnkridlgbw"
    server=smtplib.SMTP("smtp.gmail.com",587)
    # server.ehlo()

    server.starttls()
    server.login(user, password)
    server.send_message(msg)
    server.quit()
    
    
    
# email_alert("Hello", "World", "wmi1orhan@gmail.com")
email_alert("Hello", "World", "wmi1orhan@gmail.com")

import websocket, json, talib
SOCKET= "wss://stream.binance.com:9443/ws/ltcusdt@kline_{}".format(TIME_PERIOD)
# SOCKET= "wss://stream.binance.com:9443/ws/ltcusdt@kline_1m"

EMA_PERIOD=7
RSI_PERIOD=14

first_buy=False
first_sell=False

rsi_buy=False
rsi_sell=False
rsi_trig=False


ema_trig=True
margin_error='binance {"code":-2019,"msg":"Margin is insufficient."}'
quantity_error='binance {"code":-4003,"msg":"Quantity less than zero."}'
bound_errror='index -1 is out of bounds for axis 0 with size 0'
# time_error='InvalidNonce: binance {"code":-1021,"msg":"Timestamp for this request was 1000ms ahead of the server's time."}'
order_percent=99   
close_val=data[0:len(data)-1].tolist()
rsi_val=0

# balance = exchange.fetch_balance()
# free_balance = exchange.fetch_free_balance()
# positions = balance['info']['positions']


# current_positions = [position for position in positions if float(position['positionAmt']) != 0 and position['symbol'] == symbol]
# position_inf = pd.DataFrame(current_positions, columns=["symbol", "entryPrice", "unrealizedProfit", "isolatedWallet", "positionAmt", "positionSide"])

# quantity = (((float(free_balance["USDT"]) / 100 ) * float(order_percent)) * float(leverage)) / float(close_val[-1])

# # quantity=((balance['total']["USDT"]-float(free_balance["USDT"]))* float(leverage))/ float(close_val[-1])
# exchange.create_market_sell_order(newSymbol, quantity+float(position_inf["positionAmt"][len(position_inf.index) - 1]))
# exchange.create_market_sell_order(newSymbol, float(position_inf["positionAmt"][len(position_inf.index) - 1]), {"reduceOnly": True}) 

# binance_client.futures_account()['assets'][1]['walletBalance']
# binance_client.futures_account()['assets'][1]['availableBalance']

# exchange.create_market_buy_order(newSymbol, quantity-1*float(position_inf["positionAmt"][len(position_inf.index) - 1])) 
# exchange.create_market_buy_order(newSymbol, -1*float(position_inf["positionAmt"][len(position_inf.index) - 1]), {"reduceOnly": True}) 

# binance_client.futures_account()['assets'][1]['walletBalance']
# binance_client.futures_account()['assets'][1]['availableBalance']

import requests

# pushbullet_noti("NEW ORDER", ' --------------')
def Order_Status():
    global first_buy,first_sell
    balance = exchange.fetch_balance()
    free_balance = exchange.fetch_free_balance()
    positions = balance['info']['positions']
    current_positions = [position for position in positions if float(position['positionAmt']) != 0 and position['symbol'] == symbol]
    position_inf = pd.DataFrame(current_positions, columns=["symbol", "entryPrice", "unrealizedProfit", "isolatedWallet", "positionAmt", "positionSide"])
    
    ratio= free_balance["USDT"]/balance['total']["USDT"]


    if len(position_inf.index)==0 :
        first_buy=False
        first_sell=False
        
    else:
        if float(position_inf["positionAmt"][len(position_inf.index) - 1])>0 and ratio<0.2:
            first_buy=True
            first_sell=False
        elif float(position_inf["positionAmt"][len(position_inf.index) - 1])<0 and ratio<0.2:

            first_buy=False
            first_sell=True    
        
        else:
            first_buy=False
            first_sell=False
       # LONG ENTER
       def RSI_Long(position_inf,quantity):
           global first_buy
           global first_sell,rsi_buy
           

                  
           print('FirstBuy= {}'.format(first_buy))
           print('FirstSell= {}'.format(first_sell))  
                  
           if first_sell:
               try:
                   while first_sell==True:
                       
                       order = exchange.create_market_buy_order(newSymbol, -1*float(position_inf["positionAmt"][len(position_inf.index) - 1]), {"reduceOnly": True})
                       Order_Status()
                               # pushbullet_noti("Order", "RSI BUYING {} LTC coin at time ".format(order['amount'] )+str(dt.datetime.now())+" price= "+str(order['price']))
                   email_alert("Order", "RSI BUYING {} LTC coin at time ".format(order['amount'] )+str(dt.datetime.now())+" price= "+str(order['price']), "wmi1orhan@gmail.com")
                   # first_buy=False
                   # first_sell=False
          
               except:

               # if bound_errror=='{}'.format(e):
               #     # balance = exchange.fetch_balance()
               #     # free_balance = exchange.fetch_free_balance()
               #     # positions = balance['info']['positions']
               #     # current_positions = [position for position in positions if float(position['positionAmt']) != 0 and position['symbol'] == symbol]
               #     # position_inf = pd.DataFrame(current_positions, columns=["symbol", "entryPrice", "unrealizedProfit", "isolatedWallet", "positionAmt", "positionSide"])
               #     # quantity = (((float(free_balance["USDT"]) / 100 ) * float(order_percent)) * float(leverage)) / float(close_last)
        
                   try:

                       order = exchange.create_market_buy_order(newSymbol,-1*float(position_inf["positionAmt"][len(position_inf.index) - 1]), {"reduceOnly": True})
                       Order_Status()

                       
                                       # pushbullet_noti("Order", "RSI BUYING {} LTC coin at time ".format(order['amount'] )+" price= "+str(order['price']))
                       email_alert("Order", "RSI BUYING {} LTC coin at time ".format(order['amount'] )+str(dt.datetime.now())+" price= "+str(order['price']), "wmi1orhan@gmail.com")

                       # first_buy=False
                       # first_sell=False
             
                   except Exception as e:
                       print('An exception occured - {}'.format(e))
                       # pushbullet_noti("Exception", "An exception occured - {} in RSI BUY".format(e))
                       email_alert("Exception", "An exception occured - {} in RSI SELL".format(e), "wmi1orhan@gmail.com")

               # else:
                   #     print('An exception occured - {}'.format(e))
                   #     pushbullet_noti("Exception", "An exception occured - {} in BUY".format(e))



           
           elif first_buy==False:
                   try:
                       while first_buy==False:
                           
                           order = exchange.create_market_buy_order(newSymbol, quantity)
                           Order_Status()
                       # pushbullet_noti("Order", "RSI BUYING {} LTC coin at time ".format(order['amount'] )+str(dt.datetime.now())+" price= "+str(order['price']), {"reduceOnly": True})
                       # first_buy=True
                       email_alert("Order", "RSI BUYING {} LTC coin at time ".format(order['amount'] )+str(dt.datetime.now())+" price= "+str(order['price']), "wmi1orhan@gmail.com")

                   
                   except Exception as e:
                       error='{}'.format(e)
                           
                       if margin_error==error:
                           const=0.98
                           while margin_error==error:
                               try:
                                   while first_buy==False:
                                       
                                       order = exchange.create_market_buy_order(newSymbol,quantity*const)
                                       Order_Status()
                                   
                                   # pushbullet_noti("Order", "RSI BUYING {} LTC coin at time ".format(order['amount'] )+str(dt.datetime.now())+" price= "+str(order['price']))
                                   email_alert("Order", "RSI BUYING {} LTC coin at time ".format(order['amount'] )+str(dt.datetime.now())+" price= "+str(order['price']), "wmi1orhan@gmail.com")

                                   # first_buy=True
                                   # first_sell=False
                                   error='No Error'
                   
                               except Exception as e:
                                   error='{}'.format(e)
                                   const-=0.01
                           
                       else:
                           print('An exception occured - {}'.format(e))
                           # pushbullet_noti("Exception", "An exception occured - {} in RSI BUY".format(e))
                           email_alert("Exception", "An exception occured - {} in RSI SELL".format(e), "wmi1orhan@gmail.com")

                       # print('An exception occured - {}'.format(e))
                       # pushbullet_noti("Exception", "An exception occured - {} in BUY".format(e))
                       # if bound_errror=='{}'.format(e):
               
                       # elif quantity_error=='{}'.format(e):
                       #     first_buy=True
                   
       # LONG EXIT

                   
       def RSI_Short(position_inf,quantity):
           global first_buy ,close_last
           global first_sell
           
          
           print('FirstBuy= {}'.format(first_buy))
           print('FirstSell= {}'.format(first_sell))            
                   
           if first_buy:
               try:
                   while first_buy==True:

                       order = exchange.create_market_sell_order(newSymbol, float(position_inf["positionAmt"][len(position_inf.index) - 1]), {"reduceOnly": True})
                       Order_Status()    
                               # pushbullet_noti("Order", "RSI SELLING {} LTC coin at time ".format(order['amount'] )+str(dt.datetime.now())+" price= "+str(order['price']))
                   email_alert("Order", "RSI SELLING {} LTC coin at time ".format(order['amount'] )+str(dt.datetime.now())+" price= "+str(order['price']), "wmi1orhan@gmail.com")

                   # first_buy=False
                   # first_sell=False
               except :
               
                   # print('An exception occured - {}'.format(e))
                   # pushbullet_noti("Exception", "An exception occured - {} in SELL".format(e))
                   # # if bound_errror=='{}'.format(e):
         
                   try:
                       
                       order = exchange.create_market_sell_order(newSymbol, float(position_inf["positionAmt"][len(position_inf.index) - 1]), {"reduceOnly": True})
                       # pushbullet_noti("Order", "RSI SELLING {} LTC coin at time ".format(order['amount'] )+str(dt.datetime.now())+" price= "+str(order['price']))
                       email_alert("Order", "RSI SELLING {} LTC coin at time ".format(order['amount'] )+str(dt.datetime.now())+" price= "+str(order['price']), "wmi1orhan@gmail.com")

                       first_buy=False
                       first_sell=False

                   except Exception as e:
                       print('An exception occured - {}'.format(e))
                       # pushbullet_noti("Exception", "An exception occured - {} in SELL".format(e))
                       email_alert("Exception", "An exception occured - {} in RSI SELL".format(e), "wmi1orhan@gmail.com")

           elif first_sell==False:
                   try:
                       while first_sell==False:
                       
                           order = exchange.create_market_sell_order(newSymbol, quantity)
                           Order_Status()
                                       # pushbullet_noti("Order", "RSI SELLING {} LTC coin at time ".format(order['amount'] )+str(dt.datetime.now())+" price= "+str(order['price']))
                       email_alert("Order", "RSI SELLING {} LTC coin at time ".format(order['amount'] )+str(dt.datetime.now())+" price= "+str(order['price']), "wmi1orhan@gmail.com")

                       first_sell=True
                   except Exception as e:
                       error='{}'.format(e)
                       if margin_error==error:
                           const=0.98
                           while margin_error==error:
                               try:
                                   while first_sell==False:
                                   
                                       order = exchange.create_market_sell_order(newSymbol,quantity*const)
                                       Order_Status()
                                                               # pushbullet_noti("Order", "RSI SELLING {} LTC coin at time ".format(order['amount'] )+str(dt.datetime.now())+" price= "+str(order['price']))
                                   email_alert("Order", "RSI SELLING {} LTC coin at time ".format(order['amount'] )+str(dt.datetime.now())+" price= "+str(order['price']), "wmi1orhan@gmail.com")

                                   # first_buy=False
                                   # first_sell=True
                                   error='No Error'
                   
                               except Exception as e:
                                   error='{}'.format(e)
                                   const-=0.01
                                   
                       else:
                           print('An exception occured - {}'.format(e))
                           # pushbullet_noti("Exception", "An exception occured - {} in RSI SELL".format(e))
                           email_alert("Exception", "An exception occured - {} in RSI SELL".format(e), "wmi1orhan@gmail.com")
                                      
                       # print('An exception occured - {}'.format(e))
                       # pushbullet_noti("Exception", "An exception occured - {} in SELL".format(e))
                       # if bound_errror=='{}'.format(e):

                       # elif quantity_error=='{}'.format(e):
                       #     first_sell=True
                       
                
def longExit(position_inf,quantity):
    global first_sell
    global first_buy ,close_last
    

    print('FirstBuy= {}'.format(first_buy))
    print('FirstSell= {}'.format(first_sell))                 
        
    if first_buy:
        try:
            while first_buy==True:
                
                order = exchange.create_market_sell_order(newSymbol, float(position_inf["positionAmt"][len(position_inf.index) - 1]), {"reduceOnly": True})
                Order_Status()
            # pushbullet_noti("Order", "SELLING {} LTC coin at time ".format(order['amount'] )+str(dt.datetime.now())+" price= "+str(order['price']))
            email_alert("Order", "SELLING {} LTC coin at time ".format(order['amount'] )+str(dt.datetime.now())+" price= "+str(order['price']), "wmi1orhan@gmail.com")

            # first_buy=False
            first_sell=False
 
        except Exception as e:

            print('An exception occured - {}'.format(e))
            # pushbullet_noti("Exception", "An exception occured - {} in SELL".format(e))
            email_alert("Exception", "An exception occured - {} in SELL".format(e), "wmi1orhan@gmail.com")

    
 
        try:
            while first_sell==False:
                
                order = exchange.create_market_sell_order(newSymbol, quantity)
                Order_Status()
                        # pushbullet_noti("Order", "SELLING {} LTC coin at time ".format(order['amount'] )+str(dt.datetime.now())+" price= "+str(order['price']))
            # first_buy=False
            # first_sell=True
            email_alert("Order", "SELLING {} LTC coin at time ".format(order['amount'] )+str(dt.datetime.now())+" price= "+str(order['price']), "wmi1orhan@gmail.com")

        except Exception as e:
            error='{}'.format(e)
            # print('An exception occured - {}'.format(e))
            # pushbullet_noti("Exception", "An exception occured - {} in SELL".format(e))
            # # if bound_errror=='{}'.format(e):
            if margin_error==error:
                const=0.98
                while margin_error==error:
                    try:
                        while first_sell==False:
                            
                            order = exchange.create_market_sell_order(newSymbol,quantity*const)
                            Order_Status()
                                                # pushbullet_noti("Order", "SELLING {} LTC coin at time ".format(order['amount'] )+str(dt.datetime.now())+" price= "+str(order['price']))
                        # first_buy=False
                        # first_sell=True
                        error='No Error'
                        email_alert("Order", "SELLING {} LTC coin at time ".format(order['amount'] )+str(dt.datetime.now())+" price= "+str(order['price']), "wmi1orhan@gmail.com")

                    except Exception as e:
                        error='{}'.format(e)
                        const-=0.01
                        
            else:
                print('An exception occured - {}'.format(e))
                # pushbullet_noti("Exception", "An exception occured - {} in SELL".format(e))
                email_alert("Exception", "An exception occured - {} in SELL".format(e), "wmi1orhan@gmail.com")
                
    elif first_sell==False:  
            try:
                while first_sell==False:
                    order = exchange.create_market_sell_order(newSymbol, quantity)
                    Order_Status()
                # pushbullet_noti("Order", "SELLING {} LTC coin at time ".format(order['amount'] )+str(dt.datetime.now())+" price= "+str(order['price']))
                email_alert("Order", "SELLING {} LTC coin at time ".format(order['amount'] )+str(dt.datetime.now())+" price= "+str(order['price']), "wmi1orhan@gmail.com")
                
                # first_sell=True
                # first_buy=False
    
            except Exception as e:
                error='{}'.format(e)
                if margin_error==error:
                    const=0.98
                    while margin_error==error:
                        try:
                            while first_sell==False:
                                order = exchange.create_market_sell_order(newSymbol,quantity*const)
                                Order_Status()
                                                        # pushbullet_noti("Order", "SELLING {} LTC coin at time ".format(order['amount'] )+str(dt.datetime.now())+" price= "+str(order['price']))
                            # first_buy=False
                            # first_sell=True
                            error='No Error'
                            email_alert("Order", "SELLING {} LTC coin at time ".format(order['amount'] )+str(dt.datetime.now())+" price= "+str(order['price']), "wmi1orhan@gmail.com")

                        except Exception as e:
                            error='{}'.format(e)
                            const-=0.01
                                                        
                else:
                    print('An exception occured - {}'.format(e))
                    # pushbullet_noti("Exception", "An exception occured - {} in SELL".format(e))
                    email_alert("Exception", "An exception occured - {} in SELL".format(e), "wmi1orhan@gmail.com")

    
# SHORT EXIT
def longEnter(position_inf,quantity):
    global first_buy
    global first_sell
    

    print('FirstBuy= {}'.format(first_buy))
    print('FirstSell= {}'.format(first_sell))            
    if first_sell:

        try:
            while first_sell==True:
                order = exchange.create_market_buy_order(newSymbol, -1*float(position_inf["positionAmt"][len(position_inf.index) - 1]), {"reduceOnly": True})
                Order_Status()
                        # pushbullet_noti("Order", "BUYING {} LTC coin at time ".format(order['amount'] )+str(dt.datetime.now())+" price= "+str(order['price']))
            # first_buy=False
            # first_sell=False
            email_alert("Order", "BUYING {} LTC coin at time ".format(order['amount'] )+str(dt.datetime.now())+" price= "+str(order['price']), "wmi1orhan@gmail.com")
           
        except Exception as e:

            print('An exception occured - {}'.format(e))
            # pushbullet_noti("Exception", "An exception occured - {} in BUY".format(e))
            email_alert("Exception", "An exception occured - {} in BUY".format(e), "wmi1orhan@gmail.com")

        try:
            while first_buy==False:
                order = exchange.create_market_buy_order(newSymbol, quantity)
                Order_Status()
                        # pushbullet_noti("Order", "BUYING {} LTC coin at time ".format(order['amount'] )+str(dt.datetime.now())+" price= "+str(order['price']))
            # first_buy=True
            # first_sell=False
            email_alert("Order", "BUYING {} LTC coin at time ".format(order['amount'] )+str(dt.datetime.now())+" price= "+str(order['price']), "wmi1orhan@gmail.com")

        except Exception as e:
            error='{}'.format(e)
                
            if margin_error==error:
                const=0.98
                while margin_error==error:
                    try:
                        while first_buy==False:
                            order = exchange.create_market_buy_order(newSymbol,quantity*const)
                            Order_Status()
                                                # pushbullet_noti("Order", "BUYING {} LTC coin at time ".format(order['amount'] )+str(dt.datetime.now())+" price= "+str(order['price']))
                        # first_buy=True
                        # first_sell=False
                        error='No Error'
                        email_alert("Order", "BUYING {} LTC coin at time ".format(order['amount'] )+str(dt.datetime.now())+" price= "+str(order['price']), "wmi1orhan@gmail.com")

                    except Exception as e:
                        error='{}'.format(e)
                        const-=0.01
                        
                  
                # else:
                #     try:
                #         order = exchange.create_market_buy_order(newSymbol, float(position_inf["positionAmt"][len(position_inf.index) - 1]))
                #         pushbullet_noti("Order", "BUYING {} LTC coin at time ".format(order['amount'] )+str(dt.datetime.now())+" price= "+str(order['price']))
                #         first_buy=True
                #         first_sell=False
                        
                #     except Exception as e:
                #         print('An exception occured - {}'.format(e))
                #         pushbullet_noti("Exception", "An exception occured - {} in BUY".format(e))
            else:
                print('An exception occured - {}'.format(e))
                # pushbullet_noti("Exception", "An exception occured - {} in BUY".format(e))
                email_alert("Exception", "An exception occured - {} in BUY".format(e), "wmi1orhan@gmail.com")



    elif first_buy==False:
            try:
                while first_buy==False:
                    order = exchange.create_market_buy_order(newSymbol, quantity)
                    Order_Status()                
                                # pushbullet_noti("Order", "BUYING {} LTC coin at time ".format(order['amount'] )+str(dt.datetime.now())+" price= "+str(order['price']))
                # first_buy=True
                # first_sell=False
                email_alert("Order", "BUYING {} LTC coin at time ".format(order['amount'] )+str(dt.datetime.now())+" price= "+str(order['price']), "wmi1orhan@gmail.com")

            except Exception as e:
                error='{}'.format(e)
                    
                if margin_error==error:
                    const=0.98
                    while margin_error==error:
                        try:
                            while first_buy==False:
                                order = exchange.create_market_buy_order(newSymbol,quantity*const)
                                Order_Status() 
                                                        # pushbullet_noti("Order", "BUYING {} LTC coin at time ".format(order['amount'] )+str(dt.datetime.now())+" price= "+str(order['price']))
                            # first_buy=True
                            # first_sell=False
                            error='No Error'
                            email_alert("Order", "BUYING {} LTC coin at time ".format(order['amount'] )+str(dt.datetime.now())+" price= "+str(order['price']), "wmi1orhan@gmail.com")

                        except Exception as e:
                            error='{}'.format(e)
                            const-=0.01
                                        
                # print('An exception occured - {}'.format(e))
                # pushbullet_noti("Exception", "An exception occured - {} in BUY".format(e))
                # if bound_errror=='{}'.format(e):
                else:
                    print('An exception occured - {}'.format(e))
                    # pushbullet_noti("Exception", "An exception occured - {} in BUY".format(e))
                    email_alert("Exception", "An exception occured - {} in BUY".format(e), "wmi1orhan@gmail.com")

                # elif quantity_error=='{}'.format(e):
                #     first_buy=True
def on_open(ws):
    print("opened")

def on_close(ws):
    print("closed")


 
# Function to send Push Notification



# symbol='LTCUSDT'
rsi_count=0

def on_message(ws,message):
    global  first_buy,first_sell,ema_trig
    # print("received message")

    json_message=json.loads(message)
    # pprint.pprint(json_message)
    candle=json_message['k']
    is_candle_closed=candle['x']
    if is_candle_closed:
        # print('f')
        # torch.cat((data,torch.tensor(float(candle['c']))), dim=0)
        prices=exchange.fetch_ohlcv(newSymbol, timeframe=TIME_PERIOD, limit=1)
        # close_val.append(float(candle['c']))
        close_val.append(float(prices[0][4]))
        ema=talib.EMA(np.array(close_val), timeperiod = EMA_PERIOD)
        rsi=talib.RSI(np.array(close_val), timeperiod = RSI_PERIOD)
        ema_last=ema[-1]
        ema_prev=ema[-2]
        
        close_last=close_val[-1]
        close_prev=close_val[-2]
        
        balance = exchange.fetch_balance()
        free_balance = exchange.fetch_free_balance()
        used_balance=exchange.fetch_used_balance()
        positions = balance['info']['positions']
        current_positions = [position for position in positions if float(position['positionAmt']) != 0 and position['symbol'] == symbol]
        position_inf = pd.DataFrame(current_positions, columns=["symbol", "entryPrice", "unrealizedProfit", "isolatedWallet", "positionAmt", "positionSide"])
        
        ratio= free_balance["USDT"]/balance['total']["USDT"]


        if len(position_inf.index)==0 :
            first_buy=False
            first_sell=False
            
        else:
            if float(position_inf["positionAmt"][len(position_inf.index) - 1])>0 and ratio<0.2:
                first_buy=True
                first_sell=False
            elif float(position_inf["positionAmt"][len(position_inf.index) - 1])<0 and ratio<0.2:
    
                first_buy=False
                first_sell=True    
            
            else:
                first_buy=False
                first_sell=False
                
        quantity = ((((float(used_balance["USDT"])+float(free_balance["USDT"])) / 100 ) * float(order_percent)) * float(leverage)) / float(close_last)
        # order = exchange.create_market_sell_order(newSymbol,quantity)
        if ((rsi[-3]-50)* (rsi[-2]-50)<0 and (rsi[-2]-50)*(rsi[-1]-50)<0 or abs(rsi[-1]-50)<1.5):
            # if first_buy==True:
            #     longEnter(position_inf,quantity)
            ema_trig=False
        else:
            ema_trig=True
            
        if rsi[-1]<70 and rsi[-2]>70 and (ema_last-close_last)*(ema_prev-close_prev)>0 and ema_trig:
            # SELLING COIN
            # rsi_sell=True
            # longExit(position_inf,quantity)
            # quantity = (((float(free_balance["USDT"]) / 100 ) * float(order_percent)) * float(leverage)) / float(close_last)
            # longExit(position_inf,quantity)
            RSI_Short(position_inf,quantity)
            print('RSI SELL ' )
            email_alert("RSI SELL" , "wmi1orhan@gmail.com")

            # rsi_val=close_last
        if rsi[-1]>30 and rsi[-2]<30 and (ema_last-close_last)*(ema_prev-close_prev)>0 and ema_trig:
            # BUYING COIN
            # rsi_buy=True     
            # longEnter(position_inf,quantity)
            # quantity = (((float(free_balance["USDT"]) / 100 ) * float(order_percent)) * float(leverage)) / float(close_last)

            RSI_Long(position_inf,quantity)
            # longEnter(position_inf,quantity)
            email_alert("RSI BUY" , "wmi1orhan@gmail.com")

            print('RSI BUY ' )
            # rsi_val=close_last
            



                
        if (ema_last-close_last)*(ema_prev-close_prev)<0:
            # if first_buy==False and first_sell==False:
            #     quantity = ((((float(free_balance["USDT"])) / 100 ) * float(order_percent)) * float(leverage)) / float(close_last)

            # else:
            # quantity = ((((float(used_balance["USDT"])+float(free_balance["USDT"])) / 100 ) * float(order_percent)) * float(leverage)) / float(close_last)

            if ema_last<close_last:
                # if rsi_buy:
                #     if rsi_val<close_last:
                # #### BUY ####
                #         longEnter(position_inf,quantity)
                #         # quantity_buy=((float(binance_client.futures_account()['assets'][1]['walletBalance'])-float(binance_client.futures_account()['assets'][1]['availableBalance']))/close_last)*0.99 * float(leverage)
                #         # binance_order(symbol,'BUY',quantity_buy,close_last)
                #         print('RSI BUY ' )
                
       
                if ema_trig:
                    longEnter(position_inf,quantity)
                    # quantity_buy=((float(binance_client.futures_account()['assets'][1]['walletBalance'])-float(binance_client.futures_account()['assets'][1]['availableBalance']))/close_last)*0.99 * float(leverage)
                    # binance_order(symbol,'BUY',quantity_buy,close_last)
                    print('BUY ' )
            elif ema_last>close_last :
                # if rsi_sell:
                #     if rsi_val>close_last:
                #         #### SELL ####
                #         longExit(position_inf,quantity)
                #         print('RSI SELL' )
                # elif rsi_buy==False:
                if ema_trig:        
                    longExit(position_inf,quantity)
                    print('SELL' )
        # else:
        #     pushbullet_noti("No Order", +' at time '+str(dt.datetime.now()), 'TotalWallet= ' + str(balance['total']["USDT"]))
        
        # pushbullet_noti("Casual Notification", +' at time '+str(dt.datetime.now()), 'TotalWallet= ' + str(balance['total']["USDT"]))
        
        close_val.pop(0)
    # mov=current_closed*(exp_per/(1+EMA_PERIOD))+mov_ema*(1-exp_per/(1+EMA_PERIOD))
    # ex_mov=mov
        email_alert("Casual Notification", ' at time '+str(dt.datetime.now())+ ' TotalWallet= ' + str(balance['total']["USDT"]), "wmi1orhan@gmail.com")

        print('TotalWallet= ' + str(balance['total']["USDT"]))
        print('AvailableBalance= ' + str(free_balance["USDT"]))
        print('Close Val= '+str(close_last))
        print('RSI= '+str(rsi[-1]))
        print('EMA= '+str(ema_last))
        print('FirstBuy= {}'.format(first_buy))
        print('FirstSell= {}'.format(first_sell))
        print('----------------------------------------------')
        # pushbullet_noti("Casual Notification", ' at time '+str(dt.datetime.now())+ ' TotalWallet= ' + str(balance['total']["USDT"]))

    # print(torch.tensor(float(candle['c'])))
    # ema
ws=websocket.WebSocketApp(SOCKET, on_open=on_open,on_close=on_close, on_message=on_message)
ws.run_forever()
# ema2=ema2.drop(ema2.index[0:lenght])

