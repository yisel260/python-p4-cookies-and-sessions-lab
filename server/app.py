#!/usr/bin/env python3

from flask import Flask, make_response, jsonify, session
from flask_migrate import Migrate

from models import db, Article, User

app = Flask(__name__)
app.secret_key = b'Y\xf1Xz\x00\xad|eQ\x80t \xca\x1a\x10K'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/clear')
def clear_session():
    session['page_views'] = 0
    return {'message': '200: Successfully cleared session data.'}, 200

@app.route('/articles')
def index_articles():
    articles = Article.query.all()
    articles_dict = []
    for article in articles:
        articles_dict.append(article.to_dict())
    response = make_response(jsonify(articles_dict),200)
    return  response

@app.route('/articles/<int:id>')
def show_article(id):
  article = Article.query.filter(Article.id == id).first()

  if 'page_views' not in session:
    session['page_views'] = 0

  views_remaining = 3- session['page_views']
  session['page_views'] += 1


  if views_remaining > 0:
    article_dict= article.to_dict() 
    response = make_response(jsonify(article_dict),200)
    return response
  else: 
     response = {'message': 'Maximum pageview limit reached'}
     return make_response(response, 401)
     

if __name__ == '__main__':
    app.run(port=5555)
