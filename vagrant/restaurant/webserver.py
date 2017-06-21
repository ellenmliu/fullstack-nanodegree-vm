from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import cgi

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem

# Create session and connect to DB
engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

class WebServerHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        #Displays all the restaurants in the database with options to create, edit, update, and delete
        if self.path.endswith("/restaurants"):
            restaurants = session.query(Restaurant).all()
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            output = ""
            output += "<html><body>"
            output += "<h1>Restaurants</h1>"
            output += "<a href = 'restaurants/new'>Create a new restaurant</a>"
            for restaurant in restaurants:
                output += "<p>" + restaurant.name + "</p>"
                output += "<a href = 'restaurants/"+ str(restaurant.id) +"/edit'>Edit</a> <a href = \
                    'restaurants/"+ str(restaurant.id) +"/delete'>Delete</a>"
            output += "</body></html>"
            self.wfile.write(output)
            return
        #Add in a new restaurant to the database
        if self.path.endswith("/restaurants/new"):
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            output = ""
            output += "<html><body>"
            output += '''<form method='POST' enctype='multipart/form-data' action='/restaurants/new'>\
                    <h2>What's a new restaurant?</h2><input name="newRestaurantName" type="text"\
                    ><input type="submit" value="Create"> </form>'''
            output += "</body></html>"
            self.wfile.write(output)
            return
        #Edit an existing restaurant in the database
        if self.path.endswith("/edit"):
            path = self.path.split('/')
            index = path[2]
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            tempName = session.query(Restaurant).filter_by(id = index).one()
            output = ""
            output += "<html><body>"
            output += '''<form method='POST' enctype='multipart/form-data' action='restaurants/''' + index + '''/edit'>\
                    <h2>What's a new name for '''+tempName.name+ '''?</h2><input name="updateName" type="text"\
                    ><input type="submit" value="Update"> </form>'''
            output += "</body></html>"
            self.wfile.write(output)
            return
        #Delete an existing restaurant from the database
        if self.path.endswith("/delete"):
            path = self.path.split('/')
            index = path[2]
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            tempName = session.query(Restaurant).filter_by(id = index).one()
            output = ""
            output += "<html><body>"
            output += '''<form method='POST' enctype='multipart/form-data' action='restaurants/''' + index + '''/delete'>\
                    <h2>Are you sure you want to delete '''+tempName.name+ '''?</h2><input type="submit" value="Delete"> </form>'''
            output += "</body></html>"
            self.wfile.write(output)
            return
        else:
            self.send_error(404, 'File Not Found: %s' % self.path)

    def do_POST(self):
        try:
            if self.path.endswith("/restaurants/new"):
                self.send_response(301)
                self.send_header('Content-type', 'text/html')
                self.send_header('Location', '/restaurants')
                self.end_headers()
                ctype, pdict = cgi.parse_header(
                    self.headers.getheader('content-type'))
                if ctype == 'multipart/form-data':
                    fields = cgi.parse_multipart(self.rfile, pdict)
                    messagecontent = fields.get('newRestaurantName')
                newRestaurant = Restaurant(name = messagecontent[0])
                session.add(newRestaurant)
                session.commit()
                self.wfile.write(output)
                
            if self.path.endswith("/edit"):
                path = self.path.split('/')
                index = path[2]
                ctype, pdict = cgi.parse_header(
                    self.headers.getheader('content-type'))
                if ctype == 'multipart/form-data':
                    fields = cgi.parse_multipart(self.rfile, pdict)
                    messagecontent = fields.get('updateName')
                updatedName = session.query(Restaurant).filter_by(id = index).one()
                if updatedName != []:
                    updatedName.name = messagecontent[0]
                    session.add(updatedName)
                    session.commit()
                    self.send_response(301)
                    self.send_header('Content-type', 'text/html')
                    self.send_header('Location', '/restaurants')
                    self.end_headers()
                self.wfile.write(output)

            if self.path.endswith("/delete"):
                path = self.path.split('/')
                index = path[2]
                ctype, pdict = cgi.parse_header(
                    self.headers.getheader('content-type'))
                if ctype == 'multipart/form-data':
                    fields = cgi.parse_multipart(self.rfile, pdict)
                    messagecontent = fields.get('updateName')
                deleteRestaurant = session.query(Restaurant).filter_by(id = index).one()
                if deleteRestaurant != []:
                    session.delete(deleteRestaurant)
                    session.commit()
                    self.send_response(301)
                    self.send_header('Content-type', 'text/html')
                    self.send_header('Location', '/restaurants')
                    self.end_headers()
                self.wfile.write(output)
        except:
            pass

def main():
    try:
        port = 8000
        server = HTTPServer(('', port), WebServerHandler)
        print "Web Server running on port %s" % port
        server.serve_forever()
    except KeyboardInterrupt:
        print " ^C entered, stopping web server...."
        server.socket.close()

if __name__ == '__main__':
    main()
