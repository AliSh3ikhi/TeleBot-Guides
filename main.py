import logging

import re

from uuid import uuid4

from PIL import Image

from telegram.ext import Updater
from telegram.ext import CommandHandler
from telegram.ext import CallbackQueryHandler
from telegram.ext import InlineQueryHandler

from telegram.chataction import ChatAction

from telegram import ReplyKeyboardMarkup
from telegram import InlineKeyboardButton
from telegram import InlineKeyboardMarkup
from telegram import InputTextMessageContent
from telegram import InlineQueryResultArticle


###########logging##############
logging.basicConfig(level=logging.DEBUG,format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

#########################

updater = Updater("1691911932:AAHIJxR05rApgtabjuGI_rqoukA-fWJ87aw")

def start(bot,update):

    # import pdb; pdb.set_trace()
    chat_id = update.message.chat_id

    first_name = update.message.chat.first_name
    last_name = update.message.chat.last_name

    bot.send_chat_action(chat_id, ChatAction.TYPING)
    bot.sendMessage(chat_id=chat_id,text="Hello, {first_name} {last_name}")


def services(bot,update):
    chat_id = update.message.chat_id

    keyboard = [
        ['My website'],
        ['My Linkedin','My resume'],
        ['My Stackoverflow','My github','My Twitter']
        ]

    bot.sendMessage(chat_id,'Which way do you want to contact with me?', 
                    reply_markup = ReplyKeyboardMarkup(keyboard,resize_keyboard=True,one_time_keyboard=True))


def shishe(bot, update):
    chat_id = update.message.chat_id

    keyboard = [
                    [
                        InlineKeyboardButton('My site','http://www.alisheikhi.com'),
                        InlineKeyboardButton('My Linkedin','http://www.alisheikhi.com'),
                    ],
                    [
                        InlineKeyboardButton('check', callback_data='3'),
                    ]
                ]

    bot.sendMessage(chat_id,'select link',reply_markup=InlineKeyboardMarkup(keyboard))


def shishe_handler_button(bot , update):

    query = update.callback_query
    data = query.data
    chat_id = query.message.chat_id
    message_id = query.message.message_id
    description = 'default test'

    if data == '3':
        description = 'this is button 3'


    bot.editMessageText(text=description,chat_id=chat_id,message_id=message_id)

# after set setinline in botfather -alisheikhi
def feature_inline_query(bot, update):
    query = update.inline_query.query

    result = list()

    result.append(InlineQueryResultArticle(id = uuid4(), title = 'UpserCase', input_message_content =
    InputTextMessageContent(query.upper())))

    result.append(InlineQueryResultArticle(id = uuid4(), title = 'LowerCase', input_message_content =
    InputTextMessageContent(query.lower())))

    result.append(InlineQueryResultArticle(id = uuid4(), title = 'Bold', input_message_content =
    InputTextMessageContent('<b>{query}</b>',parse_mode='html')))

    result.append(InlineQueryResultArticle(id = uuid4(), title = 'Italic', input_message_content =
    InputTextMessageContent('<i>{query}</i>',parse_mode='html')))

    result.append(InlineQueryResultArticle(id = uuid4(), title = 'Code', input_message_content =
    InputTextMessageContent('<code>{query}</code>',parse_mode='html')))

    result.append(InlineQueryResultArticle(id = uuid4(), title = 'Poem', input_message_content =
    InputTextMessageContent('<pre>{query}</pre>',parse_mode='html')))


    # link by regex
    query_label = re.search(r'\s?\w+',query).group().strip()
    query_website = 'http://www.{}'.format(re.search(r'\s\w+.\w+',query).group().strip())

    # html link
    result.append(InlineQueryResultArticle(id = uuid4(), title = 'link', input_message_content =
    InputTextMessageContent('<a href="{query_website}">{query_label}</a>',parse_mode='html')))

    # markdown link
    result.append(InlineQueryResultArticle(id = uuid4(), title = 'link2', input_message_content =
    InputTextMessageContent('[{query_label}]({query_website})',parse_mode='markdown')))


    bot.answerInlineQuery(result= result)


def photo(bot ,update):
    chat_id = update.message.chat_id

    bot.send_chat_action(chat_id,ChatAction.UPLOAD_PHOTO)
    img = Image.open('./img/mar.png')
    img.thumbnail((500,500))

    unique_id = str(uuid4())
    img.save('./garbage/thumbnail - '+ unique_id,'PNG')
    photo = open('./garbage/thumbnail - '+ unique_id , 'rb')

    bot.sendPhoto(chat_id,photo,'Picture')
    photo.close()


def document(bot, update):
    chat_id = update.message.chat_id
    bot.send_chat_action(chat_id,ChatAction.UPLOAD_DOCUMENT)
    doc = open('./other/resume.txt','rb')
    bot.sendDocument(chat_id,doc)
    doc.close()


start_command = CommandHandler('start',start)
service_command = CommandHandler('services',services)
shishe_command = CommandHandler('link',shishe)
photo_command = CommandHandler('photo',photo)
document_command = CommandHandler('document',document)


shishe_handler = CallbackQueryHandler(shishe_handler_button)
feature_handler = InlineQueryHandler(feature_inline_query)

updater.dispatcher.add_handler(start_command)
updater.dispatcher.add_handler(service_command)
updater.dispatcher.add_handler(shishe_command)
updater.dispatcher.add_handler(shishe_handler)
updater.dispatcher.add_handler(feature_handler)
updater.dispatcher.add_handler(photo_command)
updater.dispatcher.add_handler(document_command)


updater.start_polling()
updater.idle()