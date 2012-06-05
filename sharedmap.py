'''
Created on Jun 5, 2012

@author: luiscberrocal
'''
import jinja2
import webapp2
import os
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext import db
from models import Location

jinja_environment = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.join(os.path.dirname(__file__), "templates")))

class SharedMapHandler(webapp2.RequestHandler):
    def get(self, token):
        query = db.GqlQuery('SELECT * FROM Location WHERE token = :token', token  = token)
        locations = query.fetch(1, 0)
        if locations:
            template = jinja_environment.get_template('shared-map.html')
            data = locations[0].toDictionary()
            data['valid'] = True
        else:
            template = jinja_environment.get_template('shared-map.html')
            data = {"token" : token,
                    "valid" : False}
        self.response.out.write(template.render(data))
    
app = webapp2.WSGIApplication([(r'/shared/([^/]+)', SharedMapHandler)],
                              debug=True)

def main():
    run_wsgi_app(app)


if __name__ == "__main__":
    main()
