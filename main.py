#!/usr/bin/env python

#   _   _  ___ _____   _____ _   _ _   _ _   ___   __
#  | \ | |/ _ \_   _| |  ___| | | | \ | | \ | \ \ / /
#  |  \| | | | || |   | |_  | | | |  \| |  \| |\ V / 
#  | |\  | |_| || |   |  _| | |_| | |\  | |\  | | |  
#  |_| \_|\___/ |_|   |_|    \___/|_| \_|_| \_| |_|                                                    

from google.appengine.ext import webapp, db
from google.appengine.ext.webapp import util

import datetime, cgi, json, hashlib

class QuoteDB(db.Model):
    quoteMD5    = db.StringProperty()
    quoteString = db.StringProperty(multiline=True)
    dateAdded   = db.DateTimeProperty(auto_now_add=True)

class QuoteAPIAdd(webapp.RequestHandler):
    def post(self):
        key   = hashlib.md5(self.request.get('quote')).hexdigest()
        quote = QuoteDB(key_name=cgi.escape(key))
        quote.quoteMD5    = key
        quote.quoteString = cgi.escape(self.request.get('quote'))
        quoteID = quote.put()

        self.response.headers['Content-Type'] = 'application/json'
        res = {"status" : "Yeah, whatever", "id" : quoteID.name() }
        self.response.out.write(json.dumps(res))

class QuoteAPIList(webapp.RequestHandler):
    def get(self):
        # GET ALL THE FUNNAY
        res = {"status" : "Yeah, whatever", "quotes":[] }
        quotes = db.GqlQuery("SELECT * FROM QuoteDB")
        for funnay in quotes:
            res['quotes'].append({ 
                "id"    : funnay.quoteMD5,
                "quote" : funnay.quoteString
            })

        self.response.headers['Content-Type'] = 'application/json'
        self.response.out.write(json.dumps(res))
            

class MainHandler(webapp.RequestHandler):
    def get(self):
        self.response.out.write(open('./index.html').read())

def main():
    application = webapp.WSGIApplication([('/', MainHandler),
                                        ('/api/add', QuoteAPIAdd),
                                        ('/api/list', QuoteAPIList),
                                        ], debug=True)
    util.run_wsgi_app(application)

if __name__ == '__main__':
    main()
