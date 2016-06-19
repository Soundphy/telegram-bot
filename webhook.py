import os
import traceback
import pickle
import telegram
from telegram.ext import Updater, CommandHandler
from flask import Flask, request
from core import start

app = Flask('__name__')

TOKEN='230669572:AAGgkxuJsfrLvftBVfYYIVV1m8d610DZoQw'
bot = telegram.Bot(token= TOKEN)
# Create the Updater and pass it your bot's token.
updater = Updater(TOKEN)

# Get the dispatcher to register handlers
dp = updater.dispatcher

# on different commands - answer in Telegram
dp.add_handler(CommandHandler("start", start))

@app.route('/HOOK', methods=['POST'])
def webhook_handler():
    if request.method == "POST":
        try:
#            chat_id = update.message.chat.id
#            text = update.message.text
#            bot.sendMessage(chat_id=chat_id, text=text)
            getdata = request.get_json(force=True)
            update = telegram.Update.de_json(getdata)
            dp.processUpdate(update)
            fout = os.path.join(os.path.dirname(__file__), 'dump.pkl')
            pickle.dump(update.message.text, open(fout, 'wb'))
        except Exception as error:
            return str(update.message.text) + '\n' + traceback.format_exc()

    return 'ok'

@app.route('/set_webhook', methods=['GET', 'POST'])
def set_webhook():
    s = bot.setWebhook('https://devsoundphybot-cuacuak.rhcloud.com/HOOK')
    if s:
        return "webhook setup ok"
    else:
        return "webhook setup failed"


@app.route('/')
def index():
    return '.'

if __name__ == '__main__':
    app.run(host='localhost', port=5000, debug=True)
