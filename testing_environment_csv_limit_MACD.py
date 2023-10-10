# -*- coding: utf-8 -*-
"""
Created on Wed Aug 31 17:13:55 2022

@author: orhan
"""

import pandas as pd
# from binance import Client
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

# exchange.set_sandbox_mode(True) # activates testnet mode
TIME_LARGE='4h'
TIME_PERIOD='15m'
SUB_TIME='3m'
# interval='30m'
symbol_name='SOL'
symbol=symbol_name+'USDT'
newSymbol=symbol_name+'/USDT'
leverage=1

import numpy as np
import websocket, json, talib
import pandas_ta as ta

prices=exchange.fetch_ohlcv(newSymbol, timeframe=TIME_PERIOD, limit=200) # open-high-low-close
price=np.array((prices)).astype(float)

EMA_PERIOD=14
RSI_PERIOD=14
VWMA_PERIOD=20

import pandas as pd



import smtplib
from email.message import EmailMessage


first_buy=False
first_sell=False



order_price=0
buy_trig=False
sell_trig=False
rsi_trig=False
ema_buy=False
ema_sell=False
margin_error='binance {"code":-2019,"msg":"Margin is insufficient."}'
quantity_error='binance {"code":-4003,"msg":"Quantity less than zero."}'
bound_errror='index -1 is out of bounds for axis 0 with size 0'
# time_error='InvalidNonce: binance {"code":-1021,"msg":"Timestamp for this request was 1000ms ahead of the server's time."}'
order_percent=100  
# close_val=data[0:len(data)-1].tolist()
# close_val=data[0:len(data)].tolist()
rsi_val=0


profit_trig=True

import datetime
import binance
from binance import Client

import time
# ohlcv = exchange.fetch_ohlcv(symbol, timeframe=TIME_PERIOD, since='2017-01-0100:00:00Z', limit=1000)
import requests
# symbol='LTCUSDT'
rsi_count=0
# prices=exchange.fetch_ohlcv(newSymbol, timeframe=TIME_PERIOD, limit=1500)
fee=0.001*leverage
# mymoney=100
quantity=0

order_percent=1
str(datetime.datetime.fromtimestamp(1576995300.0))


path='D:/Orhan/Bitcoin/bit/sol_usdt_15m.csv'
# path='D:/Orhan/Bitcoin/bit/data/Hour_data/Bitfinex_ETHUSD_1h.csv'
# 666
prices=pd.read_csv(path)


loss_exit=-0.025
profit_exit=0.02

start=len(prices)-20000
n_frame=3
profit=[]
# x=1370
available_money=100
used_money=0
prof_rate=0

for i in range(start,len(prices)-70):
        # price = [ f for x,f in enumerate(np.array((prices))[i:i+90].astype(float)) if (x%n_frame==0) ]
        price=np.array((prices.values))[i:i+70].astype(float)
        # torch.cat((data,torch.tensor(float(candle['c']))), dim=0)
        if i%100==0:
            print('Iteration',int(i))

        macd=talib.MACD(price[:,4], 26, 12,  9)
        macd=macd[2]
        ema=talib.EMA(price[:,4], timeperiod = EMA_PERIOD)
        rsi=talib.RSI(price[:,4], timeperiod = RSI_PERIOD)
        rsi_sma=talib.SMA(rsi, timeperiod = EMA_PERIOD)
        vwma_val=((price[:,2]+price[:,3]+price[:,4])/3)*price[:,5]
        wma=talib.SMA(np.array(vwma_val), timeperiod = VWMA_PERIOD)
        volume_ema=talib.SMA(price[:,5], timeperiod = VWMA_PERIOD)
        vwma=wma/volume_ema
        
        # vwma=talib.EMA(price[:,4], timeperiod = RSI_PERIOD)
        vwma_last=vwma[-1]
        vwma_prev=vwma[-2]
        
        
        rsi_sma_last=rsi[-1]-rsi_sma[-1]
        rsi_sma_prev=rsi[-2]-rsi_sma[-2]
        
        # ema_last=ema[-1]
        # ema_prev=ema[-2]
        
        close_last=price[-1,4]
        close_prev=price[-2,4]
        
        macd_last=macd[-1]
        macd_prev=macd[-2]
        
        high_val=price[-1,2]
        low_val=price[-1,3]
        

 # EXIT
        
        # SHORT EXIT

        if ema_buy==True and first_sell :
            if (order_price-low_val)/order_price>profit_exit  :

                    profit.append(profit_exit)
                    available_money+=used_money*profit_exit+used_money
                    used_money=0
                    print('Profit = '+str(profit_exit))
                    first_buy=False
                    first_sell=False

                    print('EXIT' )
                    print('SELL ' )
                    ema_buy=False
                    used_money=available_money*order_percent
                    available_money-=used_money                          
                    # order_price=close_last+profit_exit*close_last

            if (order_price-high_val)/order_price<loss_exit:
                    profit.append(loss_exit)
                    print('Profit = '+str(loss_exit))
                    first_buy=False
                    first_sell=False

                    print('EXIT SELL' )
                   # print('SELL' )
                    ema_buy=False
                    available_money+=used_money*loss_exit+used_money
                    used_money=0   
                   
                    
        # LONG EXIT             
        elif ema_sell==True and first_buy:
       
                # # if ema_sell==True :  
                if (high_val-order_price)/order_price>profit_exit  :  
                    profit.append(profit_exit)
                    print('Profit = '+str(profit_exit))
                    first_buy=False
                    first_sell=False
                    available_money+=used_money*profit_exit+used_money

                    print('EXIT' )
                    print('BUY' )

                    ema_sell=False
                    
                    # order_price=close_last+profit_exit*close_last
                    used_money=available_money*order_percent
                    available_money-=used_money      
                if (low_val-order_price)/order_price<=loss_exit:
                    profit.append(loss_exit)
                    print('Profit = '+str(loss_exit))
                    first_buy=False
                    first_sell=False
                    
                    print('EXIT BUY' )
                    ema_sell=False
                    available_money+=used_money*loss_exit+used_money
                    used_money=0             
    
    
        
        
        # ENTER
        if macd_last*macd_prev<0 :
                # LONG ENTER
                if macd_last>0 :

                        # #### BUY ####

                        ema_buy=False
                        ema_sell=True
                        if first_sell==False and first_buy==False:
                            first_buy=True
                            # ema_sell=True
                            print('FIRST BUY')
                            order_price=close_last
                            print('Order Price = '+str(order_price))
                            used_money=available_money*order_percent
                            available_money-=used_money
                            
                        elif first_sell:
                            
                            profit.append((order_price-close_last)/order_price)
                            available_money+=used_money*(order_price-close_last)/order_price+used_money
                            used_money=0
                            print('Profit = '+str((order_price-close_last)/order_price))
                            print('EXIT' )
                            print('BUY')
                            first_buy=True
                            # first_buy=True
                            first_sell=False
                            # ema_sell=True
                            order_price=close_last
                            used_money=available_money*order_percent
                            available_money-=used_money
                            print('Order Price = '+str(order_price))

                # SHORT ENTER  
                elif  macd_last<0 :

                        ema_buy=True
                        ema_sell=False
                        if first_buy==False and first_sell==False:
                            print('FIRST SELL')
                            first_sell=True
                            order_price=close_last
                            print('Order Price = '+str(order_price))
                            used_money=available_money*order_percent
                            available_money-=used_money                            
                        elif first_buy:
                            
                            profit.append((close_last-order_price)/close_last)
                            print('Profit = '+str((close_last-order_price)/close_last))
                            print('EXIT' )
                            available_money+=used_money*(close_last-order_price)/close_last+used_money
                            used_money=0
                            first_buy=False
                            first_sell=True
                            print('SELL')

                            used_money=available_money*order_percent
                            available_money-=used_money  
                            order_price=close_last
                            print('Order Price = '+str(order_price))
                            

        print('Close val = '+str(close_last))
        print('MACD = '+str(macd_last))

        print('----------------')

import math
mymoney=100
leverage=12
fee=0.0017
x=0
order_percent=0.33

            
for j in profit:
    if j!=-math.inf:
        mymoney=mymoney*order_percent*j*leverage+mymoney*(1-fee*order_percent)
    if j==-math.inf:
        print(j)
    
print('Total Money=',mymoney )    
count=0

