from google.appengine.ext import db

#
# Saving votes per IP to prevent users voting like crazy
# as that wouldn't resemble the reality now would it?
#
class VoteDB(db.Model):
	id       = db.StringProperty()
	quote_id = db.StringProperty()
	ip_addr  = db.StringProperty()
	created  = db.DateTimeProperty(auto_now_add=True)
