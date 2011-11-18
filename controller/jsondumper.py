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
