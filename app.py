# import the Flask class from flask module
from flask import Flask, render_template, redirect, \
		url_for,request,session,flash
from functools import wraps
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.socketio import SocketIO, emit

app = Flask(__name__)

# config
import os
app.config.from_object(os.environ['APP_SETTINGS'])

# socketio
socketio = SocketIO(app)

db = SQLAlchemy(app)

from models import *

# login required decorator
def login_required(f):
	@wraps(f)
	def wrap(*args, **kwargs):
		if 'logged_in' in session:
			return f(*args, **kwargs)
		else:
			# flash('You need to login first.')
			return redirect(url_for('login'))
			# return render_template('login.html', error=error)
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
	return render_template('login.html')

@app.route('/demo')
@login_required
def demo():
	return render_template('demo.html')

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
			return redirect(url_for('demo'))
		else:
			error = 'Invalid Credentials. Please try again.'
	return render_template('login.html', error=error)

@app.route('/logout')
@login_required
def logout():
	session.pop('logged_in',None)
	return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
	error = None
	if request.method == 'POST':
		user = User.query.filter_by(name=request.form['username']).first()
		if user is None:			
			new_user = User(
					name = request.form['username'],
					email = request.form['email'],
					password = request.form['password']
			)
			db.session.add(new_user)
			db.session.commit()
			flash('Register success please try to login.')
			return redirect(url_for('login'))
		else:
			error = 'Username is invalid. Please try agin'
	return render_template('register.html', error=error)

# start the server with the 'run()' method
if __name__ == '__main__':
	socketio.run(app)