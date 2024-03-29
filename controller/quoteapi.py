import cgi, hashlib
from datetime import datetime

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
            Params: limit. default 20, max 1000 for heaven's sake
                    offset. starting from zero.
                    order_by. can be 'created' or 'votes' - default 'created'
                    order. ASC or DESC - default DESC
            Response: A lot of JSON...
        """

        limit = self._get_arg("limit", 20)
        offset = self._get_arg("offset", 0)
        order_by = self._get_arg("order_by", "created")
        order = self._get_arg("order", "DESC")

        if limit < 0:
            limit = 20
        elif limit > 1000:
            limit = 1000

        if offset < 0:
            offset = 0

        if order_by != "votes":
            order_by = "created"

        order = "" if order == "ASC" else "-"

        # SERIOUSLY GOOGLE Y U TROLL ME? Y U NO MAKE SYMBOLS WORK HERE?
        #quotes = model.QuoteDB.gql("ORDER BY "+order_by+" "+order+" LIMIT "+str(limit)+" OFFSET "+str(offset))
        quotes = (model.QuoteDB.all()
            .order(order+order_by)
            .fetch(limit=limit, offset=offset)
        )

        res = []

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
                    date. Optional date of this quote. DO NOT USE EXCEPT YOU ARE SQUEEKS - Format: 'YYYY-MM-DD hh:mm:ss' or without the time
            Response: id of the new quote
        """

        if id:
            self.response.set_status(406)
            self.dump({"error": "don't post to a single quote"})
        else:
            quote_text = self._get_arg("quote")

            if quote_text:
                id = hashlib.md5(quote_text).hexdigest()
                quote = model.QuoteDB.get_by_key_name(id)

                if not quote:
                    quote = model.QuoteDB(
                        id=id,
                        quote=quote_text,
                        votes=0,
                    )
                    quote_date = self._parse_date(self._get_arg('date'))
                    if quote_date:
                        quote.created = quote_date
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

    def _parse_date(self, date_str):
        """
            Parse a string to a date using ISO8601 formats
            Returns a datetime instance or None on failure
        """
        try:
            return datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S')
        except ValueError:
            try:
                return datetime.strptime(date_str, '%Y-%m-%d')
            except ValueError:
                return None
