# -*- coding: utf-8 -*-
"""# 安裝相關套件"""

# 安裝 行情 API sdk
# !pip install fugle-realtime

# 取得 fugle http API 
from fugle_realtime import HttpClient

import datetime
import pandas as pd
import requests
import time
import threading

"""# define notify function"""

class notify_setting():
    
    def __init__(self, api_token, line_token):
        
        self.api_token = api_token
        self.line_token = line_token

    def lineNotifyMessage(self, msg):
    
        headers = {
           "Authorization": "Bearer " + self.line_token, 
           "Content-Type" : "application/x-www-form-urlencoded"
       }

        payload = {'message': msg}
        r = requests.post("https://notify-api.line.me/api/notify", headers = headers, params = payload)
        return r.status_code
        
    def price_info(self, symbol_id):
        
        api_client = HttpClient(api_token=self.api_token)
        quote_data = api_client.intraday.quote(symbolId = symbol_id)['data']['quote']
        
        open_price = quote_data['priceOpen']['price']
        trade_price = quote_data['trade']['price']
        change_rate = quote_data['changePercent']
        
        url = f"https://www.fugle.tw/ai/{symbol_id}"
        
        self.open_price = open_price
        self.trade_price = trade_price
        self.change_rate = change_rate
        self.url = url
        
        
    def price_change_strategy(self, symbol_id, up_rate, down_rate):
        
        while True:
            
            self.price_info(symbol_id)
            
            if self.change_rate >= up_rate:
                
                self.lineNotifyMessage(f"\n\n OH！\n {symbol_id} 現在價格 {self.trade_price} 元 \n 漲跌幅 {self.change_rate} % \n 漲幅已超過 {str(up_rate)} % \n {self.url}")
                print('已送出提醒！')
                break                
                
            elif self.change_rate <= down_rate:
                
                self.lineNotifyMessage(f"\n\n OH！\n {symbol_id} 現在價格 {self.trade_price} 元 \n 漲跌幅 {self.change_rate} % \n 跌幅已超過 {str(-down_rate)} % \n {self.url}")
                print('已送出提醒！')
                break                
                
            else:
                print('Nothing')
                time.sleep(3)
    
    def price_strategy(self, symbol_id ,up_price, down_price):
        
        while True:
            
            self.price_info(symbol_id)
            
            if self.trade_price >= up_price:
                
                self.lineNotifyMessage(f"\n\n OH！\n {symbol_id} 現在價格 {self.trade_price} 元 \n 漲跌幅 {self.change_rate} % \n 已超過目標價 {str(up_price)} 元 \n {self.url}")
                print('已送出提醒！')
                break
                
            elif self.trade_price <= down_price:
               
                self.lineNotifyMessage(f"\n\n OH！\n {symbol_id} 現在價格 {self.trade_price} 元 \n 漲跌幅 {self.change_rate} % \n 已低於目標價 {str(down_price)} 元 \n {self.url}")
                print('已送出提醒！')
                break
                
            else:
                print('nothing')
                time.sleep(3)

# Set Your Fugle API Token from https://developer.fugle.tw/
api_token = 'YOUR_API_TOKEN'

# Set Your line Token from https://notify-bot.line.me/my/
line_token = 'YOUR_LINE_TOKEN'

"""# 參數設定"""

# 目標價上界訂定
symbol_id = '2314'

up_price = 75

down_price = 70

up_changerate = 8

down_changerate = -1

"""# 執行策略"""

line = notify_setting(api_token=api_token,
                      line_token=line_token)

# 執行策略一：目標價提醒

strategy_1 = threading.Thread(target=line.price_strategy, args=[symbol_id, up_price, down_price])
strategy_1.start()

# 執行策略二：漲跌幅提醒

strategy_2 = threading.Thread(target=line.price_change_strategy, args=[symbol_id, up_changerate, down_changerate])
strategy_2.start()

