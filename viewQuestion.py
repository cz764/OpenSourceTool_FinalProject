# [START imports]
import os
import urllib

from google.appengine.api import users
from google.appengine.ext import ndb

from models import *        # custom models
from jane import *

import jinja2
import webapp2
import time

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(os.path.abspath(__file__)) + '/view/'),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)
# [END imports]

def redirectToQuestion(self, qid):
    query_params = {'qid': qid}
    self.redirect('/view?' + urllib.urlencode(query_params))

def getQandAs(qid, template_values):
    question = question_key(qid).get()
    answers = Answer.query(ancestor=question_key(qid)).order(-Answer.vote).fetch()
    template_values["question"] = question
    template_values["answers"] = answers
    return template_values

# [START view_question]
class ViewQuestion(webapp2.RequestHandler):
    def get(self):
    	qid = self.request.get('qid')

        template_values = getLoginTemplateStatus(self, users)
        template_values = getQandAs(qid, template_values)
        template_values["user"] = users.get_current_user()

        template = JINJA_ENVIRONMENT.get_template('viewQuestion.html', parent='layout.html')
        self.response.write(template.render(template_values))
    
# [END view_question]

# [START answer_question]
class AnswerQuestion(webapp2.RequestHandler):
    def get(self):
        qid = self.request.get('qid')
        redirectToQuestion(self, qid)
    def post(self):
        qid = self.request.get('qid')
        answer = Answer(parent=question_key(qid))
        if users.get_current_user():
            answer.author = users.get_current_user()
        answer.content = self.request.get('content')

        answer.put()
        time.sleep(0.1)
        redirectToQuestion(self,qid)
    
# [END answer_question]

# [START edit_content]
class EditContent(webapp2.RequestHandler):
    def post(self):
        qid = self.request.get('qid')
        aid = self.request.get('aid')
        if aid:
            answer = answer_key(qid, aid).get()
            answer.content = self.request.get('content')
            answer.put()
            time.sleep(0.1)
        else:
            question = question_key(qid).get()
            question.content = self.request.get('content')
            question.tags = strip_tags(self.request.get('tags'))
            question.put()
            time.sleep(0.1)
        redirectToQuestion(self, qid)

# [END edit_content]

application = webapp2.WSGIApplication([
    ('/view', ViewQuestion),
    ('/answer', AnswerQuestion),
    ('/edit', EditContent),
], debug=True)