from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem

from flask import Flask, render_template, request, redirect, url_for, flash
from flask import jsonify
app = Flask(__name__)

engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


@app.route('/restaurants/JSON')
def restaurants_json():
    restaurants = session.query(Restaurant).all()
    return jsonify(Restaurants=[i.serialize for i in restaurants])


@app.route('/restaurant/<int:restaurant_id>/menu/JSON')
def restaurant_menu_json(restaurant_id):
    items = session.query(MenuItem).filter_by(
        restaurant_id=restaurant_id).all()
    return jsonify(MenuItems=[i.serialize for i in items])


@app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/JSON')
def restaurant_menu_item_json(restaurant_id, menu_id):
    item = session.query(MenuItem).filter_by(
        id=menu_id).one()
    return jsonify(MenuItem=item.serialize)


@app.route('/')
@app.route('/restaurants')
def show_restaurants():
    restaurants = session.query(Restaurant).all()
    if not restaurants:
        flash("You have no restaurants! Go create some!")
    return render_template('restaurants.html', restaurants=restaurants)


@app.route('/restaurant/new', methods=['GET', 'POST'])
def new_restaurant():
    if request.method == 'POST':
        new_restaurant = Restaurant(name=request.form['name'])
        session.add(new_restaurant)
        session.commit()
        flash("New Restaurant Created!")
        return redirect(url_for('show_restaurants'))
    else:
        return render_template('new_restaurant.html')


@app.route('/restaurant/<int:restaurant_id>/edit', methods=['GET', 'POST'])
def edit_restaurant(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    if request.method == 'POST':
        if request.form['name']:
            restaurant.name = request.form['name']
        session.add(restaurant)
        session.commit()
        flash("Restaurant Edited!")
        return redirect(url_for('show_restaurants'))
    else:
        return render_template('edit_restaurant.html', restaurant=restaurant)


@app.route('/restaurant/<int:restaurant_id>/delete', methods=['GET', 'POST'])
def delete_restaurant(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    if request.method == 'POST':
        session.delete(restaurant)
        session.commit()
        flash("Restaurant Deleted!")
        return redirect(url_for('show_restaurants'))
    else:
        return render_template('delete_restaurant.html', restaurant=restaurant)


@app.route('/restaurant/<int:restaurant_id>/')
@app.route('/restaurant/<int:restaurant_id>/menu')
def show_menu(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    appetizers = session.query(MenuItem).filter_by(
        restaurant_id=restaurant_id, course='Appetizer').all()
    entrees = session.query(MenuItem).filter_by(
        restaurant_id=restaurant_id, course='Entree').all()
    desserts = session.query(MenuItem).filter_by(
        restaurant_id=restaurant_id, course='Dessert').all()
    beverages = session.query(MenuItem).filter_by(
        restaurant_id=restaurant_id, course='Beverage').all()
    return render_template('menu.html', restaurant=restaurant,
                           appetizers=appetizers, entrees=entrees,
                           desserts=desserts, beverages=beverages)


@app.route('/restaurant/<int:restaurant_id>/menu/new/',
           methods=['GET', 'POST'])
def new_menu_item(restaurant_id):
    if request.method == 'POST':
        new_item = MenuItem(name=request.form['name'],
                            description=request.form['description'],
                            price=request.form['price'],
                            course=request.form['course'],
                            restaurant_id=restaurant_id)
        session.add(new_item)
        session.commit()
        flash("New Menu Item Created!")
        return redirect(url_for('show_menu',
                        restaurant_id=restaurant_id))
    else:
        return render_template('new_menu_item.html',
                               restaurant_id=restaurant_id)


@app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/edit',
           methods=['GET', 'POST'])
def edit_menu_item(restaurant_id, menu_id):
    edited_item = session.query(MenuItem).filter_by(id=menu_id).one()
    if request.method == 'POST':
        if request.form['name']:
            edited_item.name = request.form['name']
        session.add(edited_item)
        session.commit()
        flash("Menu Item Edited!")
        return redirect(url_for('show_menu',
                                restaurant_id=restaurant_id))
    else:
        return render_template('edit_menu_item.html',
                               restaurant_id=restaurant_id, menu_id=menu_id,
                               edited_item=edited_item)


@app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/delete',
           methods=['GET', 'POST'])
def delete_menu_item(restaurant_id, menu_id):
    delete_item = session.query(MenuItem).filter_by(id=menu_id).one()
    if request.method == 'POST':
        session.delete(delete_item)
        session.commit()
        flash("Menu Item Deleted!")

        return redirect(url_for('show_menu',
                                restaurant_id=restaurant_id))
    else:
        return render_template('delete_menu_item.html',
                               delete_item=delete_item)


if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
