# [START imports]
import os
import urllib

from google.appengine.api import users
from google.appengine.ext import ndb

import jinja2
import webapp2


JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)
# [END imports]

# [START main_page]
class MainPage(webapp2.RequestHandler):
    def get(self):
        greetings = "rendered by Jane with bootstrap"
        if users.get_current_user():
            url = users.create_logout_url(self.request.uri)
            url_linktext = 'Logout'
        else:
            url = users.create_login_url(self.request.uri)
            url_linktext = 'Login'
        template_values = {
            'jane': greetings,
            'url': url,
            'url_linktext': url_linktext,
        }
        template = JINJA_ENVIRONMENT.get_template('layout.html')
        self.response.write(template.render(template_values))
    
# [END main_page]

# [START askquestion_page]
class AskQuestion(webapp2.RequestHandler):
    def get(self):
        greetings = "rendered by Jane without BootStrap"
        if users.get_current_user():
            url = users.create_logout_url(self.request.uri)
            url_linktext = 'Logout'
        else:
            url = users.create_login_url(self.request.uri)
            url_linktext = 'Login'

        template_values = {
            'jane': greetings,
            'url': url,
            'url_linktext': url_linktext,
        }

        template = JINJA_ENVIRONMENT.get_template('ask.html',parent='layout.html')
        self.response.write(template.render(template_values))    
# [END askquestion_page]

# [START question_list]
class QuestionList(webapp2.RequestHandler):
    def get(self):
        greetings = "rendered by Jane with bootstrap"
        if users.get_current_user():
            url = users.create_logout_url(self.request.uri)
            url_linktext = 'Logout'
        else:
            url = users.create_login_url(self.request.uri)
            url_linktext = 'Login'
        template_values = {
            'jane': greetings,
            'url': url,
            'url_linktext': url_linktext,
        }
        template = JINJA_ENVIRONMENT.get_template('layout.html')
        self.response.write(template.render(template_values))
    
# [END question_list]


application = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/index', MainPage),
    ('/ask', AskQuestion),
    ('/list', QuestionList),
], debug=True)