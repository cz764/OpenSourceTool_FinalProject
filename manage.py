# [START imports]
import os
import urllib
import time
from jane import *		# custom python script
from models import *

from google.appengine.api import users
from google.appengine.ext import ndb
from google.appengine.api import images

import jinja2
import webapp2


JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(os.path.abspath(__file__)) + '/view/'),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)
# [END imports]

list_html = 'list.html'
upload_html = 'upload.html'

def writingToTemplate(self, template_values, temp):
	template = JINJA_ENVIRONMENT.get_template(temp, parent='layout.html')
	self.response.write(template.render(template_values))

def getImgTemplateValue(self):
	template_values = getLoginTemplateStatus(self, users)
	user = users.get_current_user()
	images = Image.get_author(user)
	template_values["images"] = images
	return template_values

# [START manage_page]
class ManagePage(webapp2.RequestHandler):
	def get(self):
		if users.get_current_user():
			template_values = getQuestionList(self, True)
			template_values["isManaging"] = True
			template_values["user"] = users.get_current_user()
			writingToTemplate(self, template_values, list_html)
		else:
			template_values = getLoginTemplateStatus(self, users)
			template_values["isManaging"] = True
			writingToTemplate(self, template_values, list_html)
    
# [END manage_page]

class ImageHandler(webapp2.RequestHandler):
    def get(self, url):
		picture = Image.query(Image.url == url).get()
		if picture.ifile:
			self.response.headers['Content-Type'] = 'image/png'
			self.response.out.write(picture.ifile)
		
class Uploader(webapp2.RequestHandler):
	def get(self):
		template_values = getImgTemplateValue(self)
		template_values["display_uploader"] = True	
		writingToTemplate(self, template_values, upload_html)
	def post(self):
		template_values = {}
		if users.get_current_user():
			img = self.request.get('img')
			image = Image()
			image.ifile = img
			image.user = users.get_current_user()
			image_key = image.put()
			image = Image.get_by_id(image_key.id())
			image.url = str(image_key.id())+"_"+self.request.params['img'].filename
			image.put()
			time.sleep(0.1)
			template_values = getImgTemplateValue(self)
			template_values["status"] = "Success!"
		else:
			template_values = getLoginTemplateStatus(self, users)
			template_values["status"] = "Failed:( You're not logged in yet!"
		template_values["display_uploader"] = False
		
		writingToTemplate(self, template_values, upload_html)
	

class DeleteImage(webapp2.RequestHandler):
    def get(self, key):
		if users.get_current_user():
			img = Image.get_by_id(int(key))
			user = users.get_current_user()
			if img.user == user:
				img.key.delete()
			template_values = getImgTemplateValue(self)
			template_values["status"] = "Success!"
			template_values["display_uploader"] = False
			writingToTemplate(self, template_values, upload_html)
		else:
			template_values = getLoginTemplateStatus(self)
			template_values["status"] = "Failed:( You don't have permission!"
			template_values["display_uploader"] = False
			writingToTemplate(self, template_values, upload_html)
	


application = webapp2.WSGIApplication([
    ('/manage', ManagePage),
    ('/upload', Uploader),
    ('/img/delete/(.*)', DeleteImage),
    ('/img/(.*)', ImageHandler),
], debug=True)