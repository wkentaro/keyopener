#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# main.py
#
"""Main function of web application keyopener.ddo.jp."""


__author__ = 'www.kentaro.wada@gmail.com (Kentaro Wada)'


import datetime
import sqlite3
import httplib2
import logging
import os
import sys
import pickle

from flask import (
    Flask,
    abort,
    redirect,
    url_for,
    request,
    render_template,
    session
    )
import jinja2

from oauth2client.client import Credentials
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import AccessTokenRefreshError
from apiclient.discovery import build
from oauth2client.client import FlowExchangeError
from apiclient import errors


logging.basicConfig(stream=sys.stderr)
app = Flask(__name__, static_url_path='/static')

CLIENTSECRETS_LOCATION = os.path.join(
    os.path.dirname(__file__), 'client_secrets.json')
REDIRECT_URI = 'http://keyopener.ddo.jp/step2/'
SCOPES = ['email', 'profile']
DB_PATH = os.path.join(os.path.dirname(__file__), 'keyopener.sqlite3')


@app.route('/')
def index():
    if 'user_id' in session:
        # if signed in
        return redirect(url_for('account'))
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
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    sql = sql.format(user_id=user_id, credentials=credentials.to_json())
    c.execute(sql)
    conn.commit()
    conn.close()


def get_stored_credentials(user_id):
    # get data from database
    conn = sqlite3.connect(DB_PATH)
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
    try:
        user_info = get_user_info(credentials)
    except AccessTokenRefreshError:
        return redirect(url_for('signout'))
    user_id = user_info.get('id')
    email_address = user_info.get('email', '')
    name = user_info.get('name')
    # store
    store_credentials(user_id, credentials)
    session['user_id'] = user_id
    session['email_address'] = email_address
    session['name'] = name
    # display
    return redirect(url_for('account'))


@app.route('/account/', methods=['GET'])
def account():
    if 'user_id' not in session:
        # if not logged in
        return redirect(url_for('index'))

    user_id = session['user_id']
    credentials = get_stored_credentials(user_id)
    # get user info
    try:
        user_info = get_user_info(credentials)
    except AccessTokenRefreshError:
        return redirect(url_for('signout'))
    email_address = session['email_address']
    access_right = check_access_right(email_address)
    key_status = check_key_status()
    # return str(user_info)
    return render_template(
        'account.html',
        user_info=user_info,
        access_right=access_right,
        key_status=key_status)


def check_key_status():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    sql = "SELECT status FROM keystatus"
    c.execute(sql)
    data = c.fetchone()
    conn.close()
    return data[0]


def check_access_right(email_address):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    sql = ("""SELECT authorized FROM user WHERE """
           """email_address = '{email_address}'""")
    sql = sql.format(email_address=email_address)
    c.execute(sql)
    data = c.fetchone()
    conn.close()
    if data is None or data[0] == 0:
        return False
    else:
        return True


@app.route('/manage-access-right/')
def manage_access_right():
    if 'user_id' not in session:
        # if signed in
        return redirect(url_for('index'))
    email_address = session['email_address']
    # get authorized people
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    sql = 'SELECT email_address FROM user WHERE authorized = 1'
    # get user info
    c.execute(sql)
    authorized_people = c.fetchall()
    return render_template(
        'manage_access_right.html',
        authorized_people=authorized_people,
        email_address=email_address)


@app.route('/open-key/')
def open_key():
    if 'user_id' not in session:
        # if not logged in
        return redirect(url_for('index'))
    open_file = os.path.join(os.path.dirname(__file__), 'open.py')
    os.system('sudo python {0}'.format(open_file))
    # update db
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    sql = "UPDATE keystatus SET status = 'open'"
    c.execute(sql)
    conn.commit()
    conn.close()
    # save log
    name = session['name']
    action = 'open'
    store_access_log(name, action)
    return redirect(url_for('account'))


@app.route('/close-key/')
def close_key():
    if 'user_id' not in session:
        # if not logged in
        return redirect(url_for('index'))
    close_file = os.path.join(os.path.dirname(__file__), 'close.py')
    os.system('sudo python {0}'.format(close_file))
    # update db
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    sql = "UPDATE keystatus SET status = 'close'"
    c.execute(sql)
    conn.commit()
    conn.close()
    # save log
    name = session['name']
    action = 'close'
    store_access_log(name, action)
    return redirect(url_for('account'))


@app.route('/give-access-right/', methods=['POST'])
def give_access_right():
    email_address = request.form['email']
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    sql = ("""INSERT INTO user (email_address, authorized) """
           """VALUES ('{email_address}', 1)""")
    sql = sql.format(email_address=email_address)
    c.execute(sql)
    conn.commit()
    conn.close()
    return redirect(url_for('manage_access_right'))


def store_access_log(name, action):
    time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    sql = ("""INSERT INTO log (time, name, action) """
           """VALUES ('{time}', '{name}', '{action}')""")
    sql = sql.format(time=time, name=name.encode('utf-8'), action=action)
    c.execute(sql)
    conn.commit()
    conn.close()


@app.route('/remove-access-right/', methods=['POST'])
def remove_access_right():
    email_address = request.form['email']
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    sql = "DELETE FROM user WHERE email_address = '{email_address}'"
    sql = sql.format(email_address=email_address)
    c.execute(sql)
    conn.commit()
    conn.close()
    return redirect(url_for('manage_access_right'))


@app.route('/signout/')
def signout():
    # remove the username from the session if it's there
    session.pop('user_id', None)
    return redirect(url_for('index'))


@app.route('/log/')
def log():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    sql = 'SELECT * FROM log ORDER BY time DESC LIMIT 30'
    c.execute(sql)
    log = c.fetchall()
    conn.close()
    return render_template('log.html', log=log)


app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'
if __name__ == '__main__':
    app.run('0.0.0.0', port=80, debug=True)
