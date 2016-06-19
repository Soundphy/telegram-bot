import os
import traceback
import pickle
import telegram
from telegram.ext import Updater, ChosenInlineResultHandler
from telegram.ext import CommandHandler, InlineQueryHandler
from flask import Flask, request
from core import helpbot, inlinequery, error, collectfeedback

app = Flask(__name__)

TOKEN_PATH = os.path.join(os.environ.get('OPENSHIFT_DATA_DIR'), 'token')
with open(TOKEN_PATH, 'r') as f:
    TOKEN = f.read().strip()
bot = telegram.Bot(token= TOKEN)

# Create telegram.ext/dispatcher to manage incoming requests.
# Once an update is handled, all further handlers are ignored.
# The order defines priority.
updater = Updater(TOKEN)
dp = updater.dispatcher
dp.add_handler(CommandHandler("help", helpbot))
dp.add_handler(InlineQueryHandler(inlinequery))
dp.add_handler(ChosenInlineResultHandler(collectfeedback))
dp.add_error_handler(error)

@app.route('/HOOK', methods=['POST'])
def webhook_handler():
    if request.method == "POST":
        try:
            getdata = request.get_json(force=True)
            update = telegram.Update.de_json(getdata)
            dp.processUpdate(update)
            fout = os.path.join(os.path.dirname(__file__), 'dump.pkl')
            pickle.dump(getdata, open(fout, 'wb'))
        except Exception as error:
            return traceback.format_exc()

    return 'ok'

@app.route('/set_webhook', methods=['GET', 'POST'])
def set_webhook():
    s = bot.setWebhook('https://' + os.environ['OPENSHIFT_APP_DNS']
    + '/HOOK')
    if s:
        return "webhook setup ok"
    else:
        return "webhook setup failed"

@app.route('/remove_webhook', methods=['GET', 'POST'])
def remove_webhook():
    s = bot.setWebhook('')
    if s:
        return "webhook removed ok"
    else:
        return "webhook removed failed"

@app.route('/')
def index():
    return '.'

if __name__ == '__main__':
    app.run(host='localhost', port=5000, debug=True)
