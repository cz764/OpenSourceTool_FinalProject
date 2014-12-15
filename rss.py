# [START imports]
import os
import urllib

from google.appengine.api import users
from google.appengine.ext import ndb

from models import *        # custom models
from viewQuestion import *

import jinja2
import webapp2
import time


JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(os.path.abspath(__file__)) + '/view/'),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)
# [END imports]

class RssFeed(webapp2.RequestHandler):
	def get(self):		
		template_values = {}
		qid = self.request.get('qid')
		template_values = getQandAs(qid, template_values)

		self.response.headers['Content-Type'] = 'text/xml'
		template = JINJA_ENVIRONMENT.get_template('rss.xml')
		self.response.write(template.render(template_values))

application = webapp2.WSGIApplication([
    ('/rss?.*', RssFeed),
], debug=True)