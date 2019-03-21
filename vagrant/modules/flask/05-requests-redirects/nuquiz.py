# WebServer Flask FrameWork
from flask import Flask
from flask import render_template
from flask import request  # so i can receive form requests
from flask import redirect
from flask import url_for
# ORM Object Relational Modeling for SQL
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
# SQLite Classes
from database_setup import Base, Restaurant, MenuItem
# Resolving Issues
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///restaurantmenu.db'
db = SQLAlchemy(app)

# engine = create_engine('sqlite:///restaurantmenu.db')
# Base.metadata.bind = engine
# DBSession = sessionmaker(bind=engine)
# session = DBSession()

@app.route('/')
@app.route('/restaurants')
def restaurant():
    # DBSession = sessionmaker(bind=engine)
    # session = DBSession()
    restaurants = db.session.query(Restaurant).all()
    # restaurants = Restaurant.query.all()
    # print("restaurants: ", restaurants)
    return render_template('restaurants.html', restaurants=restaurants)

@app.route('/restaurants/<int:restaurant_id>/')
def restaurantMenu(restaurant_id):
    # DBSession = sessionmaker(bind=engine)
    # session = DBSession()
    restaurant = db.session.query(Restaurant).filter_by(id=restaurant_id).one()
    items = db.session.query(MenuItem).filter_by(restaurant_id=restaurant.id)
    return render_template('menu.html', restaurant=restaurant, items=items)

# Task 1: Create route for newMenuItem function here
@app.route('/restaurants/<int:restaurant_id>/new', methods=['GET', 'POST'])
def newMenuItem(restaurant_id):
    if request.method == 'POST':
        newItem = MenuItem(
            name=request.form['name'],
            description=request.form['description'],
            price=request.form['price'],
            course=request.form['course'],
            restaurant_id=restaurant_id)  # Extract name field from my form in html file
        # DBSession = sessionmaker(bind=engine)
        # session = DBSession()
        db.session.add(newItem)
        db.session.commit()
        return redirect(url_for('restaurantMenu', restaurant_id=restaurant_id))
    else:
        return render_template('newmenuitem.html', restaurant_id=restaurant_id)


# Task 2: Create route for editMenuItem function here
@app.route('/restaurants/<int:restaurant_id>/<int:menu_id>/edit/', methods=['POST','GET'])
def editMenuItem(restaurant_id, menu_id):
    # DBSession = sessionmaker(bind=engine)
    # session = DBSession()
    editedItem = db.session.query(MenuItem).filter_by(id=menu_id).one()
    if request.method == 'POST':
        if request.form['name']:            
            editedItem.name = request.form['name']
        db.session.add(editedItem)
        db.session.commit()
        return redirect(url_for('restaurantMenu', restaurant_id=restaurant_id))
    else:
        # USE THE RENDER_TEMPLATE FUNCTION BELOW TO SEE THE VARIABLES
        # YOU SHOULD USE IN YOUR EDITMENUITEM TEMPLATE
        return render_template('editmenuitem.html', restaurant_id=restaurant_id, menu_id=menu_id, item=editedItem)

# Task 3: Create a route for deleteMenuItem function here
@app.route('/restaurants/<int:restaurant_id>/<int:menu_id>/delete/', methods=['POST','GET'])
def deleteMenuItem(restaurant_id, menu_id):
    itemToDelete = db.session.query(MenuItem).filter_by(id=menu_id).one()
    if request.method == 'POST':
        db.session.delete(itemToDelete)
        db.session.commit()
        return redirect(url_for('restaurantMenu', restaurant_id=restaurant_id))
    else:
        db.session.rollback()
        return render_template('deleteconfirmation.html', item=itemToDelete)


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
