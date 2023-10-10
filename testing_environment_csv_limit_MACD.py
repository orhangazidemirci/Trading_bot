# -*- coding: utf-8 -*-
"""
Created on Wed Aug 31 17:13:55 2022

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
TIME_LARGE='4h'
TIME_PERIOD='15m'
SUB_TIME='3m'
# interval='30m'
symbol_name='SOL'
symbol=symbol_name+'USDT'
newSymbol=symbol_name+'/USDT'
leverage=1
# exchange.setLeverage (leverage, symbol = symbol, params = {})
import numpy as np
import websocket, json, talib
import pandas_ta as ta

prices=exchange.fetch_ohlcv(newSymbol, timeframe=TIME_PERIOD, limit=200) # open-high-low-close
price=np.array((prices)).astype(float)
# torch.cat((data,torch.tensor(float(candle['c']))), dim=0)
# ta.trend.MACD(price[:,4], 26, 12,  9)
# diff=pd.DataFrame(price[:,4])
# diff.columns = ['close']
# diff.ta.macd(close='close', fast=12, slow=26, signal=9, append=True)

# close_val.append(float(candle['c']))
# close_val.append(prices[0])
EMA_PERIOD=14
RSI_PERIOD=14
VWMA_PERIOD=20
# ema=talib.EMA(price[:,4], timeperiod = EMA_PERIOD)
# rsi=talib.RSI(price[:,4], timeperiod = RSI_PERIOD)

import pandas as pd


# macd_s,macd_l,macd=talib.MACD(price[:,4])

# rsi=talib.RSI(price[:,4], timeperiod = RSI_PERIOD)

# rsi_ema=talib.EMA(abs(rsi-50), timeperiod = EMA_PERIOD)
# macd_ema=talib.EMA(abs(macd_s+macd_l), timeperiod = EMA_PERIOD)
# macd_diff=macd[1:]-macd[0:-1]
# abs(macd_diff)<1 and  macd_ema<10
# abs(macd)<5 or (abs(rsi_ema-50))<5

# if macd<0:
#     if macd_diff>0:
#         print('SELL ONLY')
#     else:
#         print('OPEN TO BOTH SIDE')

# if macd>0:
#     if macd_diff>0:
#         print('BUY ONLY')
        
#     else:
#         print('OPEN TO BOTH SIDE')

# data = pd.DataFrame(prices)
#format columns name
# data.columns = ['datetime', 'open', 'high', 'low', 'close', 'volume']
# data.index = [dt.datetime.fromtimestamp(x/1000.0) for x in data.datetime]
# data=data.astype(float)

# data=data.values


import smtplib
from email.message import EmailMessage



# SOCKET= "wss://stream.binance.com:9443/ws/ltcusdt@kline_{}".format(TIME_PERIOD)
# SOCKET= "wss://stream.binance.com:9443/ws/ltcusdt@kline_1m"



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


# SOCKET= "wss://stream.binance.com:9443/ws/ltcusdt@kline_1m"

# def Trigger(sub_price):
#     global buy_trig,sell_trig
#     ema_sub=talib.EMA(sub_price[:,4], timeperiod = EMA_PERIOD)
    
#     vwma_val_sub=((sub_price[:,2]+sub_price[:,3]+sub_price[:,4])/3)*sub_price[:,5]
#     wma_sub=talib.SMA(np.array(vwma_val_sub), timeperiod = 14)
#     volume_ema_sub=talib.SMA(sub_price[:,5], timeperiod = 14)
#     vwma_sub=wma_sub/volume_ema_sub
    
#     # vwma=talib.EMA(price[:,4], timeperiod = RSI_PERIOD)
#     vwma_last_sub=vwma_sub[len(sub_price)-10:]
#     ema_last_sub=ema_sub[len(sub_price)-10:]
#     close_last_sub=sub_price[len(sub_price)-10:,4]
#     change=close_last_sub-vwma_last_sub
#     change[change>0]=1
#     change[change<0]=-1
#     if change[-1]<0:
#         sell_trig=True
#         buy_trig=False
#     else:
#         buy_trig=True
#         sell_trig=False

# balance = exchange.fetch_balance()
# free_balance = exchange.fetch_free_balance()
# positions = balance['info']['positions']

profit_trig=True

# price=np.array((prices)).astype(float)
# talib.MACD(price[:,4])

    #         print('You are leaked')
        
    # count=0
    
    # account=100
    
    # for j in profit:
    #   account+=leverage*account*j-account*fee
    #   if account<0:
    #     print('Fuck')
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

# path='D:/Orhan/Bitcoin/bit/eth_usdt_5m.csv'
# # path='D:/Orhan/Bitcoin/bit/data/Hour_data/Bitfinex_ETHUSD_1h.csv'
# # 1
# sub_prices=pd.read_csv(path)
# sub_prices.columns = ['close']
# sub_prices=sub_prices['close'].str.split(',', expand=True)
# sub_prices.pop(1)
# sub_prices.pop(2)
# sub_prices.pop(7)

path='D:/Orhan/Bitcoin/bit/sol_usdt_15m.csv'
# path='D:/Orhan/Bitcoin/bit/data/Hour_data/Bitfinex_ETHUSD_1h.csv'
# 666
prices=pd.read_csv(path)

# path='D:/Orhan/Bitcoin/bit/btc_usdt_15m.csv'
# # path='D:/Orhan/Bitcoin/bit/data/Hour_data/Bitfinex_ETHUSD_1h.csv'
# # 666
# prices_btc=pd.read_csv(path)# -25
# prices.columns = ['date', 'open', 'high', 'low', 'close', 'volume']
# prices_btc.columns = ['date', 'open', 'high', 'low', 'close', 'volume']
# prices_btc=prices_btc.add_suffix('_BTC')

# # prices_btc = prices_btc.iloc[25: , :]
# prices_btc=prices_btc.drop(prices_btc.copy().index[0:25])
# prices_btc=prices_btc.drop(prices_btc.copy().index[len(prices):])

# # prices_btc=prices_btc.drop(prices_btc.copy().index[0:25])


#  # x=x.copy().loc[x.notna()]
# #  x=x.drop(x.copy().index[0])
# prices_btc=prices_btc.values.tolist()
# prices_btc=pd.DataFrame(prices_btc)


# result = pd.concat([prices, prices_btc], axis=1, join='inner')
# result.head()

loss_exit=-0.025
profit_exit=0.02

# loss_exit=-0.02
# profit_exit=0.01
# prices.columns = ['close']
# prices=prices['close'].str.split(',', expand=True)
# prices.pop(1)
# prices.pop(2)
# prices.pop(7)
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
        
        
        # print('Iteration',int(i))            
        # close_val.append(float(candle['c']))
        # close_val.append(prices[0])
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
        
     #   sub_price=np.array((sub_prices))[i+1:i+31].astype(float)
        # Trigger(sub_price)
        # print(close_last,close_prev)
        
        # if first_buy or first_sell:
        #     totalmoney=mymoney+((close_last-order_price)*(quantity)+abs(quantity)*order_price)/leverage
        # else: 
        #     totalmoney=mymoney
           
        # EXIT
        
        # SHORT EXIT

        if ema_buy==True and first_sell :
            if (order_price-low_val)/order_price>profit_exit  :
                # if rsi_buy:
                #     if rsi_val<close_last:

                # if ema_buy==True:
                
                    # quantity = ((((totalmoney) / 100 ) * float(order_percent)) * float(leverage)) / float(close_last)
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
            # sub_price=np.array((prices))[i+60:i+87].astype(float)
            # Trigger(sub_price)
            # Profit_Trig(start,i)
                # rsi_trig=True
                # order_price=close_last
                # LONG ENTER
                if macd_last>0 :
                    # if rsi_buy:
                    #     if rsi_val<close_last:
                    # #### BUY ####
                    #         longEnter(position_inf,quantity)
                    #         # quantity_buy=((float(binance_client.futures_account()['assets'][1]['walletBalance'])-float(binance_client.futures_account()['assets'][1]['availableBalance']))/close_last)*0.99 * float(leverage)
                    #         # binance_order(symbol,'BUY',quantity_buy,close_last)
                    #         print('RSI BUY ' )
                    
                    # longEnter(position_inf,quantity)
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
                            
            # else:
            #     if first_sell==True:
            #         first_sell==False
            #         profit.append((order_price-close_last)/order_price)
            #         ema_buy=False
            #         ema_sell=False                        
                        
                # SHORT ENTER  
                elif  macd_last<0 :

                        ema_buy=True
                        ema_sell=False
                        if first_buy==False and first_sell==False:
                            print('FIRST SELL')
                            first_sell=True
                            # first_sell=False
                            # # quantity_buy=((float(binance_client.futures_account()['assets'][1]['walletBalance'])-float(binance_client.futures_account()['assets'][1]['availableBalance']))/close_last)*0.99 * float(leverage)
                            # # binance_order(symbol,'BUY',quantity_buy,close_last)
            
                            # ema_buy=True
                            order_price=close_last
                            print('Order Price = '+str(order_price))
                            used_money=available_money*order_percent
                            available_money-=used_money                            
                        elif first_buy:
                            
                            # quantity = -((((totalmoney) / 100 ) * float(order_percent-fee)) * float(leverage)) / float(close_last)
                            profit.append((close_last-order_price)/close_last)
                            print('Profit = '+str((close_last-order_price)/close_last))
                            print('EXIT' )
                            available_money+=used_money*(close_last-order_price)/close_last+used_money
                            used_money=0
                            # mymoney=0
                            first_buy=False
                            first_sell=True
                            print('SELL')
                            # quantity_buy=((float(binance_client.futures_account()['assets'][1]['walletBalance'])-float(binance_client.futures_account()['assets'][1]['availableBalance']))/close_last)*0.99 * float(leverage)
                            # binance_order(symbol,'BUY',quantity_buy,close_last)
                            # print('SELL' )
                            used_money=available_money*order_percent
                            available_money-=used_money  
                            order_price=close_last
                            print('Order Price = '+str(order_price))
                            
                            # ema_buy=True
                            # if rsi_sell:
                        #     if rsi_val>close_last:
                        #         #### SELL ####
                        #         longExit(position_inf,quantity)
                        #         print('RSI SELL' )
                        # elif rsi_buy==False:
    
        
  
        # print('BUY')
        # print('VWMA = '+str(vwma_last))
        print('Close val = '+str(close_last))
        print('MACD = '+str(macd_last))
        # print('RSI val = '+str(rsi[-1]))
        # print('RSI SMA val = '+str(rsi_sma[-1]))
        # print('VWMA = '+str(vwma_last))
        print('----------------')

        # else:
        #     pushbullet_noti("No Order", +' at time '+str(dt.datetime.now()), 'TotalWallet= ' + str(balance['total']["USDT"]))
        
        # pushbullet_noti("Casual Notification", +' at time '+str(dt.datetime.now()), 'TotalWallet= ' + str(balance['total']["USDT"]))
        
        # close_val.pop(0)
    # mov=current_closed*(exp_per/(1+EMA_PERIOD))+mov_ema*(1-exp_per/(1+EMA_PERIOD))
    # ex_mov=mov
        # email_alert("Casual Notification", ' at time '+str(dt.datetime.now())+ ' TotalWallet= ' + str(balance['total']["USDT"]), "wmi1orhan@gmail.com")

# for i in range(i,len(prices)-40+i):
#         # if i%4==0:
#         #     prices_large=binance_client.futures_historical_klines(symbol, TIME_LARGE, start_str=str(datetime.datetime.fromtimestamp(start-14400.0*50)), end_str=str(datetime.datetime.fromtimestamp(moving_per)))
#         #     price_large=np.array((prices_large)).astype(float)
#         price=np.array(((prices.values)))[i:i+40].astype(float)

#         rsi=talib.RSI(price[:,4], timeperiod = RSI_PERIOD)
#         rsi_ema=talib.EMA(abs(rsi-50), timeperiod = EMA_PERIOD)
        
#         macd_s,macd_l,macd=talib.MACD(price[:,4])
        
#         macd_ema=talib.EMA(abs(macd_s+macd_l), timeperiod = EMA_PERIOD)
#         macd_diff=macd[1:]-macd[0:-1]
        
#         # abs(macd_diff)<1 and  macd_ema<10
#         # abs(macd)<5 or (abs(rsi_ema-50))<5
        
                            
#         # price=np.array((prices))[i:i+40].astype(float)
#         # torch.cat((data,torch.tensor(float(candle['c']))), dim=0)
        
#         # close_val.append(float(candle['c']))
#         # close_val.append(prices[0])
#         ema=talib.EMA(price[:,4], timeperiod = EMA_PERIOD)
#         rsi=talib.RSI(price[:,4], timeperiod = RSI_PERIOD)
        
#         vwma_val=((price[:,2]+price[:,3]+price[:,4])/3)*price[:,5]
#         wma=talib.EMA(np.array(vwma_val), timeperiod = RSI_PERIOD)
#         volume_ema=talib.EMA(price[:,5], timeperiod = RSI_PERIOD)
#         vwma=wma/volume_ema
        
#         # vwma=talib.EMA(price[:,4], timeperiod = RSI_PERIOD)
#         macd_last=macd[-1]
#         macd_prev=macd[-2]
        
#         ema_last=ema[-1]
#         ema_prev=ema[-2]
        
#         close_last=price[-1,4]
#         close_prev=price[-2,4]
        
#         # if (abs(macd_diff[-1])<1 and  macd_ema[-1]<10) or abs(rsi_ema[-1]-50)<5:
#         #     print('EXIT ONLY')
#         # else:
#         if (macd_last)*(macd_prev)<0:   
#             if macd_last>0 :
#                 # if rsi_buy:
#                 #     if rsi_val<close_last:
#                 # #### BUY ####
#                 #         longEnter(position_inf,quantity)
#                 #         # quantity_buy=((float(binance_client.futures_account()['assets'][1]['walletBalance'])-float(binance_client.futures_account()['assets'][1]['availableBalance']))/close_last)*0.99 * float(leverage)
#                 #         # binance_order(symbol,'BUY',quantity_buy,close_last)
#                 #         print('RSI BUY ' )
                
#                 # longEnter(position_inf,quantity)
#                     print('MACD Last', macd_last)
#                     print('MACD Prev', macd_prev)
#                     print('Iteration', i)
#                     ema_buy=False
#                     ema_sell=True
#                     if first_sell==False and first_buy==False:
#                         first_buy=True
#                         # ema_sell=True
#                         print('FIRST BUY')
#                         order_price=close_last
#                         print('Order Price = '+str(order_price))
                        
#                     elif first_sell==True:
                        
#                         profit.append((order_price-close_last)/order_price)
#                         print('Profit = '+str((order_price-close_last)/order_price))
#                         print('Close Price = '+str(close_last))
#                         print('EXIT' )
#                         print('BUY')
#                         first_buy=True
#                         # first_buy=True
#                         first_sell=False
#                         # ema_sell=True
#                         order_price=close_last
#                         print('Order Price = '+str(order_price))
                        
#         # else:
#         #     if first_sell==True:
#     #         first_sell==False
#     #         profit.append((order_price-close_last)/order_price)
#     #         ema_buy=False
#     #         ema_sell=False                        
                        
#             # SHORT ENTER  
#             elif macd_last<0:
#                 print('MACD Last', macd_last)
#                 print('MACD Prev', macd_prev)
#                 ema_buy=True
#                 ema_sell=False
#                 if first_buy==False and first_sell==False:
#                     print('FIRST SELL')
#                     first_sell=True
#                     # first_sell=False
#                     # # quantity_buy=((float(binance_client.futures_account()['assets'][1]['walletBalance'])-float(binance_client.futures_account()['assets'][1]['availableBalance']))/close_last)*0.99 * float(leverage)
#                     # # binance_order(symbol,'BUY',quantity_buy,close_last)
    
#                     # ema_buy=True
#                     order_price=close_last
#                     print('Order Price = '+str(order_price))
                    
#                 elif first_buy==True:
                    
#                     # quantity = -((((totalmoney) / 100 ) * float(order_percent-fee)) * float(leverage)) / float(close_last)
#                     profit.append((close_last-order_price)/close_last)
#                     print('Profit = '+str((close_last-order_price)/close_last))
#                     print('Close Price = '+str(close_last))
#                     print('EXIT' )
#                     # mymoney=0
#                     first_buy=False
#                     first_sell=True
#                     # print('SELL')
#                     # quantity_buy=((float(binance_client.futures_account()['assets'][1]['walletBalance'])-float(binance_client.futures_account()['assets'][1]['availableBalance']))/close_last)*0.99 * float(leverage)
#                     # binance_order(symbol,'BUY',quantity_buy,close_last)
#                     print('SELL' )
#                     order_price=close_last
#                     print('Order Price = '+str(order_price))
                
#                 # ema_buy=True
#                 # if rsi_sell:
#             #     if rsi_val>close_last:
#             #         #### SELL ####
#             #         longExit(position_inf,quantity)
#             #         print('RSI SELL' )
#                 # elif rsi_buy==False:
    

        
#         # # EXIT
#         # if (ema_last-close_last)*(ema_prev-close_prev)<0 and ((vwma_last-close_last)*(vwma_prev-close_prev)>0 or profit_trig or sell_trig or sell_trig):
#         #     # SHORT EXIT
#         #     if ema_last<close_last:
#         #         # if rsi_buy:
#         #         #     if rsi_val<close_last:
    
#         #         # if ema_buy==True:
#         #         if ema_buy==True and order_price>close_last:
#         #             # quantity = ((((totalmoney) / 100 ) * float(order_percent)) * float(leverage)) / float(close_last)
#         #             profit.append((order_price-close_last)/order_price)
#         #             # print('Profit = '+str((order_price-close_last)/order_price))
#         #             first_buy=False
#         #             first_sell=False
    
#         #             # print('EXIT SELL ' )
#         #             ema_buy=False
#         #             buy_trig=False
#         #             sell_trig=False
#         #     # LONG EXIT        
#         #     elif ema_last>close_last :
       
#         #         # if ema_sell==True :  
#         #         if ema_sell==True and order_price<close_last and order_price>0:  
#         #             profit.append((close_last-order_price)/close_last)
#         #             # print('Profit = '+str((close_last-order_price)/close_last))
#         #             first_buy=False
#         #             first_sell=False
#         #             buy_trig=False
#         #             sell_trig=False                        
#         #             # print('EXIT BUY' )
#         #             ema_sell=False                                        
#         #                         # ema_buy=True
#         #                         # if rsi_sell:
#         #                     #     if rsi_val>close_last:
#         #                     #         #### SELL ####
#         #                     #         longExit(position_inf,quantity)
#         #                     #         print('RSI SELL' )
#         #                     # elif rsi_buy==False:                        
                            
                            
                        
                    

#                             # if rsi_sell:
#                                 #     if rsi_val>close_last:
#                                 #         #### SELL ####
#                                 #         longExit(position_inf,quantity)
#                                 #         print('RSI SELL' )
#                             # elif rsi_buy==False:                        
 
                

#     # if first_buy or first_sell:
#         #     totalmoney=mymoney+((close_last-order_price)*(quantity)+abs(quantity)*order_price)/leverage
#         # else: 
#         #     totalmoney=mymoney
            
#         # ENTER

#         # print('VWMA = '+str(vwma_last))
#         # print('----------------')

#         # else:
#         #     pushbullet_noti("No Order", +' at time '+str(dt.datetime.now()), 'TotalWallet= ' + str(balance['total']["USDT"]))
        
#         # pushbullet_noti("Casual Notification", +' at time '+str(dt.datetime.now()), 'TotalWallet= ' + str(balance['total']["USDT"]))
        
#         # close_val.pop(0)
#     # mov=current_closed*(exp_per/(1+EMA_PERIOD))+mov_ema*(1-exp_per/(1+EMA_PERIOD))
  



import math
mymoney=100
leverage=12
fee=0.0017
x=0
order_percent=0.33

# for x in range(len(profit)//100):
#     mymoney=1
#     for j in profit[x*100:100+x*100]:
#         if j!=-math.inf:
#             mymoney=mymoney*order_percent*-j*leverage+mymoney*(1-fee*order_percent)
#         if j==-math.inf:
#             print(j)
#     print('Current Profit=',mymoney )    
            
for j in profit:
    if j!=-math.inf:
        mymoney=mymoney*order_percent*j*leverage+mymoney*(1-fee*order_percent)
    if j==-math.inf:
        print(j)
    
print('Total Money=',mymoney )    
count=0
for j in profit:
    if j!=-math.inf:
        count+=j
    
    if j>9.6:
        print('You are leaked')
    
count=0

account=100

for j in profit:
  # if j!=-math.inf:
  account+=leverage*account*j-account*fee
  if account<0:
    print('Fuck')
    
print('1 Day Profit= '+str(account/100) ) 
print('----------------------' ) 


# # importing pandas as pd


# # # dictionary of lists
# dict = {'Profit': profit}
# # 	
# df = pd.DataFrame(dict)
# # 	
# # saving the dataframe
# df.to_csv('D:/Orhan/Bitcoin/bit/profit2.csv')

# path='D:/Orhan/Bitcoin/bit/profit.csv'
# # path='D:/Orhan/Bitcoin/bit/data/Hour_data/Bitfinex_ETHUSD_1h.csv'
# # 666
# profit=pd.read_csv(path)
# profit=profit.values[:,1].tolist()


# import math
# mymoney=100
# leverage=5
# fee=0.001*leverage 
# x=350
# for i,j in enumerate(profit):
#     if j!=-math.inf:
#         mymoney=mymoney*j*leverage+mymoney*(1-fee)
#     if j==-math.inf:
#         print(j)
    
# print('Total Money=',mymoney )    
