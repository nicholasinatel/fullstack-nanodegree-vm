from flask import Flask 
app = Flask(__name__)

# Decorator in Python
# Wraps our function inside the app.route function that Flask has already created
# Call the functions that follows it whenever a request with a URL that matches its argument
# In this case / or /hello invokes HelloWorld() function
@app.route('/') # Useful for routing non existing routes to the root page
@app.route('/hello')
def HelloWorld():
    return "Hello World"

if __name__ == '__main__': # if it is executed directly from the python interpreter and not used as imported module
    app.debug = True # With Debug the Server reRun itself always the code changes
    app.run(host = '0.0.0.0', port = 5000) # Server Publicly Available
    # 0.0.0.0 Tells to listen on all IP Addresses