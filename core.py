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


def inlinequery(bot, update):
    query = update.inline_query.query.strip()
    if not query or len(query) < 2:
        results = [
            InlineQueryResultAudio(id="eadb1b7155669cee75207fc5065ab4a4389ef3d4",
                                      audio_url='http://www.instantsfun.es/audio/applause.mp3',
                                      performer=None,
                                      title='Applause'),
            InlineQueryResultAudio(id="2d0dd9f34f0201ebeb9426cf32f768cfa20e4c99",
                                      audio_url="http://www.instantsfun.es/audio/star_wars_noooo.mp3",
                                      performer='Darth Vader. Star wars',
                                      title='Noooo'),
            InlineQueryResultAudio(id="8ac748e7a6f92c197e5c1663fc0efa8dceb09f7a",
                                      audio_url="http://www.instantsfun.es/audio/challenge_accepted.mp3",
                                      performer='Barney. How I met your mother',
                                      title= "Challenge accepted"),
            InlineQueryResultAudio(id='f3a1589b686014a6edf79626c8ce3ecc36d70caf',
                                      audio_url= 'http://www.instantsfun.es/audio/ha_ha.mp3',
                                      performer='Nelson. The Simpsons',
                                      title='Ha ha'),
            InlineQueryResultAudio(id='eec6e23d7367029c438c633cdab59ea81a17a903',
                                      audio_url= 'http://www.instantsfun.es/audio/crickets.mp3',
                                      performer=None,
                                      title='Crickets'),
        ]
    else:
        response = requests.get(
            'https://soundphy-peque.rhcloud.com/v0/search/' + query)
        data = response.json()['results']
        # Make sure all IDs are unique
        data = list(dict((x['identifier'], x) for x in data).values())
        results = [InlineQueryResultAudio(id=item['identifier'],
                                          audio_url=item['url'],
                                          title=item['title'].rstrip('\\'))
                   for item in data]
    bot.answerInlineQuery(update.inline_query.id, results=results,
                          cache_time=0)

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
