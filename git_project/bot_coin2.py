import telebot
from telebot.types import ReplyKeyboardMarkup,ReplyKeyboardRemove,InlineKeyboardMarkup,InlineKeyboardButton
import requests
import datetime

API_TOKEN = '8468849460:AAHCwpvGVqbLBHtRlSBfHKJxeNrO2bc8QSE'
bot = telebot.TeleBot(API_TOKEN)
name_coin = ""

li_st = ["data1" , "data2" , "data3" , "BTC" , "BNB" , "XRP" , "ADA" , "DOT" , "AVAX" , "LINK" , "LTC"]
step = dict()
coin_step = dict()



comands = {'start'             :'ای کامند برای شروع است',
           'help'              :'این کامند برای راهنمایی است',
           'send_inlinekeyboard'   :'این کامند برای ایجاد دکمه شیشه ای است'
                        }







@bot.message_handler(commands=['start'])
def send_welcome(message):
    cid = message.chat.id
    bot.send_message(cid,"به ربات من خوش امدید",reply_to_message_id=message.message_id)



@bot.message_handler(commands=['help'])
def send_welcome(message):
    cid = message.chat.id
    text = "این منو برای راهنمایی کارکرد کامند ها است\n"
    for camand,deac in comands.items():
        text += (f"{deac}: /{camand}\n")
    bot.send_message(cid,text,reply_to_message_id=message.message_id)



@bot.message_handler(commands=['send_inlinekeyboard'])
def command_send_inlinekeyboard_handler(message):
    cid = message.chat.id
    step[cid] = "A"
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton('BTC', callback_data='BTC') , InlineKeyboardButton('BNB', callback_data='BNB'))
    markup.add(InlineKeyboardButton('XRP', callback_data='XRP') , InlineKeyboardButton('ADA', callback_data='ADA'))
    markup.add(InlineKeyboardButton('DOT', callback_data='DOT') , InlineKeyboardButton('AVAX', callback_data='AVAX'))
    markup.add(InlineKeyboardButton('LINK', callback_data='LINK') , InlineKeyboardButton('LTC', callback_data='LTC'))
    
    bot.send_message(cid, 'از بین این ارز های دیجیتال یکی را انتخاب کنید', reply_markup=markup)



@bot.message_handler(func= lambda message: message.text == 'start')
def send_welcome(message):
    cid = message.chat.id
    bot.send_message(cid,"به ربات من خوش امدید",reply_to_message_id=message.message_id)
    markup = bot.send_message(cid,"دمکمه برای اضافه کردن لیست ارز دیجیتال",reply_markup=markup)



@bot.message_handler(func= lambda message: message.text == 'help')
def send_welcome(message):
    cid = message.chat.id
    text = "این منو برای راهنمایی کارکرد کامند ها است\n"
    for camand,deac in comands.items():
        text += (f"{deac}: /{camand}\n")
    bot.send_message(cid,text,reply_to_message_id=message.message_id)



@bot.message_handler(func= lambda message: message.text == 'send_inlinekeyboard')
def command_send_inlinekeyboard_handler(message):
    cid = message.chat.id
    step[cid] = "A"
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton('BTC', callback_data='BTC') , InlineKeyboardButton('BNB', callback_data='BNB'))
    markup.add(InlineKeyboardButton('XRP', callback_data='XRP') , InlineKeyboardButton('ADA', callback_data='ADA'))
    markup.add(InlineKeyboardButton('DOT', callback_data='DOT') , InlineKeyboardButton('AVAX', callback_data='AVAX'))
    markup.add(InlineKeyboardButton('LINK', callback_data='LINK') , InlineKeyboardButton('LTC', callback_data='LTC'))
    
    bot.send_message(cid, 'از بین این ارز های دیجیتال یکی را انتخاب کنید', reply_markup=markup)




@bot.callback_query_handler (func= lambda call : step[call.message.chat.id] == "A" )
def main(call) :
        cid = call.message.chat.id
        coin_step[cid] = call.data
        for data in li_st :
            if call.data == data :
                print(data)
                markup = InlineKeyboardMarkup()
                markup.add(InlineKeyboardButton("قیمت الان",callback_data="data1"))
                markup.add(InlineKeyboardButton("قیمت گزشته",callback_data="data2"))
                markup.add(InlineKeyboardButton("(دوره زمانی)قیمت گزشته",callback_data="data3"))
                bot.send_message(call.message.chat.id , 'از بین این ارز های دیجیتال یکی را انتخاب کنید', reply_markup=markup)
                step[cid] = "B"
                break



@bot.callback_query_handler(func= lambda call : step[call.message.chat.id] == "B")
def main2(call) :
        cid = call.message.chat.id
        for data in li_st :
            if call.data == data :

                if data == "data1":
                    BASE_URL = "https://api.kucoin.com"
                    params = {"symbol":f"{coin_step[cid]}-USDT","type":"1day"}
                    response = requests.get(BASE_URL+ "/api/v1/market/orderbook/level1" , params=params )
                    data_c = response.json()
                    bot.send_message(cid,f"{str(data_c['data']['price'])}$")
                    

                elif data == "data2" :
                     step[cid] = "C"
                     bot.send_message(cid,"قیمت چند روز گذشته را میخواهید ببینید:")

                elif data == "data3" :
                     step[cid] = "D"
                     bot.send_message(cid,"قیمت چند روز گذشته را میخواهید ببینید:")
                     
                break



@bot.message_handler(func=lambda message: step[message.chat.id] == "C")
def last_price_coin(message):
    cid = message.chat.id
    BASE_URL = f"https://api.kucoin.com"
    params = {"symbol":f"{coin_step[cid]}-USDT","type":"1day"}
    response = requests.get(BASE_URL +"/api/v1/market/candles" , params=params)
    data = response.json()
    time_now = datetime.datetime.today()

    
    delta = datetime.timedelta(int(message.text))
    candle = data['data'][int(message.text)]
    price = candle[2]  
    time = time_now - delta
    data_time = time.strftime("%Y/%b/%d")
    bot.send_message(cid,f"{data_time} : {price}$") 
    


@bot.message_handler(func=lambda message: step[message.chat.id] == "D")
def last_price_coin(message):
    cid = message.chat.id
    BASE_URL = f"https://api.kucoin.com"
    params = {"symbol":f"{coin_step[cid]}-USDT","type":"1day"}
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
        count += 1
        
   



bot.infinity_polling()