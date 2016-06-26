import re
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
    if not query:
        return
    response = requests.get('https://soundphy-peque.rhcloud.com/v0/search/' + query)
    data = response.json()['results']
    # Make sure all IDs are unique
    data = list(dict((x['identifier'], x) for x in data).values())
    results = list()
    for item in data:
        results.append(InlineQueryResultAudio(id=item['identifier'],
                                          audio_url=item['url'],
                                          title=item['title'].rstrip('\\')))
    bot.answerInlineQuery(update.inline_query.id, results=results,
    cache_time=0)

def error(bot, update, error):
    logger.warn('Update "%s" caused error "%s"' % (update, error))

def collectfeedback(bot, update):
    chosen_query = update.chosen_inline_result.query.strip()
    result_id = update.chosen_inline_result.result_id.strip()
    user_id = update.chosen_inline_result.from_user.id
    date_time = str(datetime.utcnow())
    fout = os.path.join(os.environ.get('OPENSHIFT_DATA_DIR'), 'collectfeed.csv')
    with open(fout, 'a') as f:
        f.write(date_time + ',' + result_id + ',' + str(user_id)
        + ',' + chosen_query + '\n')
