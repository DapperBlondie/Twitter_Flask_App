from flask import Flask, render_template, session, redirect, request, url_for, g
import Twitter_Utils as twitterutils
import urllib.parse as urlparse
from User_DB import User

app = Flask(__name__)
app.secret_key = "alireza1380##"

@app.before_request
def load_user_from_db():

    if 'screen_name' in session:
        g.user = User.loading_from_DB(session['screen_name'])
@app.route('/logout')
def logout():
    session.clear
    return redirect(url_for('homepage'))

@app.route('/')
def homepage():
    return render_template('home.html')

@app.route('/login/twitter')
def twitter_login():

    response, content = twitterutils.requestTokenClient()
    request_token = dict(urlparse.parse_qsl(content.decode('utf-8')))
    session['request_token'] = request_token

    return redirect(twitterutils.get_oauth_verifier_url(request_token))

@app.route('/auth/twitter')
def twitter_auth():

    oauth_verifier = request.args.get("oauth_verifier")
    access_token = twitterutils.make_accesstoken(oauth_verifier, session['request_token'])
    user = User.loading_from_DB(access_token['screen_name'])

    if not user:
        user = User(None, "", "", access_token['screen_name'], access_token['oauth_token'], access_token['oauth_token_secret'])
        user.saving_to_DB()
    session['screen_name'] = user.email
    return redirect(url_for('profile'))

    """ return redirect("http://127.0.0.1:8000/profile")"""

@app.route('/profile')
def profile():

    return render_template('profile.html', user=g.user.email)

@app.route('/search')
def search():
    features=["nasa", 100]
    #features.append(request.args.get('title'))
    #features.append(request.args.get('number'))
    authorized_client = twitterutils.getAuthorizationToken(g.user, g.user.email)
    tweets = twitterutils.searchAPI_2(authorized_client, features)
    tweettext = [tweet['text'] for tweet in tweets['statuses']]
    return render_template('search.html', content=tweettext)

app.run(port=8000)