from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_restful import Api, Resource, reqparse
import json



app = Flask(__name__)
api = Api(app)
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

    def to_dict(self):
        fields = {
            'title': self.title,
            'intro': self.intro,
            'text': self.text,
            'date': self.date,
        }
        return fields

    def __repr__(self):
        return '<Article %r>' % self.id


class Quote(Resource):

    def get(self):
        # парсер запросов
        parser = reqparse.RequestParser()
        parser.add_argument("id")
        params = parser.parse_args()
        id_loc = params["id"]

        article = Article.query.get(id_loc)

        # Конвертация class в json
        article = json.dumps(article.to_dict(), ensure_ascii=False, indent=4, sort_keys=True, default=str)

        return article, 200

    def post(self):
        # парсер запросов
        parser = reqparse.RequestParser()
        parser.add_argument("title")
        parser.add_argument("intro")
        parser.add_argument("text")
        params = parser.parse_args()

        #print(params["id"])

        title = params["title"]
        intro = params["intro"]
        text = params["text"]

        article = Article(title=title, intro=intro, text=text)

        try:
            db.session.add(article)
            db.session.commit()
            return f"post added"
        except:
            return "Error add"

    def put(self):
        parser = reqparse.RequestParser()
        parser.add_argument("id")
        parser.add_argument("title")
        parser.add_argument("intro")
        parser.add_argument("text")
        params = parser.parse_args()

        # print(params["id"])

        id_loc = params["id"]
        article = Article.query.get(id_loc)

        article.title = params["title"]
        article.intro = params["intro"]
        article.text = params["text"]

        try:
            db.session.commit()
            return "blog successfully update", 201
        except:
            return "Error update", 400

    def delete(self):
        # парсер запросов
        parser = reqparse.RequestParser()
        parser.add_argument("id")
        params = parser.parse_args()
        id_loc = params["id"]

        article = Article.query.get_or_404(id_loc)
        try:
            db.session.delete(article)
            db.session.commit()
            return f"Quote with id {id_loc} is deleted.", 200
        except:
            return "Error", 400


api.add_resource(Quote, "/blog", "/blog/", "/blog/<int:id>")
if __name__ == '__main__':
    app.debug = True
    app.run()