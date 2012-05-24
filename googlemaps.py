import webapp2
from google.appengine.ext.webapp.util import run_wsgi_app

from google.appengine.api import users
import jinja2
import os, settings
import datetime
import json
from models import Location
from google.appengine.ext import db
from django.utils import simplejson
  
jinja_environment = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.join(os.path.dirname(__file__), "templates")))
    
class MainPage(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()

        if user:
            template = jinja_environment.get_template('mappage.html')
            data = {"title" : "Mi Nuevo Titulo " + user.nickname(), 
                    "GOOGLE_MAPS_KEY" : settings.GOOGLE_MAPS_KEY,
                    "username" : user.nickname()}
            self.response.out.write(template.render(data))
            #self.response.headers['Content-Type'] = 'text/plain'
            #self.response.out.write('Hello, ' + user.nickname())
        else:
            #self.response.out.write('Hello, Stranger' )
            self.redirect(users.create_login_url(self.request.uri))

class ListLocations(webapp2.RequestHandler):
    def get(self):
        
        #query = db.GqlQuery('SELECT * FROM Location WHERE owner = :owner', owner = users.get_current_user().nickname())
        user = users.get_current_user()
        if user:
            query = db.GqlQuery('SELECT * FROM Location WHERE owner = :owner', owner = user)
            locations = query.fetch(50)
            mlocs = []
            for loc in locations:
                mlocs.append({'date': loc.date.strftime('%Y-%m-%d %H:%M:%S'),
                              'name': loc.name, 
                              'latitude' : loc.latitude,
                              'longitude' :loc.longitude,
                              'zoom' :loc.zoom,
                              'owner' : loc.owner.nickname()})
            json = simplejson.dumps(mlocs)
        else:
            raise Exception('NO User')
        self.response.write(json)
        
class LocationAdmin(webapp2.RequestHandler):
    def post(self):
        locdata = {
            'owner': users.get_current_user().nickname(),
            'name' : self.request.get('name'),
            'latitude' : float(self.request.get('latitude')),
            'longitude' : float(self.request.get('longitude')),
            'zoom' : int(self.request.get('zoom'))
        }
        #print locdata
        location = Location(owner = users.get_current_user())
        location.name = locdata['name']
        location.latitude = locdata['latitude']
        location.longitude = locdata['longitude']
        location.zoom = locdata['zoom']
        
        location.put()
        locdata['id'] =  451 #location.id
        locdata['date'] = location.date.strftime('%Y-%m-%d %H:%M:%S')
        
        #now= datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                
        #json_data = {"status" : "Saved", 'date' : now}
        self.response.headers['Content-Type'] = 'application/json'
        self.response.out.write(json.dumps(locdata))
        
        
app = webapp2.WSGIApplication([('/', MainPage),
                               ('/add-location.html', LocationAdmin),
                               ('/list-locations.json', ListLocations)],
                              debug=True)

def main():
    run_wsgi_app(app)


if __name__ == "__main__":
    main()
