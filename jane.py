# This is equivalent to main.py
# [START imports]
import os
import urllib

from google.appengine.api import users
from google.appengine.ext import ndb

from models import *        # custom models

import jinja2
import webapp2
import time


JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(os.path.abspath(__file__)) + '/view/'),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)
# [END imports]

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

# [START main_page]
class MainPage(webapp2.RequestHandler):
    def get(self):
        questions_query = Question.query().order(-Question.date_edit)
        questions = questions_query.fetch(2)

        template_values = getLoginTemplateStatus(self, users)
        template_values["questions"] = questions

        template = JINJA_ENVIRONMENT.get_template('layout.html')
        self.response.write(template.render(template_values))
    
# [END main_page]

# [START askquestion_page]
class AskQuestion(webapp2.RequestHandler):
    def get(self):
        template_values = getLoginTemplateStatus(self, users)
        template = JINJA_ENVIRONMENT.get_template('ask.html',parent='layout.html')
        self.response.write(template.render(template_values))
    def post(self): # create a new question collection and store them into database
        question = Question()
        if users.get_current_user():
            question.author = users.get_current_user()

        question.content = self.request.get('content')
        question.title = self.request.get('title')

        question.put()
        time.sleep(0.1)
        self.redirect('/list')

# [END askquestion_page]

# [START question_list]
class QuestionList(webapp2.RequestHandler):
    def get(self):
        questions_query = Question.query().order(-Question.date_edit)
        questions = questions_query.fetch()

        print "!!!!!!length of questions is %s" % (questions[0].author)
        template_values = getLoginTemplateStatus(self, users)

        template_values["questions"] = questions
        template = JINJA_ENVIRONMENT.get_template('list.html', parent='layout.html')
        self.response.write(template.render(template_values))

# [END question_list]


application = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/index', MainPage),
    ('/ask', AskQuestion),
    ('/list', QuestionList),
], debug=True)