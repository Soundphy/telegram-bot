#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Simple Bot to reply to Telegram messages
# This program is dedicated to the public domain under the CC0 license.
"""
This Bot uses the Updater class to handle the bot.

First, a few handler functions are defined. Then, those functions are passed to
the Dispatcher and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.

Usage:
Basic inline bot example. Applies different text transformations.
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
'''
    results.append(InlineQueryResultAudio(id=uuid4(),
                                          audio_url='http://www.instantsfun.es/audio/yeahhh.mp3',
                                          title='Yeah',
                                          input_message_content=
                                          InputTextMessageContent(
                                                'Yeah')))
    results.append(InlineQueryResultArticle(id=uuid4(),
                                            title="Caps",
                                            input_message_content=InputTextMessageContent(
                                                query.upper())))
'''
"""
from uuid import uuid4

import re

from telegram import InlineQueryResultArticle, ParseMode, \
    InputTextMessageContent, InlineQueryResultAudio, InlineQueryResultVoice
from telegram.ext import Updater, InlineQueryHandler, CommandHandler
import logging

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)


# Define a few command handlers. These usually take the two arguments bot and
# update. Error handlers also receive the raised TelegramError object in error.
def start(bot, update):
    bot.sendMessage(update.message.chat_id, text='Hi!')


def help(bot, update):
    bot.sendMessage(update.message.chat_id, text='Help!')


def escape_markdown(text):
    """Helper function to escape telegram markup symbols"""
    escape_chars = '\*_`\['
    return re.sub(r'([%s])' % escape_chars, r'\\\1', text)


def inlinequery(bot, update):
    query = update.inline_query.query
    results = list()
    results.append(InlineQueryResultVoice(id=uuid4(),
                                          voice_url='http://www.instantsfun.es/audio/acdc.ogg',
                                          title='yuju',
                                          voice_duration = 30
                                          ))

    results.append(InlineQueryResultAudio(id=uuid4(),
                                          audio_url='http://www.instantsfun.es/audio/yeahhh.mp3',
                                          title='yeah'
                                          ))
    #Development cache time 0
    bot.answerInlineQuery(update.inline_query.id, results=results,
    cache_time=0)

def error(bot, update, error):
    logger.warn('Update "%s" caused error "%s"' % (update, error))


def main():
    # Read the bot TOKEN
    with open('.tokenInlineDev', 'r') as f:
        token = f.read().rstrip()

    # Create the Updater and pass it your bot's token.
    updater = Updater(token)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))

    # on noncommand i.e message - echo the message on Telegram
    dp.add_handler(InlineQueryHandler(inlinequery))

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot. Clean old pending updates on Telegram
    # servers before starting to poll.
    updater.start_polling(clean=True)

    # Block until the user presses Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()