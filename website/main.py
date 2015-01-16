#!/usr/bin/env python
#
import os

import webapp2
import jinja2


view_path = os.path.dirname(__file__)
JINJA_ENVIRONMENT = jinja2.Environment(
        loader=jinja2.FileSystemLoader(view_path),
        extensions=['jinja2.ext.autoescape'],
        autoescape=True)


class Base(webapp2.RequestHandler):
    def render(self, html, values={}):
        template = JINJA_ENVIRONMENT.get_template(html)
        self.response.write(template.render(values))


class Index(Base):
    def get(self):
        # output = 'webapp2 running on apache2'
        # self.response.headers = [
        #         ('Content-type', 'text/plain'),
        #         ('Content-length', str(len(output)))]
        # self.response.out.write(output)
        self.render(html='index.html')


application = webapp2.WSGIApplication(
        [('/', Index)],
        debug=True)