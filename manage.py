# [START imports]
import os
import urllib
from jane import *		# custom python script
from models import *

from google.appengine.api import users
from google.appengine.ext import ndb

import jinja2
import webapp2


JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(os.path.abspath(__file__)) + '/view/'),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)
# [END imports]

def writingToTemplate(self, template_values):
	template = JINJA_ENVIRONMENT.get_template('list.html', parent='layout.html')
	self.response.write(template.render(template_values))

# [START manage_page]
class ManagePage(webapp2.RequestHandler):
	def get(self):
		if users.get_current_user():
			template_values = getQuestionList(self, True)
			writingToTemplate(self, template_values)
		else:
			template_values = getLoginTemplateStatus(self, users)
			writingToTemplate(self, template_values)
    
# [END manage_page]


application = webapp2.WSGIApplication([
    ('/manage', ManagePage),
    
], debug=True)