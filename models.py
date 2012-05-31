'''
Created on May 20, 2012

@author: luiscberrocal
'''
from google.appengine.ext import db
from django.utils import simplejson
import md5
class Location(db.Model):
    owner = db.UserProperty()
    latitude = db.FloatProperty()
    longitude = db.FloatProperty()
    name = db.StringProperty()
    zoom = db.IntegerProperty()
    date = db.DateTimeProperty(auto_now_add=True)
    loc_type = db.StringProperty(required=True, choices=set(["extent", "point"]))
    token = db.StringProperty()
    visibility = db.StringProperty(choices=set(["shared", "private"]))
    expires = db.IntegerProperty()
    map_source = db.StringProperty(required=True, choices=set(["google-maps", "open-street-maps"]))
    def toDictionary(self):
        locdata = {}
        locdata['id'] =  self.key().id()
        locdata['name'] = self.name
        locdata['date'] = self.date.strftime('%Y-%m-%d %H:%M:%S')
        locdata['owner'] = self.owner.email()
        locdata['latitude'] = self.latitude
        locdata['longitude'] = self.longitude
        locdata['zoom'] = self.zoom
        locdata['loc_type'] = self.loc_type
        locdata['token'] = self.token
        locdata['visibility'] = self.visibility
        locdata['expires'] = self.expires
        locdata['map_source'] = self.map_source
        return locdata
    
    def toJSON(self):
        locdata = self.toDictionary()
        json = simplejson.dumps(locdata)            
        return json
    
    def buildToken(self):
        m = md5.new()
        m.update(self.name)
        m.update(self.owner.email())
        return m.hexdigest()

    