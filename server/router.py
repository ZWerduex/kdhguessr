import flask, dotenv

app = flask.Flask(__name__)

# Load the secret key from the .env file and set it for the Flask app
env = dotenv.dotenv_values('.env')
assert env['FLASK_SESSION_SECRET_KEY'], 'FLASK_SESSION_SECRET_KEY must be set in .env file'
app.secret_key = env['FLASK_SESSION_SECRET_KEY'].encode('utf-8')

# HOME PAGE
@app.route('/')
def home():
    if 'user' not in flask.session:
        return flask.redirect(flask.url_for('login'))
    return f'Hello, {flask.session["user"]}! Welcome to the home page. <a href="/logout">Logout</a>'

# LOGIN PAGE
@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'user' in flask.session:
        return flask.redirect(flask.url_for('home'))
    if flask.request.method == 'POST':
        username = flask.request.form['username']
        flask.session['user'] = username
        return flask.redirect(flask.url_for('home'))
    return '''
        <form method="post" action="/login">
        <input type="text" name="username" placeholder="Username" required/>
        <button type="submit">Login</button>
        </form>
    '''

# LOGOUT
@app.route('/logout')
def logout():
    if 'user' in flask.session:
        flask.session.pop('user')
    return flask.redirect(flask.url_for('login'))