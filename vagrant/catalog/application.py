# Flask
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, make_response
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy import create_engine
# DB
from db_setup import Base, Category, Item, Rentability, User
# Python
import random
import string
import httplib2
import json
# OAuth
from flask import session as login_session

from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError

from google.oauth2 import id_token
from google.auth.transport import requests

engine = create_engine('sqlite:///catalog.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

app = Flask(__name__)
# OAuth
CLIENT_ID = json.loads(
    open('client_secrets.json', 'r').read())['web']['client_id']

APPLICATION_NAME = "Financial Wallet"

# -------------------------------------------------------------------------------
# Login Routes And Functions


@app.route('/login')
def showLogin():
    state = ''.join(random.choice(string.ascii_uppercase + string.
                                  digits)for x in range(32))
    login_session['state'] = state
    return render_template('login.html', STATE=state)
    # Render The Login Template
    # return "The current session state is %s" % login_session['state']

# -------------------------------------------------------------------------------
# Google Auth Routes


@app.route('/gconnect', methods=['POST'])
def gconnect():
    # Validate state token
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Obtain authorization code
    token = request.data

    try:
        # Specify the CLIENT_ID of the app that accesses the backend:
        idinfo = id_token.verify_oauth2_token(token, requests.Request(), CLIENT_ID)
        # print "idinfo: %s" % idinfo
        # Or, if multiple clients access the backend server:
        # idinfo = id_token.verify_oauth2_token(token, requests.Request())
        # if idinfo['aud'] not in [CLIENT_ID_1, CLIENT_ID_2, CLIENT_ID_3]:
        #     raise ValueError('Could not verify audience.')

        if idinfo['iss'] not in ['accounts.google.com', 'https://accounts.google.com']:
            raise ValueError('Wrong issuer.')

        # If auth request is from a G Suite domain:
        # if idinfo['hd'] != GSUITE_DOMAIN_NAME:
        #     raise ValueError('Wrong hosted domain.')

        # ID token is valid. Get the user's Google Account ID from the decoded token.
        userid = idinfo['sub']
        # print "userid: %s" % userid
        access_token = token
        gplus_id = userid
    except ValueError:
        # Invalid token
        pass

    # Verify that the access token is valid for this app.
    if idinfo['aud'] != CLIENT_ID:
        print CLIENT_ID
        response = make_response(
            json.dumps("Token's client ID does not match app's."), 401)
        print "Token's client ID does not match app's."
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify For Current User Already Connected
    stored_access_token = login_session.get('access_token')
    print "stored_access_token: %s " % stored_access_token
    stored_gplus_id = login_session.get('gplus_id')
    if stored_access_token is not None and gplus_id == stored_gplus_id:
        response = make_response(json.dumps(
            'Current user is already connected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        print "Watchout for Bugs - Current user is already Connected"
        # return response

    # Store the access token in the session for later use.
    login_session['access_token'] = access_token
    login_session['gplus_id'] = gplus_id
    # User Info
    login_session['username'] = idinfo['name']
    login_session['picture'] = idinfo['picture']
    login_session['email'] = idinfo['email']

    # ADD PROVIDER TO LOGIN SESSION
    login_session['provider'] = 'google'

    # Check for existing User
    user_id = getUserID(idinfo["email"])
    if not user_id:
        print "if not user_id????"
        user_id = createUser(login_session)
    login_session['user_id'] = user_id

    print "login_session[user_id]: %s" % login_session['user_id']

    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']
    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += ' " style = "width: 300px; height: 300px;border-radius: 150px;-webkit-border-radius: 150px;-moz-border-radius: 150px;"> '
    flash("you are now logged in as %s" % login_session['username'])
    print "done!"
    return output


@app.route('/gdisconnect')
def gdisconnect():
    requests.disconnect()
    # # Grab the credentials from login_session i.e Only disconnect a connected user.
    # access_token = login_session.get('access_token')
    # # If credentials is empty = No User
    # if access_token is None:
    #     response = make_response(
    #         json.dumps('Current user not connected.'), 401)
    #     response.headers['Content-Type'] = 'application/json'
    #     return response
    # url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % access_token
    # h = httplib2.Http()
    # result = h.request(url, 'GET')[0]
    # if result['status'] == '200':
    #     response = make_response(json.dumps('Successfully disconnected.'), 200)
    #     response.headers['Content-Type'] = 'application/json'
    #     return response
    # else:
    #     response = make_response(json.dumps(
    #         'Failed to revoke token for given user.', 400))
    #     response.headers['Content-Type'] = 'application/json'
    # return response

# -------------------------------------------------------------------------------
# User Helper Functions


def createUser(login_session):
    newUser = User(name=login_session['username'], email=login_session[
                   'email'], picture=login_session['picture'])
    session.add(newUser)
    session.commit()
    user = session.query(User).filter_by(email=login_session['email']).one()
    return user.id


def getUserInfo(user_id):
    user = session.query(User).filter_by(id=user_id).one()
    return user


def getUserID(email):
    try:
        user = session.query(User).filter_by(email=email).one()
        return user.id
    except:
        return None


# -------------------------------------------------------------------------------------------------
# FB Connection API
@app.route('/fbconnect', methods=['POST'])
def fbconnect():
    if request.args.get('state') != login_session['state']:
        print "BIG FAIL HAPPENING"
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    access_token = request.data
    print "access token received %s " % access_token
    # Exchange client token for long-lived server-side token with
    # GET /oauth/acces_token?grant_type=fb_exchange_token&client_id={app-id}&client_secret={app-secret}&fb_exchange_token={short-lived-token}
    app_id = json.loads(open('fb_client_secrets.json', 'r').read())[
        'web']['app_id']
    app_secret = json.loads(open('fb_client_secrets.json', 'r').read())[
        'web']['app_secret']
    url = 'https://graph.facebook.com/oauth/access_token?grant_type=fb_exchange_token&client_id=%s&client_secret=%s&fb_exchange_token=%s' % (
        app_id, app_secret, access_token)
    h = httplib2.Http()
    result = h.request(url, 'GET')[1]
    print "result from request"
    print result
    # Use token to get user info from API
    userinfo_url = "https://graph.facebook.com/v3.2/me"
    '''
        Due to the formatting for the result from the server token exchange we have to
        split the token first on commas and select the first index which gives us the key : value
        for the server access token then we split it on colons to pull out the actual token value
        and replace the remaining quotes with nothing so that it can be used directly in the graph
        api calls
    '''
    token = result.split(',')[0].split(':')[1].replace('"', '')

    print "token: %s" % token
    url = 'https://graph.facebook.com/v3.2/me?access_token=%s&fields=name,id,email' % token
    h = httplib2.Http()
    result = h.request(url, 'GET')[1]
    print "url sent for API access:%s" % url
    print "API JSON result: %s" % result
    data = json.loads(result)
    print "data: %s" % data
    login_session['provider'] = 'facebook'
    login_session['username'] = data["name"]
    login_session['email'] = data["email"]
    login_session['facebook_id'] = data["id"]

    # The token must be stored in the login_session in order to properly logout
    login_session['access_token'] = token

    # Get User Picture
    url = 'https://graph.facebook.com/v3.2/me/picture?access_token=%s&redirect=0&height=200&width=200' % token
    h = httplib2.Http()
    result = h.request(url, 'GET')[1]
    data = json.loads(result)

    login_session['picture'] = data["data"]["url"]

    # see if user exists
    user_id = getUserID(login_session['email'])
    if not user_id:
        user_id = createUser(login_session)
    login_session['user_id'] = user_id

    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']

    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += ' " style = "width: 300px; height: 300px;border-radius: 150px;-webkit-border-radius: 150px;-moz-border-radius: 150px;"> '

    flash("Now logged in as %s" % login_session['username'])
    return output


@app.route('/fbdisconnect')
def fbdisconnect():
    facebook_id = login_session['facebook_id']
    # The access token must me included to successfully logout
    access_token = login_session['access_token']
    url = 'https://graph.facebook.com/%s/permissions?access_token=%s' % (
        facebook_id, access_token)
    h = httplib2.Http()
    result = h.request(url, 'DELETE')[1]
    return "you have been logged out"
# ---------------------------------------------------------
# Disconnect based on provider
@app.route('/disconnect')
def disconnect():
    if 'provider' in login_session:
        if login_session['provider'] == 'google':
            del login_session['gplus_id']
            del login_session['access_token']
        if login_session['provider'] == 'facebook':
            fbdisconnect()
            del login_session['facebook_id']
        del login_session['username']
        del login_session['email']
        del login_session['picture']
        del login_session['user_id']
        del login_session['provider']
        flash("You have successfully been logged out.")
        return redirect(url_for('showCategories'))
    else:
        flash("You were not logged in")
        return redirect(url_for('showCategories'))

# ---------------------------------------------------------------
# Category Routes
@app.route('/')
@app.route('/category')
def showCategories():
    if 'username' not in login_session:
        categories = session.query(Category).all()
        return render_template('public_category.html', categories=categories)
    else:
        categories = session.query(Category).filter_by(user_id=login_session['user_id'])
        return render_template('category.html', categories=categories, username=login_session['username'])

# API Endpoint
@app.route('/category/JSON')
def showCategoriesJSON():
    categories = session.query(Category).all()
    return jsonify(categories=[c.serialize for c in categories])


@app.route('/category/new', methods=['GET', 'POST'])
def newCategory():
    if 'username' not in login_session:
        return redirect('/login')
    if request.method == 'GET':
        return render_template('new_category.html')
    elif request.method == 'POST':
        nova_category = Category(
            name=request.form['name'], 
            description=request.form['description'], 
            user_id=login_session['user_id'])
        session.add(nova_category)
        flash('New Wallet %s Successfully Created' % nova_category.name)
        session.commit()
        return redirect(url_for('showCategories'))


@app.route('/category/<int:category_id>/edit', methods=['GET', 'POST'])
def editCategory(category_id):
    if 'username' not in login_session:
        return redirect('/login')
    category_edit = session.query(Category).filter_by(id=category_id).one()
    if category_edit.user_id != login_session['user_id']:
        return "<script>function myFunction() {alert('You are not authorized to edit this category.');}</script><body onload='myFunction()''>"
    if request.method == 'GET':
        return render_template('edit_category.html', category_edit=category_edit)
    elif request.method == 'POST':
        category_edit.name = request.form['name']
        category_edit.description = request.form['description']
        session.add(category_edit)
        flash('Wallet %s Successfully Edited' % category_edit.name)
        session.commit()
        return redirect(url_for('showCategories'))


@app.route('/category/<int:category_id>/delete', methods=['GET', 'POST'])
def deleteCategory(category_id):
    if 'username' not in login_session:
        return redirect('/login')
    category_delete = session.query(Category).filter_by(id=category_id).one()
    if category_delete.user_id != login_session['user_id']:
        return "<script>function myFunction() {alert('You are not authorized to delete this category.');}</script><body onload='myFunction()''>"
    if request.method == 'GET':
        return render_template('delete_category.html', category_delete=category_delete)
    elif request.method == 'POST':
        session.delete(category_delete)
        flash('Wallet %s Successfully Deleted' % category_delete.name)
        session.commit()
        return redirect(url_for('showCategories'))

# ---------------------------------------------------------------
# ItemS Routes
@app.route('/category/<int:category_id>/')
@app.route('/category/<int:category_id>/item')
def showItem(category_id):
    if ('username' not in login_session):
        category = session.query(Category).filter_by(id=category_id).one()
        items = session.query(Item).filter_by(category_id=category_id)
        return render_template('public_item.html', category=category, items=items)
    else:
        category = session.query(Category).filter_by(id=category_id, user_id=login_session['user_id']).one()
        creator = getUserInfo(category.user_id)
        items = session.query(Item).filter_by(category_id=category_id, user_id=login_session['user_id']).all()
        return render_template('item.html', category=category, items=items, username=login_session['username'])

# API Endpoint
@app.route('/category/<int:category_id>/JSON')
@app.route('/category/<int:category_id>/item/JSON')
def showItemJSON(category_id):
    category = session.query(Category).filter_by(id=category_id).one()
    items = session.query(Item).filter_by(category_id=category.id)
    return jsonify(Actives=[i.serialize for i in items])


@app.route('/category/<int:category_id>/item/new', methods=['GET', 'POST'])
def newItem(category_id):
    if 'username' not in login_session:
        return redirect('/login')
    if request.method == 'GET':
        return render_template('new_item.html')
    elif request.method == 'POST':
        novo_item = Item(name=request.form['name'],
                         active=request.form['active'],
                         dy=request.form['dy'],
                         price=request.form['price'],
                         description=request.form['description'],
                         category_id=category_id,
                         user_id=login_session['user_id'])
        session.add(novo_item)
        flash('New Active %s Successfully Created' % novo_item.name)
        session.commit()
        return redirect(url_for('showItem', category_id=category_id))


@app.route('/category/<int:category_id>/item/<int:item_id>/edit', methods=['GET', 'POST'])
def editItem(category_id, item_id):
    if 'username' not in login_session:
        return redirect('/login') 
    item_edit = session.query(Item).filter_by(id=item_id).first()
    if item_edit.user_id != login_session['user_id']:
        return "<script>function myFunction() {alert('You are not authorized to edit this item.');}</script><body onload='myFunction()''>"
    if request.method == 'GET':
        return render_template('edit_item.html', category_id=category_id, item_edit=item_edit)
    elif request.method == 'POST':
        item_edit.name = request.form['name']
        item_edit.active = request.form['active']
        item_edit.dy = request.form['dy']
        item_edit.price = request.form['price']
        item_edit.description = request.form['description']
        session.add(item_edit)
        flash('Active %s Successfully Edited' % item_edit.name)
        session.commit()
        return redirect(url_for('showItem', category_id=category_id))


@app.route('/category/<int:category_id>/item/<int:item_id>/delete', methods=['GET', 'POST'])
def deleteItem(category_id, item_id):
    if 'username' not in login_session:
        return redirect('/login') 
    item_delete = session.query(Item).filter_by(id=item_id).first()
    if item_delete.user_id != login_session['user_id']:
        return "<script>function myFunction() {alert('You are not authorized to delete this item.');}</script><body onload='myFunction()''>"
    if request.method == 'GET':
        return render_template('delete_item.html', category_id=category_id, item_delete=item_delete)
    elif request.method == 'POST':
        session.delete(item_delete)
        flash('Active %s Successfully Deleted' % item_delete.name)
        session.commit()
        return redirect(url_for('showItem', category_id=category_id))

# Item API EndPoint Route


@app.route('/category/<int:category_id>/item/JSON')
@app.route('/category/<int:category_id>/item/<int:item_id>/JSON')
def showSingleItemJSON(category_id, item_id):
    item = session.query(Item).filter_by(id=item_id).one()
    return jsonify(item=item.serialize)

# ---------------------------------------------------------------
# Rentability Routes
# API Endpoint


@app.route('/category/<int:category_id>/item/<int:item_id>/rentability/JSON')
def showRentabilityJSON(category_id, item_id):
    rendas = session.query(Rentability).filter_by(item_id=item_id)
    return jsonify(Rentabilities=[r.serialize for r in rendas])


@app.route('/category/<int:category_id>/item/<int:item_id>/rentability/<int:rentability_id>/JSON')
def showSingleRentabilityJSON(category_id, item_id, rentability_id):
    renda = session.query(Rentability).filter_by(id=rentability_id).one()
    return jsonify(Renda=renda.serialize)


@app.route('/category/<int:category_id>/item/<int:item_id>')
@app.route('/category/<int:category_id>/item/<int:item_id>/rentability')
def showRentability(category_id, item_id):
    if ('username' not in login_session):
        category = session.query(Category).filter_by(id=category_id).one()
        item = session.query(Item).filter_by(id=item_id).first()
        rendas = session.query(Rentability).filter_by(item_id=item_id)
        return render_template('public_rentability.html', category=category, item=item, rendas=rendas)
    else:
        category = session.query(Category).filter_by(id=category_id, user_id=login_session['user_id']).one()
        item = session.query(Item).filter_by(id=item_id, user_id=login_session['user_id']).first()
        rendas = session.query(Rentability).filter_by(item_id=item_id, user_id=login_session['user_id']).all()
        return render_template('rentability.html', category=category, item=item, rendas=rendas, username=login_session['username'])
        


@app.route('/category/<int:category_id>/item/<int:item_id>/rentability/new', methods=['GET', 'POST'])
def newRentability(category_id, item_id):
    if 'username' not in login_session:
        return redirect('/login')
    if request.method == 'GET':
        return render_template('new_rentability.html', category_id=category_id, item_id=item_id)
    elif request.method == 'POST':
        money = float(request.form['money'])
        percent = float(request.form['percent'])
        novo_rentability = Rentability(month=request.form['month'],
                                       money=money,
                                       percent=percent,
                                       item_id=item_id,
                                       user_id=login_session['user_id'])
        session.add(novo_rentability)
        flash('New Rentability %s Successfully Created' %
              novo_rentability.month)
        session.commit()
        return redirect(url_for('showRentability', category_id=category_id, item_id=item_id))


@app.route('/category/<int:category_id>/item/<int:item_id>/rentability/<int:rentability_id>/edit', methods=['GET', 'POST'])
def editRentability(category_id, item_id, rentability_id):
    if 'username' not in login_session:
        return redirect('/login') 
    rentability_edit = session.query(
        Rentability).filter_by(id=rentability_id).first()
    if rentability_edit.user_id != login_session['user_id']:
        return "<script>function myFunction() {alert('You are not authorized to edit this rentability.');}</script><body onload='myFunction()''>"
    if request.method == 'GET':
        return render_template('edit_rentability.html', category_id=category_id, item_id=item_id, rentability_edit=rentability_edit)
    elif request.method == 'POST':
        rentability_edit.month = request.form['month']
        rentability_edit.money = float(request.form['money'])
        rentability_edit.percent = float(request.form['percent'])
        session.add(rentability_edit)
        flash('Rentability %s Successfully Edited' % rentability_edit.month)
        session.commit()
        return redirect(url_for('showRentability', category_id=category_id, item_id=item_id))


@app.route('/category/<int:category_id>/item/<int:item_id>/rentability/<int:rentability_id>/delete', methods=['GET', 'POST'])
def deleteRentability(category_id, item_id, rentability_id):
    if 'username' not in login_session:
        return redirect('/login') 
    rentability_delete = session.query(
        Rentability).filter_by(id=rentability_id).first()
    if rentability_delete.user_id != login_session['user_id']:
        return "<script>function myFunction() {alert('You are not authorized to delete this rentability.');}</script><body onload='myFunction()''>"
    if request.method == 'GET':
        return render_template('delete_rentability.html', category_id=category_id, item_id=item_id, rentability_delete=rentability_delete)
    elif request.method == 'POST':
        session.delete(rentability_delete)
        flash('Rentability %s Successfully Deleted' % rentability_delete.month)
        session.commit()
        return redirect(url_for('showRentability', category_id=category_id, item_id=item_id))


if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
