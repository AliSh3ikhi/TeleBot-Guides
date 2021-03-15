import logging

import re


from uuid import uuid4

from telegram.ext import Updater
from telegram.ext import CommandHandler
from telegram.ext import CallbackQueryHandler
from telegram.ext import InlineQueryHandler

from telegram import error
from telegram.chataction import ChatAction
from telegram import ReplyKeyboardMarkup , InlineKeyboardButton , InlineKeyboardMarkup, InlineQueryResultArticle, InputTextMessageContent


logging.basicConfig(level=logging.DEBUG,format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')



updater = Updater("1691911932:AAHIJxR05rApgtabjuGI_rqoukA-fWJ87aw")

def start(bot,update,args):

    # import pdb; pdb.set_trace()
    chat_id = update.message.chat_id

    if not args:
        bot.sendMessage(chat_id,'please type your name after /start')
    elif len(args)==1:

        bot.send_chat_action(chat_id,ChatAction.TYPING)

        bot.sendMessage(chat_id=chat_id,text='hello, {args[0]}')
    else:
        bot.sendMessage(chat_id,'only type one word after start')


def services(bot, update):
    chat_id = update.message.chat_id

    keyboard = [
        ['key1'],
        ['key2','key3'],
        ['key4','key5','key6'],
        ]

    bot.sendMessage(chat_id,'Choose one key',reply_markup = ReplyKeyboardMarkup(keyboard,resize_keyboard=True,one_time_keyboard=True))


def favor(bot, update):
    chat_id = update.message.chat_id

    keyboard = [
        [
            InlineKeyboardButton('link 1','www.google.com'),
            InlineKeyboardButton('link 2','www.google.com'),
        ],
          [
            InlineKeyboardButton('check', callback_data='3'),
          ]
        ]

    bot.sendMessage(chat_id,'Choose one key',reply_markup = InlineKeyboardMarkup(keyboard))


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
    photo = open('./img/mar.jpg','rb')

    try:
        bot.sendPhoto(chat_id,photo,'Picture')
    except error.BadRequest as e:
        if str(e) == 'photo_invalid_dimensions':
            bot.sendMessage(chat_id,'large photo!')
        else:
            bot.sendMessage(chat_id,'try later...')
    photo.close()


def document(bot, update):
    chat_id = update.message.chat_id
    bot.send_chat_action(chat_id,ChatAction.UPLOAD_DOCUMENT)
    doc = open('./other/resume.txt','rb')
    bot.sendDocument(chat_id,doc)
    doc.close()




start_command = CommandHandler('start', start, pass_args=True)
services_command = CommandHandler('service',services)
favor_command = CommandHandler('favor',favor)
photo_command = CommandHandler('photo',photo)
document_command = CommandHandler('document',document)


shishe_hander = CallbackQueryHandler(shishe_handler_button)
feature_handler = InlineQueryHandler(feature_inline_query)


updater.dispatcher.add_handler(start_command)
updater.dispatcher.add_handler(services_command)
updater.dispatcher.add_handler(favor_command)
updater.dispatcher.add_handler(shishe_hander)
updater.dispatcher.add_handler(feature_handler)
updater.dispatcher.add_handler(photo_command)
updater.dispatcher.add_handler(document_command)


updater.start_polling()
updater.idle()