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

def uniqid():
    from time import time
    return hex(int(time()*10))[2:]

def getLoginTemplateStatus(self, users):
    if users.get_current_user():
        url = users.create_logout_url(self.request.uri)
        url_linktext = 'Logout'
        isLogin = 'True'
    else:
        url = users.create_login_url(self.request.uri)
        url_linktext = 'Login'
        isLogin = 'False'
    template_values = {
        'isLogin': isLogin,
        'url': url,
        'url_linktext': url_linktext,
    }
    return template_values

class Collection(ndb.Model):
    qid = ndb.StringProperty(indexed=True)
    content = ndb.StringProperty(indexed=False)
    user = ndb.UserProperty()
    date_created = ndb.DateTimeProperty(auto_now_add=True)
    date_updated = ndb.DateTimeProperty(auto_now=True)
    tags = ndb.StringProperty(repeated=True)
    vote_up = ndb.IntegerProperty()
    vote_down = ndb.IntegerProperty()
    vote = ndb.ComputedProperty(lambda self: self.vote_up - self.vote_down)
    answers = ndb.JsonProperty(repeated=True)       # stores a list of answer json


# [START main_page]
class MainPage(webapp2.RequestHandler):
    def get(self):
        template_values = getLoginTemplateStatus(self, users)
        template = JINJA_ENVIRONMENT.get_template('layout.html')
        self.response.write(template.render(template_values))
    
# [END main_page]

# [START askquestion_page]
class AskQuestion(webapp2.RequestHandler):
    def get(self):
        template_values = getLoginTemplateStatus(self, users)
        template = JINJA_ENVIRONMENT.get_template('ask.html',parent='layout.html')
        self.response.write(template.render(template_values))
    def post(self):
        template_values = getLoginTemplateStatus(self, users)
        template_values["jane"] = "post method submitted"
        template = JINJA_ENVIRONMENT.get_template('ask.html',parent='layout.html')
        self.response.write(template.render(template_values))
        # create a new question collection and store them into database

# [END askquestion_page]

# [START question_list]
class QuestionList(webapp2.RequestHandler):
    def get(self):
        template_values = getLoginTemplateStatus(self, users)
        template = JINJA_ENVIRONMENT.get_template('layout.html')
        self.response.write(template.render(template_values))

# [END question_list]


application = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/index', MainPage),
    ('/ask', AskQuestion),
    ('/list', QuestionList),
], debug=True)