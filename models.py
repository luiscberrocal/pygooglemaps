'''
Created on May 20, 2012

@author: luiscberrocal
'''
from google.appengine.ext import db
class Locations(db.Model):
    owner = db.UserProperty()
    latitude = db.IntegerProperty()
    longitude = db.IntegerProperty()
    name = db.StringProperty()
    zoom = db.IntegerProperty()
    date = db.DateTimeProperty(auto_now_add=True)
    