import telebot
from telebot.types import ReplyKeyboardMarkup,ReplyKeyboardRemove
import requests
import datetime

API_TOKEN = '8468849460:AAHCwpvGVqbLBHtRlSBfHKJxeNrO2bc8QSE'

coins = {"1":"BTC","2":"BNB","3":"XRP","4":"ADA","5":"DOT","6":"AVAX","7":"LINK","8":"LTC"}

bot = telebot.TeleBot(API_TOKEN)

user_data = dict()
user_stap = dict()
coin_stap = dict()
cion_name = dict()

comands = {'start'             :'ای کامند برای شروع است',
           'help'              :'این کامند برای راهنمایی است',
           'sample_Keyboard'   :'این کامند برای ایجاد دکمه است',
           'remove_keyboard'   :'این کامند برای حذف دکمه است',
                        }

hideboard = ReplyKeyboardRemove()

@bot.message_handler(commands=['start'])
def send_welcome(message):
    cid = message.chat.id
    bot.send_message(cid,"به ربات من خوش امدید",reply_to_message_id=message.message_id)
    keyboard = ReplyKeyboardMarkup()
    keyboard.add('BTC' , 'BNB')
    keyboard.add('XRP' , 'ADA')
    keyboard.add('DOT' , 'AVAX')
    keyboard.add('LINK' ,'LTC' )
    bot.send_message(cid, 'دکمه های نام های ارز دیجیتال اضافه شد', reply_markup=keyboard)



@bot.message_handler(commands=['help'])
def send_welcome(message):
    cid = message.chat.id
    text = "این منو برای راهنمایی کارکرد کامند ها است\n"
    for camand,deac in comands.items():
        text += (f"{deac}: /{camand}\n")
    bot.send_message(cid,text,reply_to_message_id=message.message_id)


@bot.message_handler(commands=['sample_Keyboard'])
def command_sample_keyboard_handler(message):
    cid = message.chat.id
    key = ReplyKeyboardMarkup(resize_keyboard=True)
    key.add('BTC' , 'BNB')
    key.add('XRP' , 'ADA')
    key.add('DOT' , 'AVAX')
    key.add('LINK' ,'LTC' )
    bot.send_message(cid, 'here is your keyboard', reply_markup=key)

@bot.message_handler(commands=['remove_keyboard'])
def command_remove_keyboard_handle(message):
    cid = message.chat.id
    bot.send_message(cid,'این دکمه حذف شد',reply_markup=hideboard)



   



@bot.message_handler(func=lambda message: coin_stap.get(message.chat.id) == "X")
def last_price_coin(message):
    cid = message.chat.id
    BASE_URL = f"https://api.kucoin.com"
    params = {"symbol":f"{cion_name[cid]}-USDT","type":"1day"}
    response = requests.get(BASE_URL +"/api/v1/market/candles" , params=params)
    data = response.json()
    time_now = datetime.datetime.today()

    
    delta = datetime.timedelta(int(message.text))
    candle = data['data'][int(message.text)]
    price = candle[2]  
    time = time_now - delta
    data_time = time.strftime("%Y/%b/%d")
    bot.send_message(cid,f"{data_time} : {price}$") 
    coin_stap[cid] = "I"
    key = ReplyKeyboardMarkup(resize_keyboard=True)
    key.add('BTC' , 'BNB')
    key.add('XRP' , 'ADA')
    key.add('DOT' , 'AVAX')
    key.add('LINK' ,'LTC' )
    bot.send_message(cid, 'here is your keyboard', reply_markup=key)



@bot.message_handler(func=lambda message: coin_stap.get(message.chat.id) == "Z")
def last_price_coin(message):
    cid = message.chat.id
    BASE_URL = f"https://api.kucoin.com"
    params = {"symbol":f"{cion_name[cid]}-USDT","type":"1day"}
    response = requests.get(BASE_URL +"/api/v1/market/candles" , params=params)
    data = response.json()
    time_now = datetime.datetime.today()

    
    
    count = 0
    for j in range(int(message.text) + 1):
        number =  int(message.text) - count
        delta = datetime.timedelta(number)
        candle = data['data'][j]
        price = candle[2]  
        time = time_now - delta
        data_time = time.strftime("%Y/%b/%d")
        bot.send_message(cid, f"{data_time} : {price}$")
        count+=1
        
    coin_stap[cid] = "I"
    key = ReplyKeyboardMarkup(resize_keyboard=True)
    key.add('BTC' , 'BNB')
    key.add('XRP' , 'ADA')
    key.add('DOT' , 'AVAX')
    key.add('LINK' ,'LTC' )
    bot.send_message(cid, 'here is your keyboard', reply_markup=key)


text = ""
@bot.message_handler(func=lambda message: (coin_stap.get(message.chat.id) != "X" and coin_stap.get(message.chat.id) != "Y") or coin_stap.get(message.chat.id) == "I"  )
def get_coin(message):
    cid = message.chat.id
    for coin in coins:
        if message.text == coins[coin] :
            text = coins[coin]
            keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
            keyboard.add("1:قیمت الان")
            keyboard.add("2:قیمت گزشته")
            keyboard.add("3:(دوره زمانی)قیمت گزشته")
            bot.send_message(cid,"دکمه کوین",reply_markup=keyboard)
            coin_stap[cid] = "Y"
            cion_name[cid] = text
            break


@bot.message_handler(func=lambda message: coin_stap.get(message.chat.id) == "Y" )
def button_coin(message):
    cid = message.chat.id
    if message.text == "1" or message.text == "1:قیمت الان" :
        BASE_URL = "https://api.kucoin.com"
        params = {"symbol":f"{cion_name[cid]}-USDT","type":"1day"}
        response = requests.get(BASE_URL+ "/api/v1/market/orderbook/level1" , params=params )
        data = response.json()
        bot.send_message(cid,f"{datetime.datetime.today()} : {data['data']['price']}$")
        coin_stap[cid] = "I"
        key = ReplyKeyboardMarkup(resize_keyboard=True)
        key.add('BTC' , 'BNB')
        key.add('XRP' , 'ADA')
        key.add('DOT' , 'AVAX')
        key.add('LINK' ,'LTC' )
        bot.send_message(cid, 'here is your keyboard', reply_markup=key)

    elif message.text == "2" or message.text == "2:قیمت گزشته":
        bot.send_message(cid,"قیمت چند روز گذشته را میخواهید ببینید:")
        coin_stap[cid] = "X"

    elif message.text == "3" or message.text == "3:(دوره زمانی)قیمت گزشته":
        bot.send_message(cid,"قیمت چند روز گذشته را میخواهید ببینید:")
        coin_stap[cid] = "Z"


bot.infinity_polling()