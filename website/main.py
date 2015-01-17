#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# main.py
#
import sqlite3
import httplib2
import logging
import os
import pickle
import sqlite3

from flask import Flask, abort, redirect, url_for, request, render_template, session
import jinja2

from oauth2client.client import Credentials
from oauth2client.client import flow_from_clientsecrets
from apiclient.discovery import build
from oauth2client.client import FlowExchangeError
from apiclient import errors

app = Flask(__name__, static_url_path='/static')

CLIENTSECRETS_LOCATION = os.path.join(os.path.dirname(__file__),
        'client_secrets.json')
REDIRECT_URI = 'http://localhost:5000/step2/'
SCOPES = ['email', 'profile']

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/step1/')
def google_signin_step1():
    flow = flow_from_clientsecrets(CLIENTSECRETS_LOCATION, ' '.join(SCOPES))
    flow.redirect_uri = REDIRECT_URI
    auth_uri = flow.step1_get_authorize_url() 
    return redirect(auth_uri)

def store_credentials(user_id, credentials):
    # check if user_id already exists
    credentials_exist = get_stored_credentials(user_id)
    if credentials_exist is not None:
        sql = ("""UPDATE credentials SET credentials = '{credentials}' """
               """WHERE user_id = '{user_id}'""")
    else:
        sql = ("""INSERT INTO credentials (user_id, credentials) """
               """VALUES ('{user_id}', '{credentials}')""")
    # store credentials
    conn = sqlite3.connect('keyopener.sqlite3')
    c = conn.cursor()
    sql = sql.format(user_id=user_id, credentials=credentials.to_json())
    c.execute(sql)
    conn.commit()
    conn.close()

def get_stored_credentials(user_id):
    # get data from database
    conn = sqlite3.connect('keyopener.sqlite3')
    c = conn.cursor()
    sql = ("""SELECT credentials FROM credentials WHERE """
           """user_id = '{user_id}'""")
    sql = sql.format(user_id=user_id)
    c.execute(sql)
    data = c.fetchone()
    conn.close()
    # check if user_id already exists
    if data is None:
        return None
    else:
        credentials_json = data[0]
    # get credential
    credentials = Credentials.new_from_json(credentials_json)
    return credentials

class NoUserIdException(Exception):
    """ No user id """

def get_user_info(credentials):
    user_info_service = build(
        serviceName='oauth2', version='v2',
        http=credentials.authorize(httplib2.Http()))
    user_info = None
    try:
        user_info = user_info_service.userinfo().get().execute()
    except errors.HttpError, e:
        logging.error('An error occurred: %s', e)
    if user_info and user_info.get('id'):
        return user_info
    else:
        raise NoUserIdException()

@app.route('/step2/', methods=['GET', 'POST'])
def google_signin_step2():
    # authorize the service
    flow = flow_from_clientsecrets(CLIENTSECRETS_LOCATION, ' '.join(SCOPES))
    flow.redirect_uri = REDIRECT_URI
    authorization_code = request.args.get('code', '')
    credentials = flow.step2_exchange(authorization_code)
    # get user info
    user_info = get_user_info(credentials)
    # email_address = user_info.get('email', '')
    user_id = user_info.get('id')
    # store
    store_credentials(user_id, credentials)
    session['user_id'] = user_id
    # display
    return redirect(url_for('account'))

@app.route('/account/', methods=['GET'])
def account():
    if 'user_id' not in session:
        # if not logged in 
        return redirect(url_for('/'))

    user_id = session['user_id']
    credentials = get_stored_credentials(user_id)
    # get user info
    user_info = get_user_info(credentials)
#     email_address = user_info.get('email', '')
    user_id = user_info.get('id')
    access_right = check_access_right(user_id)
    key_status = check_key_status()
    # return str(user_info)
    return render_template(
            'account.html',
            user_info=user_info,
            access_right=access_right,
            key_status=key_status)

def check_key_status():
    conn = sqlite3.connect('keyopener.sqlite3')
    c = conn.cursor()
    sql = "SELECT status FROM keystatus"
    c.execute(sql)
    data = c.fetchone()
    conn.close()
    return data[0]

def check_access_right(user_id):
    conn = sqlite3.connect('keyopener.sqlite3')
    c = conn.cursor()
    sql = ("""SELECT authorized FROM user WHERE """
           """user_id = '{user_id}'""")
    sql = sql.format(user_id=user_id)
    c.execute(sql)
    data = c.fetchone()
    conn.close()
    if data is None or data[0] == 0:
        return False
    else:
        return True

def give_access_right(user_id):
    conn = sqlite3.connect('keyopener.sqlite3')
    c = conn.cursor()
    sql = ("""INSERT INTO user (user_id, authorized) """
           """VALUES ('{user_id}', 1)""")
    sql = sql.format(user_id=user_id)
    c.execute(sql)
    conn.close()

def remove_access_right(user_id):
    conn = sqlite3.connect('keyopener.sqlite3')
    c = conn.cursor()
    sql = ("""UPDATE user SET authorized = 0 """
           """WHERE user_id = '{user_id}'""")
    sql = sql.format(user_id=user_id)
    c.execute(sql)
    conn.close()

@app.route('/signout')
def signout():
    # remove the username from the session if it's there
    session.pop('user_id', None)
    return redirect(url_for('index'))

app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'
if __name__ == '__main__':
    app.run('0.0.0.0', debug=True)