from google.appengine.ext import db

# _________________________________________ 
#/ <eggsby> I know it insulted his         \
#\ intelligence but his code insulted mine /
# ----------------------------------------- 
#        \   ^__^
#         \  (oo)\_______
#            (__)\       )\/\
#                ||----w |
#                ||     ||

class QuoteDB(db.Model):
    quoteMD5    = db.StringProperty()
    quoteString = db.StringProperty(multiline=True)
    created     = db.DateTimeProperty(auto_now_add=True)
    votesUp     = db.IntegerProperty()
    votesDown   = db.IntegerProperty()
