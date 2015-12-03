# import the Flask class from flask module
from flask import Flask, render_template, redirect, \
		url_for,request,session,flash
from functools import wraps

from flask.ext.socketio import SocketIO, emit

app = Flask(__name__)

#config
app.secret_key = 'E\x134\xa2rw,.L\x0f\x92s\x9b^\x99\x9a\x8a\r\xd2\x96\xb3\xe8_K'
socketio = SocketIO(app)

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
@socketio.on('connect')
def test_connect():
	session['test'] = True
 	emit('response', {'data': 'Connected'})

@socketio.on('message')
def handle_message(message):
	emit('response', {'data': 'Server Say :' + message['data']})

@app.route('/')
def welcome():
  return render_template('welcome.html')

@app.route('/index',methods=['GET','POST'])
@login_required
def home():
	return render_template('index.html')

# route for handling the login page logic
@app.route('/login', methods=['GET', 'POST'])
def login():
	error = None
	if request.method == 'POST':
		if (request.form['username'] != 'admin') \
				or request.form['password'] != 'admin':
			error = 'Invalid Credentials. Please try again.'
		else:
			session['logged_in'] = True
			return redirect(url_for('home'))
	return render_template('login.html', error=error)

@app.route('/logout')
@login_required
def logout():
	session.pop('logged_in',None)
	return redirect(url_for('welcome'))

# start the server with the 'run()' method
if __name__ == '__main__':
	socketio.run(app,debug=True)