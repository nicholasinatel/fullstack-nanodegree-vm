from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from database_setup import Base, Restaurant, MenuItem

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///restaurantmenu.db'
db = SQLAlchemy(app)

# ---------------------------------------------------------------
# Restaurant Routes
@app.route('/')
@app.route('/restaurants')
def showRestaurants():
    restaurants = db.session.query(Restaurant).all()
    return render_template('restaurants.html', restaurants=restaurants)
# API Endpoint
@app.route('/restaurants/JSON')
def showRestaurantsJSON():
    restaurants = db.session.query(Restaurant).all()
    return jsonify(Restaurant=[restaurant.serialize for restaurant in restaurants])

@app.route('/restaurant/new', methods=['GET', 'POST'])
def newRestaurant():
    if request.method == 'GET':
        return render_template('newrestaurant.html')
    if request.method == 'POST':
        newRestaurant = Restaurant(name=request.form['name'])
        db.session.add(newRestaurant)
        db.session.commit()
        # Flash
        return redirect(url_for('showRestaurants'))


@app.route('/restaurant/<int:restaurant_id>/edit', methods=['GET','POST'])
def editRestaurant(restaurant_id):
    restaurant = db.session.query(Restaurant).filter_by(id=restaurant_id).one()
    if request.method == 'GET':
        return render_template('editrestaurant.html', restaurant=restaurant)
    if request.method == 'POST':
        if request.form['name']:
            restaurant.name = request.form['name']
        db.session.add(restaurant)
        db.session.commit()
        #Flash
        return redirect(url_for('showRestaurants'))


@app.route('/restaurant/<int:restaurant_id>/delete', methods=['GET','POST'])
def deleteRestaurant(restaurant_id):
    restaurant = db.session.query(Restaurant).filter_by(id=restaurant_id).one()
    if request.method == 'GET':
        return render_template('deleterestaurant.html', restaurant=restaurant)
    if request.method == 'POST':
        db.session.delete(restaurant)
        db.session.commit()
        #Flash
        return redirect(url_for('showRestaurants'))
# ---------------------------------------------------------------
# MenuItemS Routes
@app.route('/restaurant/<int:restaurant_id>/')
@app.route('/restaurant/<int:restaurant_id>/menu')
def showMenu(restaurant_id):
    restaurant = db.session.query(Restaurant).filter_by(id=restaurant_id).one()
    items = db.session.query(MenuItem).filter_by(restaurant_id=restaurant_id).all()
    return render_template('menu.html', restaurant=restaurant, items=items)
# API Endpoint
@app.route('/restaurant/<int:restaurant_id>/JSON')
@app.route('/restaurant/<int:restaurant_id>/menu/JSON')
def showMenuJSON(restaurant_id):
    items = db.session.query(MenuItem).filter_by(restaurant_id=restaurant_id).all()
    return jsonify(MenuItems=[i.serialize for i in items])

@app.route('/restaurant/<int:restaurant_id>/menu/new', methods=['GET','POST'])
def newMenuItem(restaurant_id):
    if request.method == 'GET':
        return render_template('newmenuitem.html', restaurant_id=restaurant_id)
    if request.method == 'POST':
        newItem = MenuItem(
                name=request.form['name'],
                course=request.form['course'],
                description=request.form['description'],
                price=request.form['price'],
                restaurant_id=restaurant_id)
        db.session.add(newItem)
        db.session.commit()
        # Flash
        return redirect(url_for('showMenu', restaurant_id=restaurant_id))

@app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/edit', methods=['GET','POST'])
def editMenuItem(restaurant_id, menu_id):
    item = db.session.query(MenuItem).filter_by(id=menu_id).one()
    if request.method == 'GET':
        return render_template('editmenuitem.html', restaurant_id=restaurant_id, item=item)
    if request.method == 'POST':
        if request.form['name']:
           item.name = request.form['name']
        if request.form['description']:
           item.description = request.form['description']
        if request.form['price']:
           item.price = request.form['price']
        if request.form['course']:
           item.course = request.form['course']
        db.session.add(item)
        db.session.commit()
        # Flash
        return redirect(url_for('showMenu', restaurant_id=restaurant_id))

        
        

@app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/delete', methods=['GET','POST'])
def deleteMenuItem(restaurant_id, menu_id):
    item = db.session.query(MenuItem).filter_by(id=menu_id).one()
    if request.method == 'GET':
        return render_template('deletemenuitem.html', restaurant_id=restaurant_id, item=item)
    if request.method == 'POST':
        db.session.delete(item)
        db.session.commit()
        return redirect(url_for('showMenu', restaurant_id=restaurant_id))
# ---------------------------------------------------------------
# MenuItem API EndPoint Route
@app.route('/restaurant/<int:restaurant_id>/menu/JSON')
@app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/JSON')
def showMenuSingleItemJSON(restaurant_id, menu_id):
    item = db.session.query(MenuItem).filter_by(id=menu_id).one()
    return jsonify(MenuItem=item.serialize)

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5001)
