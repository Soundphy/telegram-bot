from flask import Flask
from multiprocessing import Process
from SoundphyBot import main


application = Flask('SoundphyBot')

@application.route("/")
def hello():
    return "Hello World"

token = '222041805:AAGiJzBAGO1npx1yavCJc77ihv7t5dcnnRg'
p = Process(target=main, args=(token,))
p.start()

if __name__ == '__main__':
    from wsgiref.simple_server import make_server
    HOST, PORT = 'localhost', 5000
    print('Serving at http://%s:%s' % (HOST, PORT))
    make_server(HOST, PORT, application).serve_forever()
