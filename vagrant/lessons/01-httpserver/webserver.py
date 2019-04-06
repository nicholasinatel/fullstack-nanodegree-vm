# https://docs.python.org/2/library/basehttpserver.html
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import cgi  # CommonGatewayInterface
import crud


# Handler Class - What code to execute based on the type of request
# Extending the class WebServerHandler from the class BaseHTTPRequestHandler


class WebServerHandler(BaseHTTPRequestHandler):
    def do_GET(self):  # Use pattern looking for the end of the path
        # ROOT ROUTE
        if self.path.endswith("/"):
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            message = "<h1>Hello!</h1>"
            message += "<h1>Hello!</h1>"
            message += "<ul>"
            message += '<li><a href="http://localhost:8080/hello">Hello</a></li>'
            message += '<li><a href="http://localhost:8080/restaurants">Restaurants</a></li>'
            message += "</ul>"
            self.wfile.write(message)
            return
        # HELLO ROUTE
        if self.path.endswith("/hello"):
            self.send_response(200)  # Response code
            # Indicate that im replying with text in the form of html to the client
            self.send_header('Content-type', 'text/html')
            self.end_headers()  # Sends blank line, indicating the end of response
            message = ""
            message += "<h1>Hello!</h1>"
            message += '''<form method='POST' enctype='multipart/form-data' action='/hello'><h2>What would you like me to say?</h2><input name="message" type="text" ><input type="submit" value="Submit"> </form>'''
            message += "</body></html>"
            self.wfile.write(message)  # Send the message built to the client
            print(message)  # Handy for debugging
            return
        # RESTAURANTS ROUTE
        if self.path.endswith("/restaurants"):
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            session = crud.connect()
            results = crud.listAll(session)
            message = ""
            message += "<html><body><style>a { color: blue;} a:hover{cursor: pointer;} p {margin-bottom: 0;}</style>"
            message += "<a href= '/restaurants/new'> Make a New Restaurant Here</a></br></br>"
            message += "<h1> Restaurant List </h1>"
            for result in results:
                message += "<p>"
                message += result.name
                message += "</p>"
                # print("result.id: ", result.id)
                message += '<a href="http://localhost:8080/%s/edit">Edit</a>' % result.id
                message += "<br>"
                message += '<a href="http://localhost:8080/%s/delete">Delete</a>' % result.id
            message += "</body></html>"
            self.wfile.write(message)
            print(message)
            return
        # NEW RESTAURANT ROUTE
        if self.path.endswith("/restaurants/new"):
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            message = ""
            message += "<html><body>"
            message += "<h1> Make a new Restaurant </h1>"
            message += "<form method='POST' enctype='multipart/form-data' action='/restaurants/new'>"
            message += "<input name='newRestaurantName' type='text' placeholder='New Restaurant Name'>"
            message += "<input type='submit' value='Create'>"
            message += "</form></body></html>"
            self.wfile.write(message)
            return
        # EDIT ROUTE
        if self.path.endswith("/edit"):
            restaurantIDPath = self.path.split("/")[1]
            print("restaurantIDPath: ", restaurantIDPath)
            session = crud.connect()
            myRestaurantQuery = crud.listOne(session, restaurantIDPath)
            # session.query(Restaurant).filter_by( id = restaurantIDPath).one()
            if myRestaurantQuery != []:
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                output = "<html><body>"
                output += "<h1>"
                output += myRestaurantQuery.name
                output += "</h1>"
                output += "<form method='POST' enctype='multipart/form-data' action='/restaurants/%s/edit'>" % restaurantIDPath
                output += "<input name = 'newRestaurantName' type='text' placeholder = '%s' >" % myRestaurantQuery.name
                output += "<input type= 'submit' value='Rename'>"
                output += "</form></body></html>"
                self.wfile.write(output)
            return
        # DELETE ONE RESTAURANT ROUTE
        if self.path.endswith("/delete"):
            restaurantIDPath = self.path.split("/")[1]
            print("restaurantIDPath: ", restaurantIDPath)
            session = crud.connect()
            myRestaurantQuery = crud.listOne(session, restaurantIDPath)
            if myRestaurantQuery != []:
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                output = "<html><body>"
                output += "<h1>Are you sure you want to delete %s?" % myRestaurantQuery.name + "</h1>"
                output += "<form method='POST' enctype='multipart/form-data' action='/restaurants/%s/delete'>" % restaurantIDPath
                output += "<input type= 'submit' value='DELETE'>"
                output += "</form></body></html>"
                self.wfile.write(output)
            return
        else:
            self.send_error(404, 'File Not Found: %s' % self.path)

    def do_POST(self):
        try:
            # DELETE RESTAURANT ROUTE
            if self.path.endswith("delete"):
                restaurantIDPath = self.path.split("/")[2]
                session = crud.connect()
                crud.deleteOne(session, restaurantIDPath)
                self.send_response(301)
                self.send_header('Content-type', 'text/html')
                self.send_header('Location', '/restaurants')
                self.end_headers()
            # EDIT RESTAURANT ROUTE
            if self.path.endswith("edit"):
                # Grab the input from the form
                ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
                if ctype == 'multipart/form-data':
                    fields = cgi.parse_multipart(self.rfile, pdict)
                    messagecontent = fields.get('newRestaurantName')  
                    restaurantIDPath = self.path.split("/")[2]
                    # Query for the object withe the matching ID
                    session = crud.connect()
                    # myRestaurantQuery = crud.listOne(session, "id", restaurantIDPath)
                    # Change name Field for the message content grabbed from the header
                    # if myRestaurantQuery != []:
                    crud.updateOne(session, restaurantIDPath, messagecontent[0])
                    # myRestaurantQuery.name = messagecontent[0]
                    self.send_response(301)
                    self.send_header('Content-type', 'text/html')
                    self.send_header('Location', '/restaurants')
                    self.end_headers()
            # CREATE NEW RESTAURANT ROUTE
            if self.path.endswith("/restaurants/new"):
                print("POST method sequence init")
                #cgi parses's post request headers
                # Parse a HTML form header into a main value and dictionary of parameters
                ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
                print("ctype: ", ctype)
                print("pdict: ", pdict)
                if ctype == 'multipart/form-data':
                    fields = cgi.parse_multipart(self.rfile, pdict)
                    messagecontent = fields.get('newRestaurantName')
                    session = crud.connect()
                    print("session: ", session)
                    flag = crud.create(session, messagecontent[0])# Create new Restaurant Class
                    if(flag == True):
                        self.send_response(301)
                        self.send_header('Content-type', 'text/html')
                        self.send_header('Location', '/restaurants')
                        self.end_headers()

                return

            # self.send_response(301)
            # self.send_header('Content-type', 'text/html')
            # self.end_headers()
            # # Parse a HTML form header into a main value and dictionary of parameters
            # ctype, pdict = cgi.parse_header(
            #     self.headers.getheader('content-type'))
            # if ctype == 'multipart/form-data':  # check if this is form data being received
            #     # collect all the fields in a form
            #     fields = cgi.parse_multipart(self.rfile, pdict)
            #     # get a value of a specific field or set of fields
            #     messagecontent = fields.get('message')

            #     output = ""
            #     output += "<html><body>"
            #     output += " <h2> Okay, how about this: </h2>"
            #     # Return the first value of the array submitted in the form
            #     output += "<h1> %s </h1>" % messagecontent[0]
            #     output += '''<form method='POST' enctype='multipart/form-data' action='/hello'><h2>What would you like me to say?</h2><input name="message" type="text" ><input type="submit" value="Submit"> </form>'''
            #     output += "</body></html>"

            #     self.wfile.write(output)
            #     print output
        except:
            self.send_error(400, 'Bad Request: %s' % self.path)


# Main Method - Instantiate Server/Specify port to listen
def main():
    # Try to start the server
    try:
        port = 8080
        # HTTPServer(serverAddres, RequestHandler)
        #serverAddress a tuple with host and port number
        server = HTTPServer(('', port), WebServerHandler)
        print("Web Server running on port %s" % port)
        server.serve_forever()  # Keep it constantly listening until CTRL C
    # Stop if CTRL C
    except KeyboardInterrupt:
        print(" ^C entered, stopping web server....")
        server.socket.close()


# Execute main method when executed script
if __name__ == '__main__':
    main()
