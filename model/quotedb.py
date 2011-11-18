from google.appengine.ext import db

class QuoteDB(db.Model):
    quoteMD5    = db.StringProperty()
    quoteString = db.StringProperty(multiline=True)
    created     = db.DateTimeProperty(auto_now_add=True)
    votesUp     = db.IntegerProperty()
    votesDown   = db.IntegerProperty()
