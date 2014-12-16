import os
import urllib

from google.appengine.api import users
from google.appengine.ext import ndb

from models import *        # custom models
from jane import *

import jinja2
import webapp2
import time

# [END imports]

# [START vote_up]
class VoteUp(webapp2.RequestHandler):
    def get(self):
        qid = self.request.get('qid')
        query_params = {'qid': qid}
        self.redirect('/view?' + urllib.urlencode(query_params))        
    def post(self):
        qid = self.request.get('qid')
        aid = self.request.get('aid')
        user = users.get_current_user().nickname()
        query_params = {'qid': qid}
        if aid:
        	answer = answer_key(qid, aid).get()
        	if answer:
	        	if user in answer.ups:
	        		self.redirect('/view?' + urllib.urlencode(query_params))
	        	else:
	        		answer.ups.append(user)
	        		answer.put()
	        else:
	        	self.response.headers['Content-Type'] = 'text/plain'
    			self.response.write('cannot find answer!')
        else:
        	question = question_key(qid).get()
        	if user in question.ups:
        		self.redirect('/view?' + urllib.urlencode(query_params))
        	else:
        		question.ups.append(user)
        		question.put()
        
        time.sleep(0.1)

        query_params = {'qid': qid}
        self.redirect('/view?' + urllib.urlencode(query_params))
    
    	# self.response.headers['Content-Type'] = 'text/plain'
    	# self.response.write('Vote Up completed!')
# [END view_question]


# [START vote_down]
class VoteDown(webapp2.RequestHandler):
    def get(self):
        qid = self.request.get('qid')
        query_params = {'qid': qid}
        self.redirect('/view?' + urllib.urlencode(query_params))    
    def post(self):
        qid = self.request.get('qid')
        aid = self.request.get('aid')
        user = users.get_current_user().nickname()
        query_params = {'qid': qid}
        if aid:
            answer = answer_key(qid, aid).get()
            if answer:
                if user in answer.downs:
                    self.redirect('/view?' + urllib.urlencode(query_params))
                else:
                    answer.downs.append(user)
                    answer.put()
            else:
                self.response.headers['Content-Type'] = 'text/plain'
                self.response.write('cannot find answer!')
        else:
            question = question_key(qid).get()
            if user in question.downs:
                self.redirect('/view?' + urllib.urlencode(query_params))
            else:
                question.downs.append(user)
                question.put()
        
        time.sleep(0.1)

        query_params = {'qid': qid}
        self.redirect('/view?' + urllib.urlencode(query_params))
    
# [END vote_down]



application = webapp2.WSGIApplication([
    ('/vote/up?.*', VoteUp),
    ('/vote/down?.*', VoteDown),
], debug=True)