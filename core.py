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
"""
import re
import requests
import os
from telegram import InlineQueryResultAudio
import logging

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)


# Define handlers.
def helpbot(bot, update):
    bot.sendMessage(update.message.chat_id, text='Help!')

def inlinequery(bot, update):
    query = update.inline_query.query.strip()
    if not query:
        return
    response = requests.get('https://soundphy-peque.rhcloud.com/v0/search/' + query)
    data = response.json()['results']
    results = list()
    for item in data:
        results.append(InlineQueryResultAudio(id=item['identifier'],
                                          audio_url=item['url'],
                                          title=item['title']))
    bot.answerInlineQuery(update.inline_query.id, results=results,
    cache_time=0)

def error(bot, update, error):
    logger.warn('Update "%s" caused error "%s"' % (update, error))

def collectfeedback(bot, update):
    chosen_query = update.chosen_inline_result.query.strip()
    identifier = update.chosen_inline_result.result_id.strip()
    fout = os.path.join(os.path.dirname(__file__), 'collectfeed.csv')
    with open(fout, 'a') as f:
        f.write(identifier + ',' + chosen_query + '\n')
