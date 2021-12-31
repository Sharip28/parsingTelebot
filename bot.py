import csv
import telebot
from telebot import types
from code import main
from Mytoken import *

bot = telebot.TeleBot(token)

description_photo=types.InlineKeyboardMarkup()
btn1=types.InlineKeyboardButton('description',callback_data='description')
btn2=types.InlineKeyboardButton('photo',callback_data='photo')
btn3=types.InlineKeyboardButton('look for more info',callback_data='more')
btn4=types.InlineKeyboardButton('back',callback_data="back")
btn5=types.InlineKeyboardButton('quit',callback_data="quit")
description_photo.add(btn1,btn2,btn3,btn4,btn5)
x=[]
@bot.message_handler(commands=['start'])
def start(message):
    chat_id=message.chat.id
    username=message.from_user.first_name
    bot.send_message(chat_id,f'''Привет,{username}\n 
    Добро пожаловать в мой телеграм бот!У нас есть свежие для тебя новости,
    чтобы открыть меню новостей я попрошу тебя ввести что-нибудь)''')
    main()
file1=open('zagolovki.csv')
file1=file1.readlines()
file2=open('text.csv')
file2=file2.readlines()
file3=open('foto.csv') 
file3=file3.readlines() 
file4=open('url.csv') 
file4=file4.readlines() 
list1=[0,]

@bot.message_handler(content_types=['text'])
def start_text(message):
    chat_id=message.chat.id  
    inline_keyboard=types.InlineKeyboardMarkup()
    for i in range(10):
        btn=types.InlineKeyboardButton(text=str(file1[i]),callback_data=str(i))
        inline_keyboard.add(btn)
    bot.send_message(chat_id,'news:',reply_markup=inline_keyboard)  
ph=0
desc=0
mr=0
msg1=1
msg2=1
msg3=1
@bot.callback_query_handler(func=lambda c:True)
def inline(c):
    chat_id=c.message.chat.id
    for i in range(10):      
        if str(i)==c.data:
            x.append(i)  
            bot.edit_message_text('Some title news you can see Description and photo',chat_id,c.message.message_id,reply_markup=description_photo)  
    global ph,desc,mr,msg1,msg2,msg3
    if c.data =='description':     
        msg1=bot.send_message(chat_id,file2[x[-1]]).message_id
        desc+=1 
    if c.data=='photo':
        msg2=bot.send_message(chat_id,file3[x[-1]]).message_id
        ph+=1     
    if c.data=='more':
        mr+=1
        msg3=bot.send_message(chat_id,file4[x[-1]]).message_id      
    if c.data=='back':    
        if desc!=0:
            bot.delete_message(chat_id,msg1)
            desc-=1
        if ph!=0:
            bot.delete_message(chat_id,msg2)
            ph-=1
        if mr!=0:
            bot.delete_message(chat_id,msg3)
            mr-=1
        chat_id=c.message.chat.id
        inline_keyboard=types.InlineKeyboardMarkup()
        for i in range(10):
            btn=types.InlineKeyboardButton(text=str(file1[i]),callback_data=str(i))
            inline_keyboard.add(btn)
        bot.edit_message_text('вы вернулись назад:',chat_id,c.message.message_id,reply_markup=inline_keyboard)
    
    if c.data=='quit':
        username=c.from_user.first_name
        bot.send_message(chat_id,f'Пока,{username}')
        bot.send_sticker(chat_id,'CAACAgIAAxkBAAEBA7tgVz_C3cS75JUUwyuDUvhx9pXPJwACqQkAAnlc4gkW68sz_f3XOh4E')
        bot.send_message(chat_id,f'Надеюсь,тебе было полезно.Жду тебя еще)')               

bot.polling()