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
    id        = db.StringProperty()
    quote     = db.StringProperty(multiline=True)
    created   = db.DateTimeProperty(auto_now_add=True)
    votes     = db.IntegerProperty()
    admin_key = db.StringProperty()

    def __str__(self):
        if self.votes < 0:
            return self.quote + ' (' + str(self.votes) + ')'
        return self.quote + ' (+' + str(self.votes) + ')'
