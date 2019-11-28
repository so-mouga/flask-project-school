from flask import Flask, request, render_template, redirect, url_for
import csv

from flask_sqlalchemy import SQLAlchemy


# db variable initialization
app = Flask(__name__, instance_relative_config=True)
app.config["DEBUG"] = True

app.config.from_pyfile('config.py')
db = SQLAlchemy(app)


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(4096))
    password = db.Column(db.String(4096))

class tweet(db.Model):
    __tablename__ = 'tweet'
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(4096))

SQLALCHEMY_DATABASE_URI = "mysql+mysqlconnector://{username}:{password}@{hostname}/{databasename}".format(
    username="mouga",
    password="ipssi2019",
    hostname="mouga.mysql.pythonanywhere-services.com",
    databasename="mouga$twitter",
)
app.config["SQLALCHEMY_DATABASE_URI"] = SQLALCHEMY_DATABASE_URI
app.config["SQLALCHEMY_POOL_RECYCLE"] = 299
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.drop_all()
db.create_all()


@app.route('/')
def home():
    return 'Bienvenue!'


@app.route('/gaz', methods=['GET', 'POST'])
def save_gazouille():
    if request.method == 'POST':
        print(request.form)
        dump_to_csv(request.form)
        return redirect(url_for('timeline'))
        # return "OK"
    if request.method == 'GET':
        return render_template('formulaire.html')


@app.route('/timeline', methods=['GET'])
def timeline():
    gaz = parse_from_csv()
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
    with open('./gazouilles.csv', 'a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(donnees)
