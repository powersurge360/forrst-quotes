import datetime, cgi, hashlib

from jsondumper import *
from google.appengine.ext import db

import model

class QuoteAPI(JSONDumper):
    def get(self, id=None):
        """
            GET - Get all quotes or a single one
            Params: id. to get a single quote
            Returns: JSON object(s) of quote(s)
        """

        if id:
            self._get_single(id)
        else:
            self._get_all()

    def _get_single(self, id):
        """
            GET - Get a single quote
            Params: id. The md5 digest of the quote
            Response: quote object
        """
        try:
            quote = model.QuoteDB.get_by_key_name(id)
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

    def _get_all(self):
        """
            GET - List all the quotes.
            Params: nada
            Response: A lot of JSON...
        """
        # GET ALL THE FUNNAY
        res = []
        #quotes = db.GqlQuery("SELECT * FROM QuoteDB")
        quotes = model.QuoteDB.all()
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

    def post(self):
        """
            POST - Add a quote.
            Params: quote. If you can't figure out what that's for...
            Response: id of the new quote
        """

        quoteStr = cgi.escape(self.request.get('quote').strip())

        if quoteStr:
            key   = hashlib.md5(quoteStr).hexdigest()
            quote = model.QuoteDB(key_name=cgi.escape(key))
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
