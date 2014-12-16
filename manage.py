# [START imports]
import os
import urllib
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

class ImageHandler(webapp2.RequestHandler):
    def get(self, url):
	# picture = Image.query(Image.url == url).get()
	# if picture.ifile:
	# 	self.response.headers['Content-Type'] = 'image/png'
	# 	self.response.out.write(picture.ifile)
		self.response.headers['Content-Type'] = 'text/plain'
		self.response.write("in ImageHandler")

class Uploader(webapp2.RequestHandler):
    def get(self):
		# header(self)
		# display = JINJA_ENVIRONMENT.get_template('temp_upload.html')
		# self.response.write(display.render())
		# footer(self)
		self.response.headers['Content-Type'] = 'text/plain'
		self.response.write("in uploader")
    def post(self):
		# header(self)
		# if users.get_current_user():
		# 	res = self.request.get('img')
		# 	image = Image()
		# 	image.ifile = res
		# 	image.user = str(users.get_current_user())
		# 	image_key = image.put()
		# 	image = Image.get_by_id(image_key.id())
		# 	image.url = str(image_key.id())+"_"+self.request.params['img'].filename
		# 	image.put()
		# self.response.write('<p class="main">Upload Success!</p>')
		# footer(self)
		self.response.headers['Content-Type'] = 'text/plain'
		self.response.write("in uploader post method")

class DeleteImage(webapp2.RequestHandler):
    def get(self, key):
	# if users.get_current_user():
	# 	img = Image.get_by_id(int(key))
	# 	user = str(users.get_current_user())
	# 	if img.user == user:
	# 		img.key.delete()
	# 	self.response.write('<p class="main"><b>Success!</b></p>')
	# else:
	# 	self.response.write('''<p class="main">You don't have permission!</p>''')
		self.response.headers['Content-Type'] = 'text/plain'
		self.response.write("in DeleteImage")
	


application = webapp2.WSGIApplication([
    ('/manage', ManagePage),
    ('/upload', Uploader),
    ('/img/delete/(.*)', DeleteImage),
    ('/img/(.*)', ImageHandler),
], debug=True)