'''
Created on Jun 5, 2012

@author: luiscberrocal
'''
import jinja2
import webapp2
import os
from google.appengine.ext.webapp.util import run_wsgi_app


jinja_environment = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.join(os.path.dirname(__file__), "templates")))

class SharedMapHandler(webapp2.RequestHandler):
    def get(self, token):
        template = jinja_environment.get_template('shared-map.html')
        data = {"token" : token}
        self.response.out.write(template.render(data))
    
app = webapp2.WSGIApplication([(r'/shared/([^/]+)', SharedMapHandler)],
                              debug=True)

def main():
    run_wsgi_app(app)


if __name__ == "__main__":
    main()
