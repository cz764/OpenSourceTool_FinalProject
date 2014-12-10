# [START imports]
import os
import urllib
from jane import getLoginTemplateStatus		# custom python script

from google.appengine.api import users
from google.appengine.ext import ndb

import jinja2
import webapp2


JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(os.path.abspath(__file__)) + '/view/'),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)
# [END imports]

# [START main_page]
class MainPage(webapp2.RequestHandler):
    def get(self):
        template_values = getLoginTemplateStatus(self, users)
        template = JINJA_ENVIRONMENT.get_template('manage.html', parent='layout.html')
        self.response.write(template.render(template_values))
    
# [END main_page]


application = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/manage', MainPage),
    
], debug=True)