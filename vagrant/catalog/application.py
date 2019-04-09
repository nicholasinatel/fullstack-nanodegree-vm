from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from database_setup import Base, Catalog, Item

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///catalog.db'
db = SQLAlchemy(app)

# ---------------------------------------------------------------
# Restaurant Routes
@app.route('/')
@app.route('/restaurants')
def showRestaurants():

# API Endpoint
@app.route('/restaurants/JSON')
def showRestaurantsJSON():

@app.route('/restaurant/new', methods=['GET', 'POST'])
def newRestaurant():


@app.route('/restaurant/<int:restaurant_id>/edit', methods=['GET','POST'])
def editRestaurant(restaurant_id):


@app.route('/restaurant/<int:restaurant_id>/delete', methods=['GET','POST'])
def deleteRestaurant(restaurant_id):

# ---------------------------------------------------------------
# MenuItemS Routes
@app.route('/restaurant/<int:restaurant_id>/')
@app.route('/restaurant/<int:restaurant_id>/menu')
def showMenu(restaurant_id):

# API Endpoint
@app.route('/restaurant/<int:restaurant_id>/JSON')
@app.route('/restaurant/<int:restaurant_id>/menu/JSON')
def showMenuJSON(restaurant_id):

@app.route('/restaurant/<int:restaurant_id>/menu/new', methods=['GET','POST'])
def newMenuItem(restaurant_id):

@app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/edit', methods=['GET','POST'])
def editMenuItem(restaurant_id, menu_id):
      
        

@app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/delete', methods=['GET','POST'])
def deleteMenuItem(restaurant_id, menu_id):

# ---------------------------------------------------------------
# MenuItem API EndPoint Route
@app.route('/restaurant/<int:restaurant_id>/menu/JSON')
@app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/JSON')
def showMenuSingleItemJSON(restaurant_id, menu_id):


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5001)
