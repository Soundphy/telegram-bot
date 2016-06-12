from flask import Flask
from multiprocessing import Process
from SoundphyBot import main


application = Flask('SoundphyBot')

@application.route("/")
def hello():
    return "Hello World"

p = Process(target=main)
p.start()

if __name__ == '__main__':
    from wsgiref.simple_server import make_server
    HOST, PORT = 'localhost', 5000
    print('Serving at http://%s:%s' % (HOST, PORT))
    make_server(HOST, PORT, application).serve_forever()
