# https://docs.python.org/2/library/basehttpserver.html
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import cgi  # CommonGatewayInterface

# Handler Class - What code to execute based on the type of request
# Extending the class WebServerHandler from the class BaseHTTPRequestHandler


class WebServerHandler(BaseHTTPRequestHandler):
    def do_GET(self):  # Use pattern looking for the end of the path
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
            print message
            return
        if self.path.endswith("/hola"):
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            message = ""
            message += "<html><body>"
            message += "<h1>&#161 Hola !</h1>"
            message += '''<form method='POST' enctype='multipart/form-data' action='/hello'><h2>What would you like me to say?</h2><input name="message" type="text" ><input type="submit" value="Submit"> </form>'''
            message += "</body></html>"
            self.wfile.write(message)
            print message
            return
        else:
            self.send_error(404, 'File Not Found: %s' % self.path)

    def do_POST(self):
        try:
            self.send_response(301)
            self.send_header('Content-type', 'text/html')
            self.end_headers()

            # Parse a HTML form header into a main value and dictionary of parameters
            ctype, pdict = cgi.parse_header(
                self.headers.getheader('content-type'))
            if ctype == 'multipart/form-data':  # check if this is form data being received
                # collect all the fields in a form
                fields = cgi.parse_multipart(self.rfile, pdict)
                # get a value of a specific field or set of fields
                messagecontent = fields.get('message')

                output = ""
                output += "<html><body>"
                output += " <h2> Okay, how about this: </h2>"
                # Return the first value of the array submitted in the form
                output += "<h1> %s </h1>" % messagecontent[0]
                output += '''<form method='POST' enctype='multipart/form-data' action='/hello'><h2>What would you like me to say?</h2><input name="message" type="text" ><input type="submit" value="Submit"> </form>'''
                output += "</body></html>"

                self.wfile.write(output)
                print output
        except:
            pass
            
# Main Method - Instantiate Server/Specify port to listen
def main():
    # Try to start the server
    try:
        port = 8080
        # HTTPServer(serverAddres, RequestHandler)
        #serverAddress a tuple with host and port number
        server = HTTPServer(('', port), WebServerHandler)
        print "Web Server running on port %s" % port
        server.serve_forever()  # Keep it constantly listening until CTRL C
    # Stop if CTRL C
    except KeyboardInterrupt:
        print " ^C entered, stopping web server...."
        server.socket.close()


# Execute main method when executed script
if __name__ == '__main__':
    main()
