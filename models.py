from google.appengine.ext import ndb

DEFAULT_QUESTION_NAME = 'default_question'

def question_key(qid):
    """Constructs a Datastore key for a Question entity with question_id."""
    return ndb.Key('Question', int(qid))

def answer_key(aid):
    """Constructs a Datastore key for a Question entity with question_id."""
    return ndb.Key('Answer', int(aid))

class Question(ndb.Model):
    author = ndb.UserProperty()
    title = ndb.StringProperty(indexed=False)
    content = ndb.StringProperty(indexed=False)
    date_create = ndb.DateTimeProperty(auto_now_add=True)
    date_edit = ndb.DateTimeProperty(auto_now=True)
    tags = ndb.StringProperty(repeated=True)
    ups = ndb.StringProperty(repeated=True, indexed=False)        # stores a list of users who voted up on this question
    downs = ndb.StringProperty(repeated=True, indexed=False)       # stores a list of users who voted down on this question
    vote = ndb.ComputedProperty(lambda self: len(self.ups) - len(self.downs))

class Answer(ndb.Model):
    author = ndb.UserProperty()
    content = ndb.StringProperty(indexed=False)
    date_create = ndb.DateTimeProperty(auto_now_add=True)
    date_edit = ndb.DateTimeProperty(auto_now=True)
    ups = ndb.StringProperty(repeated=True, indexed=False)        # stores a list of users who voted up on this question
    downs = ndb.StringProperty(repeated=True, indexed=False)       # stores a list of users who voted down on this question
    vote = ndb.ComputedProperty(lambda self: len(self.ups) - len(self.downs))


class Vote(ndb.Model):
    users = ndb.JsonProperty(repeated=True)     # stores the json list for voted users
    up = ndb.IntegerProperty(default=0)
    down = ndb.IntegerProperty(default=0)
    vote = ndb.ComputedProperty(lambda self: self.up - self.down)

    
