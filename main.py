#!/usr/bin/env python

#   _   _  ___ _____   _____ _   _ _   _ _   ___   __
#  | \ | |/ _ \_   _| |  ___| | | | \ | | \ | \ \ / /
#  |  \| | | | || |   | |_  | | | |  \| |  \| |\ V /
#  | |\  | |_| || |   |  _| | |_| | |\  | |\  | | |
#  |_| \_|\___/ |_|   |_|    \___/|_| \_|_| \_| |_|

from google.appengine.ext import webapp
from google.appengine.ext.webapp import util

import controller

def main():
    url_mapping = [
        (r'/', controller.MainHandler),
        (r'/api/quote', controller.QuoteAPI),
        (r'/api/quote/([a-f\d]{32})', controller.QuoteAPI),
        (r'/api/vote', controller.VoteAPI)
    ]

    application = webapp.WSGIApplication(url_mapping, debug=True)

    util.run_wsgi_app(application)

if __name__ == '__main__':
    main()
