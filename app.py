from flask import Flask, render_template, url_for

app = Flask(__name__)


@app.route('/')
@app.route('/home')
def hello_world():  # put application's code here
    return render_template("index.html")


@app.route('/user/<string:name>/<int:id>')
def print_user(name,id):
    name = name.title() # Заглавная буква
    return f'User {name}, id {str(id)}'


@app.route('/about')
def about():  # put application's code here
    return render_template("about.html")


if __name__ == '__main__':
    app.run()
