from flask import Flask, request, render_template, redirect, url_for
import csv

app = Flask(__name__)


@app.route('/')
def home():
    return 'Bienvenue !'


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

