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

from flask import Flask, abort, redirect, url_for, request, render_template
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
        return
    # store credentials
    conn = sqlite3.connect('keyopener.sqlite3')
    c = conn.cursor()
    sql = ("""INSERT INTO credentials (user_id, credentials) """
           """VALUES ('{user_id}', '{credentials}')""")
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
    email_address = user_info.get('email', '')
    user_id = user_info.get('id')
    # store
    store_credentials(user_id, credentials)
    # display
    text = str(user_info)
    return text + '<a href="/session-test/?user_id={0}">test</a>'.format(user_id)

@app.route('/session-test/', methods=['GET'])
def session_test():
    user_id = request.args.get('user_id', '')
    credentials = get_stored_credentials(user_id)
    # get user info
    user_info = get_user_info(credentials)
    email_address = user_info.get('email', '')
    user_id = user_info.get('id')
    # display
    text = str(user_info)
    return text


if __name__ == '__main__':
    app.run(debug=True)