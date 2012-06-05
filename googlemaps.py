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
import md5
  
jinja_environment = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.join(os.path.dirname(__file__), "templates")))
    

    

class MainPage(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()

        if user:
            template = jinja_environment.get_template('map-layout.html')
            logoff_url =users.create_logout_url(self.request.uri)
            data = {"title" : "Mi Nuevo Titulo " + user.nickname(), 
                    "GOOGLE_MAPS_KEY" : settings.GOOGLE_MAPS_KEY,
                    "username" : user.nickname(),
                    "logoff_url": logoff_url}
            self.response.out.write(template.render(data))
            
        else:
            #self.response.out.write('Hello, Stranger' )
            self.redirect(users.create_login_url(self.request.uri))

class ListLocations(webapp2.RequestHandler):
    def get(self):
        
        #query = db.GqlQuery('SELECT * FROM Location WHERE owner = :owner', owner = users.get_current_user().nickname())
        user = users.get_current_user()
        if user:
            query = db.GqlQuery('SELECT * FROM Location WHERE owner = :owner ORDER BY date DESC', owner = user)
            locations = query.fetch(50)
            mlocs = []
            for loc in locations:
                mlocs.append(loc.toDictionary())
            json = simplejson.dumps(mlocs)
        else:
            raise Exception('NO User loggedin')
        self.response.write(json)
class DeleteLocations(webapp2.RequestHandler):
    def post(self):
        mid = self.request.get('id')
        loc =  Location.get_by_id(int(mid))
        res = {}
        if loc:
            res = loc.toDictionary()
            loc.delete()
            res['success'] = True
        else:
            res['success'] = False
        json = simplejson.dumps(res)
        self.response.write(json)

def add_location(request, loc_type, map_source ="google-maps", visibility = "private"):
    location = Location(owner = users.get_current_user(), 
                            map_source =map_source, loc_type = loc_type)
    location.visibility = visibility
    
    if loc_type == "extent":
        location.name = request.get('loc-name')
        location.latitude = float(request.get('latitude'))
        location.longitude =float(request.get('longitude'))
        location.zoom = int(request.get('zoom'))
    elif loc_type == "point":
        location.name = request.get('point-name')
        location.latitude = float(request.get('latitude-point'))
        location.longitude =float(request.get('longitude-point'))
        location.zoom = int(request.get('zoom-point'))
    tkn = location.buildToken()
    location.token = tkn
        
    location.put()
    return location.toJSON()
        
        
        

class AddLocation(webapp2.RequestHandler):
    def post(self):
        json = add_location(self.request, "extent")
        self.response.out.write(json)
        
class AddPoint(webapp2.RequestHandler):
    def post(self):
        json = add_location(self.request, "point")
        self.response.out.write(json)
                
app = webapp2.WSGIApplication([('/', MainPage),
                               ('/add-location.html', AddLocation),
                               ('/list-locations.json', ListLocations), 
                               ('/delete-locations.json', DeleteLocations),
                               ('/add-point.html', AddPoint),],
                              debug=True)

def main():
    run_wsgi_app(app)


if __name__ == "__main__":
    main()
