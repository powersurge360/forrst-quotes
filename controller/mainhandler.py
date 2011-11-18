from base import *

class MainHandler(Base):
    def get(self):
        """
            GET - Shows the homepage containing a list of quotes.
        """

        self._render_view('index')
