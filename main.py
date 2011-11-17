#!/usr/bin/env python

#   _   _  ___ _____   _____ _   _ _   _ _   ___   __
#  | \ | |/ _ \_   _| |  ___| | | | \ | | \ | \ \ / /
#  |  \| | | | || |   | |_  | | | |  \| |  \| |\ V /
#  | |\  | |_| || |   |  _| | |_| | |\  | |\  | | |
#  |_| \_|\___/ |_|   |_|    \___/|_| \_|_| \_| |_|

from google.appengine.ext import webapp, db
from google.appengine.ext.webapp import util

import simplejson as json

import datetime, cgi, hashlib

class QuoteDB(db.Model):
    quoteMD5    = db.StringProperty()
    quoteString = db.StringProperty(multiline=True)
    created     = db.DateTimeProperty(auto_now_add=True)
    votesUp     = db.IntegerProperty()
    votesDown   = db.IntegerProperty()


class JSONDumper(webapp.RequestHandler):
    """
        Dump some json to the client and handle jsonp requests correctly
        Params: data. The data to dump as json
    """
    def dump(self, data):
        if self.request.get('callback'):
            self.response.headers['Content-Type'] = 'text/javascript'
            self.response.out.write(
                self.request.get('callback') + "({" + json.dumps(data) + "})")
        else:
            self.response.headers['Content-Type'] = 'application/json'
            self.response.out.write(json.dumps(data))

"""
    Handler class responsible for interacting with single quotes
"""
class QuoteAPI(JSONDumper):
    """
        GET - Get all quotes or a single one
        Params: id. to get a single quote
        Returns: JSON object(s) of quote(s)
    """
    def get(self, id=None):
        if id:
            self._get_single(id)
        else:
            self._get_all()


    """
        GET - Get a single quote
        Params: id. The md5 digest of the quote
        Response: quote object
    """
    def _get_single(self, id):
        try:
            quote = QuoteDB.get_by_key_name(id)
            self.dump({
                "id": quote.quoteMD5,
                "quote": quote.quoteString,
                "created": quote.created.isoformat(),
                "votes": {
                    "up": quote.votesUp,
                    "down": quote.votesDown
                }
            })
        except db.BadKeyError, e:
            self.response.set_status(404)
            self.dump({"error": "no such id"})


    """
        GET - List all the quotes.
        Params: nada
        Response: A lot of JSON...
    """
    def _get_all(self):
        # GET ALL THE FUNNAY
        res = []
        quotes = db.GqlQuery("SELECT * FROM QuoteDB")
        for quote in quotes:
            res.append({
                "id": quote.quoteMD5,
                "quote": quote.quoteString,
                "created": quote.created.isoformat(),
                "votes": {
                    "up": quote.votesUp,
                    "down": quote.votesDown
                }
            })

        self.dump(res)


    """
        POST - Add a quote.
        Params: quote. If you can't figure out what that's for...
        Response: id of the new quote
    """
    def post(self):
        quoteStr = cgi.escape(self.request.get('quote').strip())
        if quoteStr:
            key   = hashlib.md5(quoteStr).hexdigest()
            quote = QuoteDB(key_name=cgi.escape(key))
            quote.quoteMD5 = key
            quote.quoteString = quoteStr
            quote.votesUp = 0
            quote.votesDown = 0
            quoteID = quote.put()

            self.response.set_status(201) # created
            self.dump({"id" : quoteID.name() })
        else:
            self.response.set_status(406)
            self.dump({"error": "need quote"})


class MainHandler(webapp.RequestHandler):
    def get(self):
        self.response.out.write(open('./index.html').read())


def main():
    mapping = [
        ('/', MainHandler),
        ('/api/quote', QuoteAPI),
        ('/api/quote/([a-f\d]{32})', QuoteAPI)
    ]
    application = webapp.WSGIApplication(mapping, debug=True)
    util.run_wsgi_app(application)

if __name__ == '__main__':
    main()
