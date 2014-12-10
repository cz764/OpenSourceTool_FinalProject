from google.appengine.ext import ndb

DEFAULT_QUESTION_NAME = 'default_question'

def question_key(question_name=DEFAULT_QUESTION_NAME):
    """Constructs a Datastore key for a Question entity with question_name."""
    return ndb.Key('Questions', question_name)


class Question(ndb.Model):
    author = ndb.UserProperty()
    title = ndb.StringProperty(indexed=False)
    content = ndb.StringProperty(indexed=False)
    date_create = ndb.DateTimeProperty(auto_now_add=True)
    date_edit = ndb.DateTimeProperty(auto_now=True)
    tags = ndb.StringProperty(repeated=True)
    up = ndb.IntegerProperty(default=0)
    down = ndb.IntegerProperty(default=0)
    vote = ndb.ComputedProperty(lambda self: self.up - self.down)

class Answer(ndb.Model):
    author = ndb.UserProperty()
    content = ndb.StringProperty(indexed=False)
    date_create = ndb.DateTimeProperty(auto_now_add=True)
    date_edit = ndb.DateTimeProperty(auto_now=True)
    up = ndb.IntegerProperty(default=0)
    down = ndb.IntegerProperty(default=0)
    vote = ndb.ComputedProperty(lambda self: self.up - self.down)


class Collection(ndb.Model):
    Question
    answers = ndb.JsonProperty(repeated=True)       # stores a list of answer json
