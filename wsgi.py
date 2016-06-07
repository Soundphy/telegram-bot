from flask import Flask

application = Flask('SoundphyBot')

@application.route("/")
def hello():
    return "Hello World"

if __name__ == '__main__':
    from wsgiref.simple_server import make_server
    HOST, PORT = 'localhost', 5000
    print('Serving at http://%s:%s' % (HOST, PORT))
    make_server(HOST, PORT, application).serve_forever()
