from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


# Создаем макет БД
class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    intro = db.Column(db.String(300), nullable=False)
    text = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Article %r>' % self.id


@app.route('/')
@app.route('/home')
def hello_world():  # put application's code here
    return render_template("index.html")


@app.route('/user/<string:name>/<int:id>')
def print_user(name, id):
    name = name.title()  # Заглавная буква
    return f'User {name}, id {str(id)}'


@app.route('/about')
def about():  # put application's code here
    return render_template("about.html")


@app.route('/create_blog', methods=['POST', 'GET'])
def create_blog():  # put application's code here
    if request.method == "POST":
        title = request.form['title']
        intro = request.form['intro']
        text = request.form['text']

        article = Article(title=title, intro=intro, text=text)
        print(article)

        try:
            db.session.add(article)
            db.session.commit()
            return redirect('/')
        except:
            return "Error add"
    else:
        return render_template("create_blog.html")


if __name__ == '__main__':
    app.debug = True
    app.run()
