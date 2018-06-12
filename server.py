import re, bcrypt
from flask import Flask, session, request, redirect, render_template, flash, url_for
from db.data_layer import get_user_by_email, get_user_by_id, create_user, get_request, search_tvshow, like_tvshow
from flask_wtf.csrf import CSRFProtect

app = Flask(__name__)
app.secret_key = '8118d0875ad5b6b3ad830b956b111fb0'
csrf = CSRFProtect(app)

EMAIL_REGEX = re.compile(r'^([a-zA-Z0-9_\-\.]+)@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.)|(([a-zA-Z0-9\-]+\.)+))([a-zA-Z]{2,4}|[0-9]{1,3})(\]?)$')

@app.route('/')
def index():
    if 'user_id' in session:
        # get tvshows search result
        # get list of tvshow that liked by user
        liked_tvshow = 
        # do iteration for tvshows
        # if tvshow.api_id is on tv
        
        user = get_user_by_id(session['user_id'])
        return render_template('index.html', user=user)
    else:
        return render_template('index.html')

@app.route('/search', methods=['POST'])
def postsearch():
    keyword = request.form['html_keyword']
    return redirect(url_for('search', keyword=keyword))

@app.route('/search/<keyword>', methods=['GET'])
def search(keyword):
    tv_shows = search_tvshow(keyword)
    return render_template('index.html', tv_shows = tv_shows)


@app.route('/like/<user_id>/<tvshow_api_id>')
def like(user_id, tvshow_api_id):
    like_tvshow(user_id, tvshow_api_id)
    return redirect(url_for('index'))

def is_blank(name, field):
    if len(field) == 0:
        flash('{} cannot be blank'.format(name))
        return True
    return False

@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        fullname = request.form['html_fullname']
        email = request.form['html_email']
        password = request.form['html_password']
        confirm = request.form['html_confirm']

        is_valid = True

        is_valid = not is_blank('Fullname', fullname)
        is_valid = not is_blank('Email', email)
        is_valid = not is_blank('Password', password)
        is_valid = not is_blank('Confirm Password', confirm)

        if password != confirm:
            flash('Password do not match')
            is_valid = False
        if len(password) < 6:
            flash('Password have to be more than 6')
            is_valid = False
        if not EMAIL_REGEX.match(email):
            flash('Email format is wrong')
            is_valid = False

        if is_valid:
            try:
                encoded = password.encode('UTF-8')
                encrypted_password = bcrypt.hashpw(encoded, bcrypt.gensalt())
                user = create_user(email, fullname, encrypted_password)
                setup_web_session(user)
                return redirect(url_for('index'))
            except:
                raise
                flash('Email alredy registered')
        return redirect(url_for('register'))
    else:
        return render_template('register.html')

@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        email = request.form['html_email']
        password = request.form['html_password']

        try:
            user = get_user_by_email(email)
            encoded = password.encode('UTF-8')
            if bcrypt.checkpw(encoded, user.password):
                setup_web_session(user)
                return redirect(url_for('index'))
            else:
                flash('User not found')
        except:
            flash('Login failed')
        return redirect(url_for('login'))
    else:
        return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

def setup_web_session(user):
    session['user_id'] = user.id
    session['user_name'] = user.email
    session['name'] = user.name

app.jinja_env.auto_reload = True
app.config['TEMPLATE_AUTO_RELOAD'] = True
app.run(debug=True, use_reloader=True)
