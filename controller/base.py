import os
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template

class Base(webapp.RequestHandler):
    """
        Base controller that makes it easier to render views.
    """

    view_path = "./view/%s.html"

    def _render_view(self, view, data = {}):
        """
            Renders the given view along with the given data and sends it to the
            layout.

            Parameters:
                - view: path/name of the view relative to the view/ directory
                  and without an extension.
                - data: A dictionary with keys and values to insert into the
                  template.

            Example:
                self._render_view('index', {'quotes': [....]})
        """

        self.response.out.write(template.render(self.view_path % (view), data))
