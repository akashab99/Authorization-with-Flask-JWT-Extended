# System Imports
from flask import Flask, jsonify, make_response, request, render_template, session , redirect
import jwt
from datetime import datetime, timedelta
from functools import wraps

# Flask application object
app = Flask(__name__)

# SECRET KEY
app.config['SECRET_KEY'] = '0idVtXuqyZkhqp8YTw3'


# TOKEN_VALIDATION
def token_required(func):
    @wraps(func)
    def decorated(*args, **kwargs):
        token = request.args.get('token')
        if not token:
            return jsonify({'Alert!': 'Token is missing!'}), 401
        return func(*args, **kwargs)
    return decorated


# Session Validation
@app.route('/')
def home():
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        return 'logged in currently'


# Login Validation
@app.route('/login', methods=['POST'])
def login():
    if request.form['username'] and request.form['password'] == '123456':
        session['logged_in'] = True

        token = jwt.encode({
            'user': request.form['username'],
            'password':  request.form['password'],
            'expiration': str(datetime.now() + timedelta(seconds=60))
        },
            app.config['SECRET_KEY'])
        return jsonify({'token': token})
    else:
        return make_response('Unable to verify', 403, {'WWW-Authenticate': 'Basic realm: "Authentication Failed "'})

# Authentication with Token
@app.route('/auth')
@token_required
def auth():
    return 'JWT is verified. Welcome to your dashboard !'

@app.route('/open')
def openroute():
    return 'This is a Public or Open'


@app.route('/logout', methods=['POST'])
def logout():
    session.clear()
    session['logged_in'] = False
    return redirect("/login")


if __name__ == "__main__":
    app.run(debug=True)
