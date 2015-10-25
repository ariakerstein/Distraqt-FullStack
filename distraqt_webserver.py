from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import cgi

# import CRUD Operations from Lesson 1
from distraqt_database_setup import Base, Distraqt
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Create session and connect to DB
# engine = create_engine('sqlite:///restaurantmenu.db')
engine = create_engine('sqlite:///distraqt.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

class webServerHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        try:
            if self.path.endswith("/distraqt/new"):
                #test js to include timer 
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                output = ""
                output += "<html><body>"
                # output += "<h1>Distraqt will help you achieve deliberate practice, have fun and flow.</h1>"
                output += "<h1>What will you work on?</h1>"
                output += "<form method = 'POST' enctype='multipart/form-data' id = 'flowNow' action = '/distraqt/new'>"
                output += "<input name = 'newFlowBlock' type = 'text' placeholder = 'What will you flow on?' > "
                output += "<input type='submit' value='Create'>"
                output += "</form></body></html>"
                self.wfile.write(output)
                return


            if self.path.endswith("/distraqt"):
                distraqts = session.query(Distraqt).all()
                output = ""
                # Distraqt test
                output += "<h1>Distraqt</h1>"
        # <!--<p>Distraqt will help you achieve your goals and enjoy yourself in the process.</p>-->
                output += "<p>Play your work. Achieve flow.</p>"
                output += "<a href = '/distraqt/new' > Generate a New flow Block Here </a></br>"

                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                output += "<html><body>"
                for distraqt in distraqts:
                    output += distraqt.block
                    output += "</br>"
                    # Objective 2 -- Add Edit and Delete Links
                    output += "<a href ='#' >Edit </a> "
                    output += "</br>"
                    output += "<a href =' #'> Delete </a>"
                    output += "</br></br>"

                output += "</body></html>"
                self.wfile.write(output)
                return

            if self.path.endswith("/edit"):
                restaurantIDPath = self.path.split("/")[2]
                myRestaurantQuery = session.query(Distraqt).filter_by(
                    id=restaurantIDPath).one()
                if myRestaurantQuery:
                    self.send_response(200)
                    self.send_header('Content-type', 'text/html')
                    self.end_headers()
                    output = "<html><body>"
                    output += "<h1>"
                    output += myRestaurantQuery.name
                    output += "</h1>"
                    output += "<form method='POST' enctype='multipart/form-data' action = '/distraqt/%s/edit' >" % restaurantIDPath
                    output += "<input name = 'newRestaurantName' type='text' placeholder = '%s' >" % myRestaurantQuery.name
                    output += "<input type = 'submit' value = 'Rename'>"
                    output += "</form>"
                    output += "</body></html>"

                    self.wfile.write(output)
            if self.path.endswith("/delete"):
                restaurantIDPath = self.path.split("/")[2]

                myRestaurantQuery = session.query(Restaurant).filter_by(
                    id=restaurantIDPath).one()
                if myRestaurantQuery:
                    self.send_response(200)
                    self.send_header('Content-type', 'text/html')
                    self.end_headers()
                    output = ""
                    output += "<html><body>"
                    output += "<h1>Are you sure you want to delete %s?" % myRestaurantQuery.name
                    output += "<form method='POST' enctype = 'multipart/form-data' action = '/restaurants/%s/delete'>" % restaurantIDPath
                    output += "<input type = 'submit' value = 'Delete'>"
                    output += "</form>"
                    output += "</body></html>"
                    self.wfile.write(output)        


        except IOError:
            self.send_error(404, 'File Not Found: %s' % self.path)

    # Objective 3 Step 3- Make POST method
    def do_POST(self):
        try:


            if self.path.endswith("/distraqt/new"):
                ctype, pdict = cgi.parse_header(
                    self.headers.getheader('content-type'))
                if ctype == 'multipart/form-data':
                    fields = cgi.parse_multipart(self.rfile, pdict)
                    messagecontent = fields.get('newFlowBlock')

                    # Create new Distraqt Object
                    newDistraqt = Distraqt(block=messagecontent[0])
                    session.add(newDistraqt)
                    session.commit()

                    self.send_response(301)
                    self.send_header('Content-type', 'text/html')
                    #redirect on submit to /restaurants
                    self.send_header('Location', '/distraqt')
                    self.end_headers()

            if self.path.endswith("/delete"):
                restaurantIDPath = self.path.split("/")[2]
                myRestaurantQuery = session.query(Restaurant).filter_by(
                    id=restaurantIDPath).one()
                if myRestaurantQuery:
                    session.delete(myRestaurantQuery)
                    session.commit()
                    self.send_response(301)
                    self.send_header('Content-type', 'text/html')
                    self.send_header('Location', '/restaurants')
                    self.end_headers()

            if self.path.endswith("/edit"):
                ctype, pdict = cgi.parse_header(
                    self.headers.getheader('content-type'))
                if ctype == 'multipart/form-data':
                    fields = cgi.parse_multipart(self.rfile, pdict)
                    messagecontent = fields.get('newRestaurantName')
                    restaurantIDPath = self.path.split("/")[2]

                    myRestaurantQuery = session.query(Restaurant).filter_by(
                        id=restaurantIDPath).one()
                    if myRestaurantQuery != []:
                        myRestaurantQuery.name = messagecontent[0]
                        session.add(myRestaurantQuery)
                        session.commit()
                        self.send_response(301)
                        self.send_header('Content-type', 'text/html')
                        self.send_header('Location', '/restaurants')
                        self.end_headers()

        except:
            pass


            # if self.path.endswith("/edit"):
            #     ctype, pdict = cgi.parse_header(
            #         self.headers.getheader('content-type'))
            #     if ctype == 'multipart/form-data':
            #         fields = cgi.parse_multipart(self.rfile, pdict)
            #         messagecontent = fields.get('newRestaurantName')
            #         restaurantIDPath = self.path.split("/")[2]

            #         myRestaurantQuery = session.query(Restaurant).filter_by(
            #             id=restaurantIDPath).one()
            #         if myRestaurantQuery != []:
            #             myRestaurantQuery.name = messagecontent[0]
            #             session.add(myRestaurantQuery)
            #             session.commit()
            #             self.send_response(301)
            #             self.send_header('Content-type', 'text/html')
            #             self.send_header('Location', '/restaurants')
            #             self.end_headers()

            # if self.path.endswith("/restaurants/new"):
            #     ctype, pdict = cgi.parse_header(
            #         self.headers.getheader('content-type'))
            #     if ctype == 'multipart/form-data':
            #         fields = cgi.parse_multipart(self.rfile, pdict)
            #         messagecontent = fields.get('newRestaurantName')

            #         # Create new Restaurant Object
            #         newRestaurant = Restaurant(name=messagecontent[0])
            #         session.add(newRestaurant)
            #         session.commit()

            #         self.send_response(301)
            #         self.send_header('Content-type', 'text/html')
            #         #redirect on submit to /restaurants
            #         self.send_header('Location', '/restaurants')
            #         self.end_headers()


                    # # Create new Restaurant Object
                    # newRestaurant = Restaurant(name=messagecontent[0])
                    # session.add(newRestaurant)
                    # session.commit()

                    # self.send_response(301)
                    # self.send_header('Content-type', 'text/html')
                    # #redirect on submit to /restaurants
                    # self.send_header('Location', '/restaurants')
                    # self.end_headers()


            # if self.path.endswith("/restaurants"):
            #     ctype, pdict = cgi.parse_header(
            #         self.headers.getheader('content-type'))
            #     if ctype == 'multipart/form-data':
            #         fields = cgi.parse_multipart(self.rfile, pdict)
            #         messagecontent = fields.get('newRestaurantName')

            #         # Create new Restaurant Object
            #         newRestaurant = Restaurant(name=messagecontent[0])
            #         session.add(newRestaurant)
            #         session.commit()

            #         self.send_response(301)
            #         self.send_header('Content-type', 'text/html')
            #         #redirect on submit to /restaurants
            #         self.send_header('Location', '/restaurants')
            #         self.end_headers()
                

def main():
    try:
        server = HTTPServer(('', 8081), webServerHandler)
        print 'Web server running... Open localhost:8081/distraqt in your browser'
        server.serve_forever()
    except KeyboardInterrupt:
        print '^C received, shutting down server'
        server.socket.close()

if __name__ == '__main__':
    main()
