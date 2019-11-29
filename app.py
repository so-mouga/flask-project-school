import csv, sys, os, pprint
from flask import Flask, request, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.orm.exc import MultipleResultsFound

# db variable initialization
app = Flask(__name__, instance_relative_config=True)
app.config["DEBUG"] = True
app.url_map.strict_slashes = False

app.config.from_pyfile('config.py')
db = SQLAlchemy(app)

class User(db.Model):
  __tablename__ = 'user'
  id = db.Column(db.Integer, primary_key=True)
  nickename = db.Column(db.String(4096))
  tweet = db.relationship('Tweet')

  def __init__(self, nickename):
    self.nickename = nickename

class Tweet(db.Model):
  __tablename__ = 'tweet'
  id = db.Column(db.Integer, primary_key=True)
  content = db.Column(db.String(4096))
  user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

  def __init__(self, content, user_id):
    self.content = content
    self.user_id = user_id


basedir = os.path.abspath(os.path.dirname(__file__))
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')

app.config["SQLALCHEMY_DATABASE_URI"] = SQLALCHEMY_DATABASE_URI
app.config["SQLALCHEMY_POOL_RECYCLE"] = 299
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.drop_all()
db.create_all()

db.session.add(User('ipssi'))
db.session.add(User('kevin'))

db.session.add(Tweet("lorem ippsu", 1))
db.session.add(Tweet("Hello Word", 1))
db.session.add(Tweet("test 1", 2))
db.session.add(Tweet("Hello Word", 2))
db.session.commit()

@app.after_request
def add_header(response):
    header = response.headers
    response.cache_control.max_age = 300
    header['Access-Control-Allow-Origin'] = [
        '195.154.176.62',
        '80.15.154.187'
    ]
    return response

@app.route('/')
def home():
  return 'Bienvenue'


@app.route('/timeline/<nickename>/', methods=['GET'])
def timeline_user(nickename):
  try:
    user = db.session.query(User).filter(User.nickename == nickename).one()
    tweets = db.session.query(Tweet).filter(Tweet.user_id == user.id).all()
    gaz = []
    for tweet in tweets:
      gaz.append({'user': user.nickename, 'text': tweet.content})
    return render_template("timeline.html", gaz=gaz)
  except NoResultFound:
    return 'pas de post avec le user :' + nickename
  return nickename


@app.route('/gaz', methods=['GET', 'POST'])
def save_gazouille():
  if request.method == 'POST':
    if len(request.form.get("user-text")) <= 280:
      print(request.form)
      dump_to_csv(request.form)
      return redirect(url_for('timeline'))
  if request.method == 'GET':
    return render_template('formulaire.html')


@app.route('/timeline/', methods=['GET'])
def timeline():
  tweets = Tweet.query.all()
  gaz = []
  for tweet in tweets:
    user = db.session.query(User).filter(User.id == tweet.user_id).one()
    gaz.append({'user': user.nickename, 'text': tweet.content})

  return render_template("timeline.html", gaz=gaz)


def parse_from_csv():
  gaz = []
  with open('./gazouilles.csv', 'r') as f:
    reader = csv.reader(f)
    for row in reader:
      gaz.append({"user": row[0], "text": row[1]})
  return gaz


def dump_to_csv(d):
  donnees = [d["user-name"], d["user-text"]]
  try:
    user = db.session.query(User).filter(
        User.nickename == d["user-name"]).one()
    db.session.add(Tweet(d["user-text"], user.id))
    db.session.commit()
  except NoResultFound:
    # create user noit exist
    db.session.add(User(d["user-name"]))
    db.session.commit()

    # save user's tweet
    user = db.session.query(User).filter(
        User.nickename == d["user-name"]).one()
    db.session.add(Tweet(d["user-text"], user.id))
    db.session.commit()
