import cgi
import simplejson as json

from google.appengine.ext import webapp

class JSONDumper(webapp.RequestHandler):
    def dump(self, data):
        """
            Dump some json to the client and handle jsonp requests correctly
            Params: data. The data to dump as json
        """

        if self.request.get('callback'):
            self.response.headers['Content-Type'] = 'text/javascript'
            self.response.out.write(
                self.request.get('callback') + "({" + json.dumps(data) + "})")
        else:
            self.response.headers['Content-Type'] = 'application/json'
            self.response.out.write(json.dumps(data))

    def _get_arg(self, arg_name, default=''):
        """
            Gets you an escaped GET/POST parameter or None if there is no such argument
            Params: arg_name. obviously.
                    default. obvious as well.
        """

        value = self.request.get(arg_name, default)
        if type(default) is str:
            value = cgi.escape(value.strip())

        return value
