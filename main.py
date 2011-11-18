#!/usr/bin/env python

#   _   _  ___ _____   _____ _   _ _   _ _   ___   __
#  | \ | |/ _ \_   _| |  ___| | | | \ | | \ | \ \ / /
#  |  \| | | | || |   | |_  | | | |  \| |  \| |\ V /
#  | |\  | |_| || |   |  _| | |_| | |\  | |\  | | |
#  |_| \_|\___/ |_|   |_|    \___/|_| \_|_| \_| |_|

from google.appengine.ext import webapp
from google.appengine.ext.webapp import util

from model.quotedb import *
from controller.jsondumper import *
from controller.quoteapi import *

import simplejson as json
import datetime, cgi, hashlib

class MainHandler(webapp.RequestHandler):
    def get(self):
        self.response.out.write(open('./index.html').read())

def main():
    materialdesigner = [
        ('/', MainHandler),
        ('/api/quote', QuoteAPI),
        ('/api/quote/([a-f\d]{32})', QuoteAPI)
    ]

    application = webapp.WSGIApplication(materialdesigner, debug=True)

    util.run_wsgi_app(application)

if __name__ == '__main__':
    main()
