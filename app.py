# import the Flask class from flask module
from flask import Flask, render_template, redirect, \
		url_for,request,session,flash
from functools import wraps
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.socketio import SocketIO, emit

app = Flask(__name__)

#config
app.secret_key = 'E\x134\xa2rw,.L\x0f\x92s\x9b^\x99\x9a\x8a\r\xd2\x96\xb3\xe8_K'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://localhost/trus_sensor'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
socketio = SocketIO(app)

db = SQLAlchemy(app)

from models import *

# login required decorator
def login_required(f):
	@wraps(f)
	def wrap(*args, **kwargs):
		error = None
		if 'logged_in' in session:
			return f(*args, **kwargs)
		else:
			error = 'You neeed to login first.'
			# flash('You need to login first.')
			# return redirect(url_for('login',error=error))
			return render_template('login.html', error=error)
	return wrap

# using socketio to receiving message
@socketio.on('connect', namespace='/sensor')
def connect():
 	emit('status', {'data': 'Connected'})

@socketio.on('message', namespace='/sensor')
def handle_message(message):
	emit('response', {'data': message['data']}, broadcast=True)

@app.route('/')
def welcome():

	posts = db.session.query(User).all()
	return render_template('welcome.html',posts=posts)

@app.route('/index',methods=['GET','POST'])
@login_required
def home():
	return render_template('index.html')

# route for handling the login page logic
@app.route('/login', methods=['GET', 'POST'])
def login():
	error = None
	if request.method == 'POST':
		user = User.query.filter_by(name=request.form['username']).first()
		if user is not None and user.password == request.form['password']:
			session['logged_in'] = True
			return redirect(url_for('home'))
		else:
			error = 'Invalid Credentials. Please try again.'
	return render_template('login.html', error=error)

@app.route('/logout')
@login_required
def logout():
	session.pop('logged_in',None)
	return redirect(url_for('welcome'))

# start the server with the 'run()' method
if __name__ == '__main__':
	socketio.run(app,debug=True)