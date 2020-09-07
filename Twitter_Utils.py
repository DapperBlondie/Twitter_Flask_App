import oauth2
import urllib.parse as urlparse
import CONSTANTS
import json
from User_DB import User

consumer = oauth2.Consumer(CONSTANTS.Consumer_key, CONSTANTS.Consumer_Secret)

def userInfo():

    user_firstname = input('What is your firstname ? \n')
    user_lastname = input('What is your lastname ? \n')
    user_email = input('Please enter your email : \n')
    user = User.loading_from_DB(email=user_email)
    return user, user_firstname, user_lastname, user_email

def requestTokenClient():

    client = oauth2.Client(consumer)
    response, content = client.request(CONSTANTS.Request_Token_url, 'POST')
    return response, content

def requestTokenCallback(response, content):

    if response.status != 200:
        print("there is some thing wrong :(( ")
        print(response.status)

    else:
        request_token_callback = dict(urlparse.parse_qsl(content.decode('utf-8')))

        print("Please Go th the following website : ")
        print("{}?oauth_token={}".format(CONSTANTS.Authorization_url, request_token_callback['oauth_token']))

        oauth_verifier = int(input("what is the pin-code ? \n"))
        token = oauth2.Token(request_token_callback['oauth_token'], request_token_callback['oauth_token_secret'])
        token.set_verifier(oauth_verifier)
        return token

def get_oauth_verifier_url(request_token_callback):

    """response, content = requestTokenClient()
    request_token_callback = dict(urlparse.parse_qsl(content.decode('utf-8')))"""

    return "{}?oauth_token={}".format(CONSTANTS.Authorization_url, request_token_callback['oauth_token'])

def make_accesstoken(oauth_verifier, request_token_callback):

    token = oauth2.Token(request_token_callback['oauth_token'], request_token_callback['oauth_token_secret'])
    token.set_verifier(oauth_verifier)
    client = oauth2.Client(consumer, token)
    reponse, content = client.request(CONSTANTS.Access_Token_url, 'POST')
    return dict(urlparse.parse_qsl(content.decode('utf-8')))

def accessToken(token):

    client = oauth2.Client(consumer, token)
    response, content = client.request(CONSTANTS.Access_Token_url, 'POST')

    if response.status != 200:
        print("There is something wrong during receiving Access Token :(( ")
        print(response)
    else:
        access_token_callback = dict(urlparse.parse_qsl(content.decode('utf-8')))
        return access_token_callback

def saving_New_to_DB(access_token_callback, firstname, lastname, email):

    user = User(None, firstname, lastname, email, access_token_callback['oauth_token'],
                access_token_callback['oauth_token_secret'])
    user.saving_to_DB()
    return user

def getAuthorizationToken(user, user_email):

    user.loading_from_DB(user_email)
    authorized_token = oauth2.Token(user.oauth_token, user.oauth_token_secret)
    authorized_client = oauth2.Client(consumer, authorized_token)
    return authorized_client

def searchAPI_2(authorized_client, features):

    user_title = features[0]
    user_number = features[1]

    while user_number > 100:
        user_number = user_number - 1

    response, content = authorized_client.request(
        "https://api.twitter.com/1.1/search/tweets.json?q={}&result_type=popular&count={}".format(user_title,
                                                                                                  user_number),
        'GET')
    tweets = json.loads(content.decode('utf-8'))
    if response.status != 200:
        print("There is something went wrong during searching :(( ")
    else:
        return tweets


def searchAPI(authorized_client):

    while True:

        user_title = input('What do you want to search about it ? \n')
        user_number = int(input('How many tweets do you want to see ? (MAX : 100) \n'))

        while user_number > 100:
            user_number = user_number - 1

        response, content = authorized_client.request(
            "https://api.twitter.com/1.1/search/tweets.json?q={}&result_type=popular&count={}".format(user_title,
                                                                                                      user_number),
            'GET')
        tweets = json.loads(content.decode('utf-8'))

        if response.status != 200:
            print('Something went wrong, Please try again')

        else:

            print('this the text & images : \n')
            for tweet in tweets['statuses']:
                print(tweet['text'])
                print('\n')

        ans = input("Do you want to exit ? (yes/no)\n")
        if ans == "yes":
            print("Thankyou for using our App.")
            break
        elif ans == "no":
            continue