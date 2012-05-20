import webapp2
from google.appengine.ext.webapp.util import run_wsgi_app

from google.appengine.api import users
import jinja2
import os, settings

jinja_environment = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.join(os.path.dirname(__file__), "templates")))
    
class MainPage(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()

        if user:
            template = jinja_environment.get_template('mappage.html')
            data = {"title" : "Mi Nuevo Titulo " + user.nickname(), 
                    "GOOGLE_MAPS_KEY" : settings.GOOGLE_MAPS_KEY}
            self.response.out.write(template.render(data))
            #self.response.headers['Content-Type'] = 'text/plain'
            #self.response.out.write('Hello, ' + user.nickname())
        else:
            #self.response.out.write('Hello, Stranger' )
            self.redirect(users.create_login_url(self.request.uri))

app = webapp2.WSGIApplication([('/', MainPage)],
                              debug=True)

def main():
    run_wsgi_app(app)


if __name__ == "__main__":
    main()
