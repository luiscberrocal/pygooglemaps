'''
Created on May 20, 2012

@author: luiscberrocal
'''
from google.appengine.ext import db
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
    

    