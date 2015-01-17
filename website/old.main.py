#!/usr/bin/env python
#
import httplib2
import logging
import os
import pickle

import webapp2
import jinja2

from oauth2client.client import flow_from_clientsecrets
from apiclient.discovery import build


__author__ = 'www.kentaro.wada@gmail.com (Kentaro Wada)'


JINJA_ENVIRONMENT = jinja2.Environment(
        loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
        extensions=['jinja2.ext.autoescape'],
        autoescape=True)

CLIENT_SECRETS = os.path.join(os.path.dirname(__file__), 'client_secrets.json')
flow = flow_from_clientsecrets(CLIENT_SECRETS,
        scope='https://www.googleapis.com/auth/plus.me',
        redirect_uri='http://localhost:8080/granted/')


class Base(webapp2.RequestHandler):
    def render(self, html, values={}):
        template = JINJA_ENVIRONMENT.get_template(html)
        self.response.write(template.render(values))


class Index(Base):
    def get(self):
        self.render(html='index.html')


class Grant(Base):
    def get(self):
        auth_uri = flow.step1_get_authorize_url()
        self.redirect(auth_uri)


class LoginLanding(Base):
    def get(self):
        # authorize the service
        credentials = flow.step2_exchange(self.request.get('code'))
        http = httplib2.Http()
        http = credentials.authorize(http)
        service = build('plus', 'v1', http=http)
        # get api values
        user = service.people().get(userId='me').execute(http=http)
        text = 'Welcome, {0}!\n{1}'.format(user['displayName'],
                credentials.to_json())
        self.response.write(text)

class SessionTest(Base):
    def get(self):
        http = httplib2.Http()
        http = credentials.authorize(http)
        service = build('plus', 'v1', http=http)
        # get api values
        user = service.people().get(userId='me').execute(http=http)
        text = 'Hello, {0}!'.format(user['displayName'])
        self.response.write(text)


app = webapp2.WSGIApplication([
    ('/', Index),
    ('/grant/', Grant),
    ('/granted/', LoginLanding),
    ('/session-test/', SessionTest),
    ], debug=True)