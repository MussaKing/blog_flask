from flask import Flask

app = Flask(__name__)


@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'


@app.route('/hi')
def hi_world():  # put application's code here
    return 'hi World!'


if __name__ == '__main__':
    app.run()
