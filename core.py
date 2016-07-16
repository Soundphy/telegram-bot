"""
Core functions.
"""
import requests
import os
from telegram import InlineQueryResultAudio
import logging
from datetime import datetime


# Enable logging
logging.basicConfig(
    filename=os.path.join(os.path.dirname(__file__), 'core.log'),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.DEBUG)

logger = logging.getLogger(__name__)


# Define handlers.
def helpbot(bot, update):
    bot.sendMessage(update.message.chat_id, text='Help!')

def start(bot, update):
    text = 'This bot can help you find and share sounds. It works'+\
    ' automatically, no need to add it anywhere. Simply open any of '+\
    'your chats and type `@SoundphyBot something` in the message '+\
    'field. Then tap on a result to send. For example, try typing '+\
    '`@SoundphyBot Star Wars` here.'''
    bot.sendMessage(update.message.chat_id, text=text,\
        parse_mode='Markdown')

def inlinequery(bot, update):
    query = update.inline_query.query.strip()
    if not query or len(query) < 2:
        response = requests.get(
            'https://soundphy-peque.rhcloud.com/v0/popular')
    else:
        response = requests.get(
            'https://soundphy-peque.rhcloud.com/v0/search/' + query)
    data = response.json()['results']
    if not data:
        troll = 'https://www.myinstants.com/media/sounds/epic.swf_1.mp3'
        results = [InlineQueryResultAudio(id='0'*40,
                                    audio_url=troll,
                                    performer='Try again 😁',
                                    title='NOT FOUND')]
    else:
        results = [InlineQueryResultAudio(id=item['identifier'],
                                    audio_url=item['url'],
                                    performer=performer(item),
                                    title=item['title'].rstrip('\\'))
                                    for item in data]
    bot.answerInlineQuery(update.inline_query.id, results=results)

def error(bot, update, error):
    logger.warn('Update "%s" caused error "%s"' % (update, error))


def collectfeedback(bot, update):
    chosen_query = update.chosen_inline_result.query.strip()
    result_id = update.chosen_inline_result.result_id.strip()
    user_id = update.chosen_inline_result.from_user.id
    date_time = str(datetime.utcnow())
    fout = os.path.join(os.environ.get('OPENSHIFT_DATA_DIR'),
                        'collectfeed.csv')
    with open(fout, 'a') as f:
        f.write(date_time + ',' + result_id + ',' + str(user_id) +
                ',' + chosen_query + '\n')

# Define auxiliar functions
def performer(item):
    sequence = ['subsection', 'section', 'category', 'description']
    chain = ' / '.join(item[key] for key in sequence if item[key])
    # Telegram api automatically cuts long chains,code below for
    # cosmetic reasons
    if len(chain) > 100:
        chain = chain[:96]+' ...'
    return chain
