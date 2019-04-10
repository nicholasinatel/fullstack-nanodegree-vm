# Flask
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy import create_engine

# DB
from db_setup import Base, Category, Item, Rentability


engine = create_engine('sqlite:///catalog.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

app = Flask(__name__)

# ---------------------------------------------------------------
# Category Routes


@app.route('/')
@app.route('/category')
def showCategories():
    categories = session.query(Category).all()
    # print "categories: "
    # for category in categories:
    #     print category.name
    return render_template('category.html', categories=categories)

# API Endpoint


@app.route('/category/JSON')
def showCategoriesJSON():
    return "showCategoriesJSON"


@app.route('/category/new', methods=['GET', 'POST'])
def newCategory():
    if request.method == 'GET':
        return render_template('new_category.html')
    elif request.method == 'POST':
        nova_category = Category(
            name=request.form['name'], description=request.form['description'])
        session.add(nova_category)
        session.commit()
        return redirect(url_for('showCategories'))


@app.route('/category/<int:category_id>/edit', methods=['GET', 'POST'])
def editCategory(category_id):
    category_edit = session.query(Category).filter_by(id=category_id).one()
    if request.method == 'GET':
        return render_template('edit_category.html', category_edit=category_edit)
    elif request.method == 'POST':
        category_edit.name = request.form['name']
        category_edit.description = request.form['description']
        session.add(category_edit)
        session.commit()
        return redirect(url_for('showCategories'))


@app.route('/category/<int:category_id>/delete', methods=['GET', 'POST'])
def deleteCategory(category_id):
    category_delete = session.query(Category).filter_by(id=category_id).one()
    if request.method == 'GET':
        return render_template('delete_category.html', category_delete=category_delete)
    elif request.method == 'POST':
        session.delete(category_delete)
        session.commit()
        return redirect(url_for('showCategories'))

# ---------------------------------------------------------------
# ItemS Routes
@app.route('/category/<int:category_id>/')
@app.route('/category/<int:category_id>/item')
def showItem(category_id):
    category = session.query(Category).filter_by(id=category_id).one()
    items = session.query(Item).filter_by(category_id=category_id)
    return render_template('item.html', category=category, items=items)

# API Endpoint
@app.route('/category/<int:category_id>/JSON')
@app.route('/category/<int:category_id>/item/JSON')
def showItemJSON(category_id):
    return "showItemJSON"


@app.route('/category/<int:category_id>/item/new', methods=['GET', 'POST'])
def newItem(category_id):
    if request.method == 'GET':
        return render_template('new_item.html')
    elif request.method == 'POST':
        novo_item = Item(name=request.form['name'],
                         active=request.form['active'],
                         dy=request.form['dy'],
                         price=request.form['price'],
                         description=request.form['description'],
                         category_id=category_id)
        session.add(novo_item)
        session.commit()
        return redirect(url_for('showItem', category_id = category_id))


@app.route('/category/<int:category_id>/item/<int:item_id>/edit', methods=['GET', 'POST'])
def editItem(category_id, item_id):
    item_edit = session.query(Item).filter_by(id=item_id).first()
    if request.method == 'GET':
        return render_template('edit_item.html', category_id=category_id, item_edit=item_edit)
    elif request.method == 'POST':
        item_edit.name = request.form['name']
        item_edit.active = request.form['active']
        item_edit.dy = request.form['dy']
        item_edit.price = request.form['price']
        item_edit.description = request.form['description']
        session.add(item_edit)
        session.commit()
        return redirect(url_for('showItem', category_id=category_id))


@app.route('/category/<int:category_id>/item/<int:item_id>/delete', methods=['GET', 'POST'])
def deleteItem(category_id, item_id):
    item_delete = session.query(Item).filter_by(id=item_id).first()
    if request.method == 'GET':
        return render_template('delete_item.html', category_id=category_id, item_delete=item_delete)
    elif request.method == 'POST':
        session.delete(item_delete)
        session.commit()
        return redirect(url_for('showItem', category_id=category_id))

# Item API EndPoint Route
@app.route('/category/<int:category_id>/item/JSON')
@app.route('/category/<int:category_id>/item/<int:item_id>/JSON')
def showSingleItemJSON(category_id, item_id):
    return "showSingleItemJSON"

# ---------------------------------------------------------------
# Rentability Routes
@app.route('/category/<int:category_id>/item/<int:item_id>')
@app.route('/category/<int:category_id>/item/<int:item_id>/rentability')
def showRentability(category_id, item_id):
    category = session.query(Category).filter_by(id=category_id).one()
    item = session.query(Item).filter_by(id=item_id).first()
    rendas = session.query(Rentability).filter_by(item_id=item_id)
    return render_template('rentability.html', category=category, item=item, rendas=rendas)

@app.route('/category/<int:category_id>/item/<int:item_id>/rentability/new', methods=['GET', 'POST'])
def newRentability(category_id, item_id):
    if request.method == 'GET':
        return render_template('new_rentability.html', category_id=category_id, item_id=item_id)
    elif request.method == 'POST':
        money = float(request.form['money'])
        percent = float(request.form['percent'])
        novo_rentability = Rentability(month=request.form['month'],
                         money=money,
                         percent=percent,
                         item_id=item_id)
        session.add(novo_rentability)
        session.commit()
        return redirect(url_for('showRentability', category_id=category_id, item_id=item_id))

@app.route('/category/<int:category_id>/item/<int:item_id>/rentability/<int:rentability_id>/edit', methods=['GET', 'POST'])
def editRentability(category_id, item_id, rentability_id):
    rentability_edit = session.query(Rentability).filter_by(id=rentability_id).first()
    if request.method == 'GET':
        return render_template('edit_rentability.html', category_id=category_id, item_id=item_id, rentability_edit=rentability_edit)
    elif request.method == 'POST':
        rentability_edit.month = request.form['month']
        rentability_edit.money = float(request.form['money'])
        rentability_edit.percent = float(request.form['percent'])
        session.add(rentability_edit)
        session.commit()
        return redirect(url_for('showRentability', category_id=category_id, item_id=item_id))


@app.route('/category/<int:category_id>/item/<int:item_id>/rentability/<int:rentability_id>/delete', methods=['GET', 'POST'])
def deleteRentability(category_id, item_id, rentability_id):
    rentability_delete = session.query(Rentability).filter_by(id=rentability_id).first()
    if request.method == 'GET':
        return render_template('delete_rentability.html', category_id=category_id, item_id=item_id, rentability_delete=rentability_delete)
    elif request.method == 'POST':
        session.delete(rentability_delete)
        session.commit()
        return redirect(url_for('showRentability', category_id=category_id, item_id=item_id))

if __name__ == '__main__':
    # app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
