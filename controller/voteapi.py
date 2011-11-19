from datetime import datetime, timedelta

from jsondumper import *
from google.appengine.ext import db

import model

class VoteAPI(JSONDumper):
    def post(self):
        """
            POST - Make a new vote
            Params: quote_id. the id (MD5) of the quote to vote for
                    vote: 1 or -1 to make your vote
            Returns: JSON object of the updated quote
        """

        quote_id = self._get_arg('quote_id')
        vote_value = self._get_arg('vote')

        if vote_value == '1' or vote_value == '-1':
            try:
                quote = model.QuoteDB.get_by_key_name(quote_id)
            except (db.BadKeyError, db.BadValueError):
                quote = None

            if quote:
                id = quote.id + '_' + self.request.remote_addr
                vote = model.VoteDB.get_by_key_name(id)

                # allow voting once a day
                if vote and (datetime.now() - vote.created) < timedelta(days=1):
                    self.response.set_status(403)
                    self.dump({"error": "you may only vote once every 24 hours for every quote"})
                    return

                vote = model.VoteDB(key_name=id)
                vote.id = id
                vote.quote_id = quote.id
                vote.ip_addr = self.request.remote_addr
                vote.put()

                if vote_value == '1':
                    quote.votes += 1
                else:
                    quote.votes -= 1
                quote.put()

                self.response.set_status(201)
                self.dump({
                    "id": quote.id,
                    "quote": quote.quote,
                    "created": quote.created.isoformat(),
                    "votes": quote.votes
                })
            else:
                self.response.set_status(406)
                self.dump({"error": "no such quote"})
        else:
            self.response.set_status(406)
            self.dump({"error": "you gotta make a vote (1 or -1)"})
