# import the Flask class from flask module
from flask import Flask, render_template, redirect, \
		url_for,request,session,flash

app = Flask(__name__)

#config
app.secret_key = 'E\x134\xa2rw,.L\x0f\x92s\x9b^\x99\x9a\x8a\r\xd2\x96\xb3\xe8_K'

@app.route('/')
def welcome():
  return render_template('welcome.html')

@app.route('/index')
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
			return redirect(url_for('home'))
	return render_template('login.html', error=error)

# start the server with the 'run()' method
if __name__ == '__main__':
	app.run(debug=True)