# POC Application
from flask import Flask, render_template, request, session, redirect, url_for
from time import *
import os, hashlib, database

app = Flask(__name__)
app.config.from_object(__name__)
port = int(os.getenv("PORT", 5000))

app.secret_key = "OCML3BRawWEUeaxcuKHLpw"
app.config['SESSION_TYPE'] = 'filesystem'

hist = database.load(database.CHATHISTORY)
users = database.load(database.USERS)


# Homepage
@app.route("/")
def index():
	return render_template('home.html', chathistory=hist, user=session.get("USERNAME"))


# Login Page
@app.route("/login", methods=["GET", "POST"])
def login():
	if request.method == "POST":
		req = request.form
		username = req.get("username")
		password = req.get("password")

		if not username in users:
			print("Username not found")
			return redirect(request.url)
		else:
			user = users[username]

		if not hashlib.sha224(password).hexdigest() == user["password"]:
			print("Incorrect password")
			return redirect(request.url)
		else:
			session["USERNAME"] = user["username"]
			print("session username set")
			return redirect(url_for("index"))

	return render_template("login.html")


# If no username exists, redirect user to login page
@app.before_request
def loggedincheck():
	print(session.get("USERNAME"))
	if session.get("USERNAME") is None and request.endpoint != 'login' and request.endpoint != 'signup':
		print("No username found in session")
		return render_template("login.html")


# Makes a new post
@app.route("/newspost/", methods=['GET', 'POST'])
def newspost():
	body = request.form['comment']
	uname = session.get("USERNAME")
	tstamp = now()
	unique_key = uname + ":::" + tstamp
	hist[unique_key] = {'user': uname, 'name': users[uname]['name'], 'body': body, 'timestamp': tstamp}
	database.save(hist, database.CHATHISTORY)
	return redirect(url_for('index'))


# Log the user out of the site
@app.route("/logout")
def logout():
	session.pop("USERNAME", None)
	return redirect(url_for("login"))


# Create a new user
@app.route("/signup", methods=['GET', 'POST'])
def signup():
	username = request.form['username']
	password = request.form['password']
	name = request.form['name']
	email = request.form['email']
	bio = request.form['bio']
	for key in users.keys():
		if username == key:
			print("username exists")
			return render_template("login.html", user_exists=True)

	users[username] = {'username': username, 'password': str(hashlib.sha224(password).hexdigest()),
						 'name': name, 'email': email, 'bio': bio}
	database.save(users, database.USERS)
	session["USERNAME"] = username
	return redirect(url_for("index"))



# Timestamping
def now():
	return str(strftime("%Y-%m-%d %H:%M:%S", gmtime()))


# Begin the application
if __name__ == '__main__':
	database.save(users, database.USERS)
	app.config["SECRET_KEY"] = "OCML3BRawWEUeaxcuKHLpw"
	app.run(host='0.0.0.0', port=port)