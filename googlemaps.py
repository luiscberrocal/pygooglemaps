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
            query = db.GqlQuery('SELECT * FROM Location WHERE owner = :owner', owner = user)
            locations = query.fetch(50)
            mlocs = []
            for loc in locations:
                mlocs.append({'id' : loc.key().id(),
                              'date': loc.date.strftime('%Y-%m-%d %H:%M:%S'),
                              'name': loc.name, 
                              'latitude' : loc.latitude,
                              'longitude' :loc.longitude,
                              'zoom' :loc.zoom,
                              'owner' : loc.owner.nickname()})
            json = simplejson.dumps(mlocs)
        else:
            raise Exception('NO User')
        self.response.write(json)
class DeleteLocations(webapp2.RequestHandler):
    def post(self):
        mid = self.request.get('id')
        loc =  Location.get_by_id(int(mid))
        res = {}
        if loc:
            loc.delete()
            res['success'] = True
        else:
            res['success'] = False
        json = simplejson.dumps(res)
        self.response.write(json)
                      
class AddLocation(webapp2.RequestHandler):
    def post(self):
        locdata = {
            'owner': users.get_current_user().nickname(),
            'name' : self.request.get('name'),
            'latitude' : float(self.request.get('latitude')),
            'longitude' : float(self.request.get('longitude')),
            'zoom' : int(self.request.get('zoom'))
        }
        #print locdata
        location = Location(owner = users.get_current_user(), 
                            map_source ="google-maps", loc_type = "extent")
        location.name = locdata['name']
        location.latitude = locdata['latitude']
        location.longitude = locdata['longitude']
        location.zoom = locdata['zoom']
        #location.loc_type = "extent"
        #location.map_source ="google-maps"
        location.visibility = "private"
        m = md5.new()
        m.update(location.name)
        location.token = m.hexdigest()
        location.put()
        locdata['id'] =  location.key().id()
        locdata['date'] = location.date.strftime('%Y-%m-%d %H:%M:%S')
        
        #now= datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                
        #json_data = {"status" : "Saved", 'date' : now}
        self.response.headers['Content-Type'] = 'application/json'
        self.response.out.write(json.dumps(locdata))
        
        
app = webapp2.WSGIApplication([('/', MainPage),
                               ('/add-location.html', AddLocation),
                               ('/list-locations.json', ListLocations), 
                               ('/delete-locations.json', DeleteLocations)],
                              debug=True)

def main():
    run_wsgi_app(app)


if __name__ == "__main__":
    main()
