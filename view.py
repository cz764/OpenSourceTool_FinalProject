# [START imports]
import os
import urllib

from google.appengine.api import users
from google.appengine.ext import ndb

from models import *        # custom models
from jane import getLoginTemplateStatus

import jinja2
import webapp2
import time


JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(os.path.abspath(__file__)) + '/view/'),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)
# [END imports]


# [START view_question]
class ViewQuestion(webapp2.RequestHandler):
    def get(self):
    	qid = self.request.get('qid')
    	question_key = ndb.Key('Question', int(qid))
    	question = question_key.get()
    	answers = Answer.query(ancestor=question_key).order(-Answer.vote).fetch()

        template_values = getLoginTemplateStatus(self, users)
        template_values["question"] = question
        template_values["answers"] = answers
        template_values["user"] = users.get_current_user()

        template = JINJA_ENVIRONMENT.get_template('viewQuestion.html', parent='layout.html')
        self.response.write(template.render(template_values))
    
# [END view_question]

# [START answer_question]
class AnswerQuestion(webapp2.RequestHandler):
    def get(self):
        qid = self.request.get('qid')
        query_params = {'qid': qid}
        self.redirect('/view?' + urllib.urlencode(query_params))
    def post(self):
        qid = self.request.get('qid')
        question_key = ndb.Key('Question', int(qid))
        answer = Answer(parent=question_key)
        if users.get_current_user():
            answer.author = users.get_current_user()
        answer.content = self.request.get('content')

        answer.put()
        time.sleep(0.1)

        query_params = {'qid': qid}
        self.redirect('/view?' + urllib.urlencode(query_params))
    
# [END answer_question]

application = webapp2.WSGIApplication([
    ('/view', ViewQuestion),
    ('/answer', AnswerQuestion),
], debug=True)