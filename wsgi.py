from flask import Flask
from multiprocessing import Process
from soundphy_bot import main


application = Flask('soundphy_bot')

@application.route("/")
def hello():
    return "Hello World"

p = Process(target=main)

if __name__ == '__main__':
    from wsgiref.simple_server import make_server
    HOST, PORT = 'localhost', 5000
    print('Serving at http://%s:%s' % (HOST, PORT))
    make_server(HOST, PORT, application).serve_forever()
