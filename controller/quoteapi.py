import cgi, hashlib

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
        except db.BadKeyError, e:
            quote = None

        if quote:
            self.dump({
                "id": quote.id,
                "quote": quote.quote,
                "created": quote.created.isoformat(),
                "votes": quote.votes
            })
        else:
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
                "id": quote.id,
                "quote": quote.quote,
                "created": quote.created.isoformat(),
                "votes": quote.votes
            })

        self.dump(res)

    def post(self, id=None):
        """
            POST - Add a quote.
            Params: quote. If you can't figure out what that's for...
            Response: id of the new quote
        """

        if id:
            self.response.set_status(406)
            self.dump({"error": "don't post to a single quote"})
        else:
            quote_text = self._get_arg('quote')

            if quote_text:
                id = hashlib.md5(quote_text).hexdigest()
                quote = model.QuoteDB.get_by_key_name(id)

                if not quote:
                    quote = model.QuoteDB(key_name=id)
                    quote.id = id
                    quote.quote = quote_text
                    quote.votes = 0
                    quoteID = quote.put()

                    self.response.set_status(201) # created
                    self.dump({
                        "id" : quoteID.name()
                    })
                else:
                    self.response.set_status(403)
                    self.dump({"error": "yo don't overwrite some other dude's quote man"})
            else:
                self.response.set_status(406)
                self.dump({"error": "need quote"})
