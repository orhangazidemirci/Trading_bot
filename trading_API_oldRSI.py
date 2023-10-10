# -*- coding: utf-8 -*-
"""
Created on Sun Aug 14 02:52:11 2022

@author: orhan
"""
import pandas as pd
import datetime as dt

# # FUTURE API
user_key = 'YOUR USER KEY'
secret_key = 'YOUR SECRET KEY'

import ccxt

exchange = ccxt.binance({
"apiKey": user_key,
"secret": secret_key,

'options': {
'defaultType': 'future'
},
'enableRateLimit': True
})

TIME_PERIOD='15m'
symbol_name='LTC'
symbol=symbol_name+'USDT'
newSymbol=symbol_name+'/USDT'
leverage=5
exchange.setLeverage (leverage, symbol = symbol, params = {})

prices=exchange.fetch_ohlcv(newSymbol, timeframe=TIME_PERIOD, limit=30) # Get 30 rows of date-open-high-low-close-volume values of LTCUSDT for 15 min time interval 

data = pd.DataFrame(prices)
data.columns = ['datetime', 'open', 'high', 'low', 'close', 'volume']
data.index = [dt.datetime.fromtimestamp(x/1000.0) for x in data.datetime]
data=data.astype(float)

data=data.values[:,4] # Selecting only the close values
import numpy as np

import smtplib
from email.message import EmailMessage

#### Email Alert To Get Notified  
def email_alert(subject,body,to):
    msg= EmailMessage()
    msg.set_content(body)
    msg['subject']=subject
    msg['to']=to
    
    user="YOUR EMAIL"
    msg['from']=user
    password="your password"
    server=smtplib.SMTP("smtp.gmail.com",587)
    # server.ehlo()

    server.starttls()
    server.login(user, password)
    server.send_message(msg)
    server.quit()
    
    
    
email_alert("Hello", "World", "YOUR EMAIL") # Emailing 

import websocket, json, talib
SOCKET= "wss://stream.binance.com:9443/ws/ltcusdt@kline_{}".format(TIME_PERIOD)

EMA_PERIOD=7
RSI_PERIOD=14

first_buy=False
first_sell=False

rsi_buy=False
rsi_sell=False

margin_error='binance {"code":-2019,"msg":"Margin is insufficient."}'
quantity_error='binance {"code":-4003,"msg":"Quantity less than zero."}'
bound_errror='index -1 is out of bounds for axis 0 with size 0'
# time_error='InvalidNonce: binance {"code":-1021,"msg":"Timestamp for this request was 1000ms ahead of the server's time."}'
order_percent=99   
close_val=data[0:len(data)-1].tolist()
rsi_val=0

import requests

def Order_Status():
    global first_buy,first_sell,close_last,used_balance,free_balance,position_inf
    balance = exchange.fetch_balance()
    used_balance=exchange.fetch_used_balance()
    free_balance = exchange.fetch_free_balance()
    positions = balance['info']['positions']
    current_positions = [position for position in positions if float(position['positionAmt']) != 0 and position['symbol'] == symbol]
    position_inf = pd.DataFrame(current_positions, columns=["symbol", "entryPrice", "unrealizedProfit", "isolatedWallet", "positionAmt", "positionSide"])

    if len(position_inf.index)==0 :
        first_buy=False
        first_sell=False
        
    else:
        if float(position_inf["positionAmt"][len(position_inf.index) - 1])>0:
            first_buy=True
            first_sell=False
        elif float(position_inf["positionAmt"][len(position_inf.index) - 1])<0:

            first_buy=False
            first_sell=True    
        
        else:
            first_buy=False
            first_sell=False
            
# LONG ENTER
def RSI_Long(position_inf,quantity):
   global first_buy, first_sell,rsi_buy  
   print('FirstBuy= {}'.format(first_buy))
   print('FirstSell= {}'.format(first_sell))  
          
   try:
       while first_sell==True:
           
           order = exchange.create_market_buy_order(newSymbol, -1*float(position_inf["positionAmt"][len(position_inf.index) - 1]), {"reduceOnly": True})
           Order_Status()
       email_alert("Order", "RSI BUYING {} LTC coin at time ".format(order['amount'] )+str(dt.datetime.now())+" price= "+str(order['price']), "YOUR EMAIL")

   except:

       try:

           order = exchange.create_market_buy_order(newSymbol,-1*float(position_inf["positionAmt"][len(position_inf.index) - 1]), {"reduceOnly": True})
           Order_Status()

           email_alert("Order", "RSI BUYING {} LTC coin at time ".format(order['amount'] )+str(dt.datetime.now())+" price= "+str(order['price']), "YOUR EMAIL")

       except Exception as e:
           print('An exception occured - {}'.format(e))
           email_alert("Exception", "An exception occured - {} in RSI SELL".format(e), "YOUR EMAIL")

# LONG EXIT     
def RSI_Short(position_inf,quantity):
   global first_buy ,close_last
   global first_sell
   
  
   print('FirstBuy= {}'.format(first_buy))
   print('FirstSell= {}'.format(first_sell))            
           
   try:
       while first_buy==True:

           order = exchange.create_market_sell_order(newSymbol, float(position_inf["positionAmt"][len(position_inf.index) - 1]), {"reduceOnly": True})
           Order_Status()    
       email_alert("Order", "RSI SELLING {} LTC coin at time ".format(order['amount'] )+str(dt.datetime.now())+" price= "+str(order['price']), "YOUR EMAIL")

   except :

       try:
           
           order = exchange.create_market_sell_order(newSymbol, float(position_inf["positionAmt"][len(position_inf.index) - 1]), {"reduceOnly": True})
           email_alert("Order", "RSI SELLING {} LTC coin at time ".format(order['amount'] )+str(dt.datetime.now())+" price= "+str(order['price']), "YOUR EMAIL")

           first_buy=False
           first_sell=False

       except Exception as e:
           print('An exception occured - {}'.format(e))
           email_alert("Exception", "An exception occured - {} in RSI SELL".format(e), "YOUR EMAIL")


def on_open(ws):
    print("opened")

def on_close(ws):
    print("closed")

def on_message(ws,message):
    global  first_buy,first_sell,ema_trig
    json_message=json.loads(message)
    candle=json_message['k']
    is_candle_closed=candle['x']
    if is_candle_closed:
        prices=exchange.fetch_ohlcv(newSymbol, timeframe=TIME_PERIOD, limit=1)
        close_val.append(float(prices[0][4]))
        ema=talib.EMA(np.array(close_val), timeperiod = EMA_PERIOD)
        rsi=talib.RSI(np.array(close_val), timeperiod = RSI_PERIOD)
        ema_last=ema[-1]
        ema_prev=ema[-2]
        
        close_last=close_val[-1]
        close_prev=close_val[-2]
        
        Order_Status()     
        quantity = ((((float(used_balance["USDT"])+float(free_balance["USDT"])) / 100 ) * float(order_percent)) * float(leverage)) / float(close_last)
       
        if rsi[-1]<70 and rsi[-2]>70 and (ema_last-close_last)*(ema_prev-close_prev)>0:
            # SELLING COIN
            RSI_Short(position_inf,quantity)
            print('RSI SELL ' )
            email_alert("RSI SELL" , "YOUR EMAIL")

        if rsi[-1]>30 and rsi[-2]<30 and (ema_last-close_last)*(ema_prev-close_prev)>0:
            # BUYING COIN
            RSI_Long(position_inf,quantity)
            email_alert("RSI BUY" , "YOUR EMAIL")
            print('RSI BUY ' )
               
        close_val.pop(0)
        email_alert("Casual Notification", ' at time '+str(dt.datetime.now())+ ' TotalWallet= ' + str(balance['total']["USDT"]), "YOUR EMAIL")

        print('TotalWallet= ' + str(balance['total']["USDT"]))
        print('AvailableBalance= ' + str(free_balance["USDT"]))
        print('Close Val= '+str(close_last))
        print('RSI= '+str(rsi[-1]))
        print('EMA= '+str(ema_last))
        print('FirstBuy= {}'.format(first_buy))
        print('FirstSell= {}'.format(first_sell))
        print('----------------------------------------------')

ws=websocket.WebSocketApp(SOCKET, on_open=on_open,on_close=on_close, on_message=on_message)
ws.run_forever()

