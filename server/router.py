import flask, dotenv

from database import SQLite3Database
from session_manager import SessionManager

app = flask.Flask(__name__)

# Load the secret key from the .env file and set it for the Flask app
env = dotenv.dotenv_values('.env')
assert env['FLASK_SESSION_SECRET_KEY'], 'FLASK_SESSION_SECRET_KEY must be set in .env file'
app.secret_key = env['FLASK_SESSION_SECRET_KEY'].encode('utf-8')

sm = SessionManager(SQLite3Database())

# HOME
@app.route('/')
def home():
    if not sm.is_logged_in():
        return flask.redirect(flask.url_for('login'))
    user = sm.user()
    return '''
        <h1>Welcome, {}!</h1>
        <a href="/logout">Logout</a>
        <form method="post" action="/create">
        <button type="submit">Create room</button>
        </form>
        <form method="post" action="/join">
        <input type="text" name="room_code" placeholder="Room Code" required/>
        <button type="submit">Join room</button>
        </form>
    '''.format(user)

# LOGIN
@app.route('/login', methods=['GET', 'POST'])
def login():
    if sm.is_logged_in():
        return flask.redirect(flask.url_for('home'))
    if flask.request.method == 'POST':
        username = flask.request.form['username']
        password = flask.request.form['password']
        sm.login(username, password)
        return flask.redirect(flask.url_for('home'))
    return '''
        <form method="post" action="/login">
        <input type="text" name="username" placeholder="Username" required/>
        <input type="password" name="password" placeholder="Password" required/>
        <button type="submit">Login</button>
        </form>
    '''

# LOGOUT
@app.route('/logout')
def logout():
    sm.logout()
    return flask.redirect(flask.url_for('login'))