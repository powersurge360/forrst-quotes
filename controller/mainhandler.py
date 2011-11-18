from base import *
import model

class MainHandler(Base):
    """
        Controller that handles the frontpage.
    """

    def get(self):
        """
            GET - Shows the homepage containing a list of quotes.
        """

        quotes = model.QuoteDB.all().order('-created')
        self._render_view('index', {'quotes': quotes})
