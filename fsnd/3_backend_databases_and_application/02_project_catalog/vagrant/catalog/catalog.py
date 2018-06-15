#!/usr/bin/python2

"""
    File name: catalog.py
    Author: Christian Eik
    Date created: 2018-06-10
    Date last modified: 2018-06-15
    Python Version: 2.7

    Run the flask app for the catalog project.
"""

import random
import string
import json
import requests
import httplib2

from oauth2client.client import flow_from_clientsecrets, FlowExchangeError

from sqlalchemy import create_engine, desc
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.exc import NoResultFound
from database_setup import Base
from database_setup import Users, Categories, Products, ProductsCategories

from flask import Flask, render_template, request, redirect, jsonify, url_for
from flask import flash, make_response
from flask import session as login_session

app = Flask(__name__)

CLIENT_ID = json.loads(open(
    'google_client_secret.json', 'r').read())['web']['client_id']

engine = create_engine('sqlite:///catalog_project.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)


@app.route('/login')
def login():
    """
    Handler for the login page.

    Add a state variable to login_session.

    Args:
        None

    Return:
        Render the login.html template with a STATE variable.
    """

    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in range(32))
    login_session['state'] = state
    return render_template('login.html', STATE=state)


@app.route('/gconnect', methods=['POST'])
def gconnect():
    """
    Handler for the gconnect page.

    Take care of authentication with Google Oauth. Add the provider,
    username, and email to login_session. This handler is called via JS on the
    login.html page. The page also takes care of redirection after successful
    login.

    Args:
        None

    Return:
        Return an instance of Flasks Response class in case of errors. In case
        of successful auth, create a flash message.
    """

    # Validate state token
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Obtain authorization code
    code = request.data

    try:
        # Upgrade the authorization code into a credentials object
        oauth_flow = flow_from_clientsecrets('google_client_secret.json',
                                             scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(
            json.dumps('Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Check that the access token is valid.
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
           % access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])
    # If there was an error in the access token info, abort.
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is used for the intended user.
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(
            json.dumps("Token's user ID doesn't match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is valid for this app.
    if result['issued_to'] != CLIENT_ID:
        response = make_response(
            json.dumps("Token's client ID does not match app's."), 401)
        print("Token's client ID does not match app's.")
        response.headers['Content-Type'] = 'application/json'
        return response

    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    # The values of login_session are set down below!
    # This is to test if the user is alread logged in!
    stored_access_token = login_session.get('access_token')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_access_token is not None and gplus_id == stored_gplus_id:
        response = make_response(json.dumps(
            'Current user is already connected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Store the access token in the session for later use.
    login_session['access_token'] = credentials.access_token
    login_session['gplus_id'] = gplus_id

    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()

    login_session['provider'] = 'google'
    login_session['username'] = data['name']
    login_session['email'] = data['email']

    user_id = get_user_id(login_session['email'])
    if not user_id:
        user_id = create_user(login_session)
    login_session['user_id'] = user_id

    flash("you are now logged in as %s" % login_session['email'])

    return "All good"


@app.route('/logout')
def logout():
    """
    Handler for the logout page.

    Delete the relevant values from login_session.

    Args:
        None

    Return:
        Redirect to the catalog page.
    """

    if 'provider' in login_session:
        if login_session['provider'] == 'google':
            glogout()
            del login_session['gplus_id']
            del login_session['access_token']
        del login_session['username']
        del login_session['email']
        del login_session['user_id']
        del login_session['provider']
        flash("You have been Successfully logged out!")
        return redirect(url_for('catalog'))
    else:
        flash("You were not logged out!")
        return redirect(url_for('catalog'))


@app.route('/glogout')
def glogout():
    """
    Helper handler for lougout for Google Users.

    Is called by the logout function if the provider is google.

    Args:
        None

    Return:
        Return a success/failure response.
    """

    access_token = login_session.get('access_token')
    if access_token is None:
        response = make_response(json.dumps(
            'Current user not connected.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % access_token
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]
    if result['status'] == '200':
        response = make_response(json.dumps('Successfully disconnected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response
    else:
        response = make_response(json.dumps(
            'Failed to revoke token for given user.', 400))
        response.headers['Content-Type'] = 'application/json'
        return response


@app.route('/')
@app.route('/catalog/')
def catalog():
    """
    Handler for the catalog page.

    Args:
        None

    Return:
        Render the catalog.html template with the cat, subcat, and
        last_products variables.
    """

    session = DBSession()
    categories = session.query(Categories).filter_by(parent_id=None).all()
    last_products = session.query(Products).order_by(
        desc(Products.created_at)).limit(10)
    return render_template('catalog.html', categories=categories,
                           last_products=last_products)


@app.route('/catalog/<string:cat_name>/')
def cat_page(cat_name):
    """
    Handler for the category page.

    Args:
        cat_name <string>: Name of a category

    Return:
        Render the cat.html template with the cat, subcat, and last_products
        variables.
    """

    session = DBSession()
    cat = session.query(Categories).filter_by(name=cat_name).one_or_none()
    if not cat:
        flash('The category %s does not exist' % cat_name)
        return redirect(url_for('catalog'))
    else:
        subcats = session.query(Categories).filter_by(parent_id=cat.id).all()
        last_products = session.query(Products).join(ProductsCategories).filter(
            ProductsCategories.category_id == cat.id).order_by(
            desc(Products.created_at)).all()
        return render_template('cat.html', cat=cat, subcats=subcats,
                               last_products=last_products)


@app.route('/catalog/products/<string:product_name>/')
def product_page(product_name):
    """
    Handler for the product page.

    Args:
        product_name <string>: Name of a product

    Return:
        Render the product.html template with a product variable.
    """

    session = DBSession()
    product = session.query(Products).filter_by(
        name=product_name).one_or_none()
    if not product:
        flash('The product %s does not exist' % product_name)
        return redirect(url_for('catalog'))
    else:
        return render_template('product.html', product=product)


@app.route('/catalog/add_product/', methods=['GET', 'POST'])
def add_product():
    """
    Handler for the add_product page.

    Args:
        None

    GET: Render the new_product.html template.

    POST: Create a new product based on the form input and add it to the
    database. Then redirect to /catalog.
    """

    if 'username' not in login_session:
        return redirect('/login')

    if request.method == 'POST':
        session = DBSession()
        new_product = Products(name=request.form['name'],
                               description=request.form['description'],
                               price_cents=int(request.form['price'])*100,
                               created_by=login_session['user_id'])
        session.add(new_product)
        session.commit()
        flash('New Item %s Successfully Created' % new_product.name)
        return redirect(url_for('catalog'))
    else:
        return render_template('new_product.html')


@app.route('/catalog/<string:product_name>/edit_product/',
           methods=['GET', 'POST'])
def edit_product(product_name):
    """
    Handler for the add_product page.

    Args:
        product_name <string>: Name of a product

    GET: Render the edit_product.html template.

    POST: Edit a product based on the input of the form and commit the changes
    to the database. Then redirect to the product_page of the edited product.
    """

    if 'username' not in login_session:
        return redirect('/login')

    session = DBSession()
    edited_product = session.query(Products).filter_by(
        name=product_name).one_or_none()

    if not edited_product:
        flash('The product %s does not exist' % product_name)
        return redirect(url_for('catalog'))

    elif edited_product.created_by != login_session['user_id']:
        flash('You are not the owner of this product and therefore can not \
            edit it')
        return redirect(url_for('product_page',
                                product_name=edited_product.name))

    else:
        if request.method == 'POST':
            new_name = request.form['name']
            new_description = request.form['description']
            new_price = request.form['price']

            if new_name:
                id_of_new_name = session.query(Products).filter_by(
                    name=new_name).first()
                if id_of_new_name:
                    flash('A product with the name %s already exists. Please \
                        pick a different name' % new_name)
                    return render_template('edit_product.html',
                                           default_name=new_name,
                                           default_description=new_description,
                                           default_price=new_price/100)
                edited_product.name = new_name
            if new_description:
                edited_product.description = new_description
            if new_price:
                new_price_foat = float(new_price)*100
                if new_price_foat < 1:
                    flash('The price can not be lower than $0.01! This is not \
                        a charity...')
                    return render_template('edit_product.html',
                                           default_name=new_name,
                                           default_description=new_description,
                                           default_price=new_price_foat/100)
                edited_product.price_cents = int(new_price_foat)

            session.add(edited_product)
            session.commit()
            flash('Product %s Successfully Edited' % edited_product.name)
            return redirect(url_for('product_page',
                                    product_name=edited_product.name))
        else:
            return render_template('edit_product.html')


@app.route('/catalog/<string:product_name>/delete_product/',
           methods=['GET', 'POST'])
def delete_product(product_name):
    """
    Handler for the delete_product page.

    Args:
        product_name <string>: Name of a product

    GET: Render the delete_product.html template.

    POST: Delete a product, then redirect to /catalog.
    """

    if 'username' not in login_session:
        return redirect('/login')

    session = DBSession()
    delete_product = session.query(Products).filter_by(
        name=product_name).one_or_none()

    if not delete_product:
        flash('A product named %s does not exist and can therefore not be \
            deleted' % product_name)
        return redirect(url_for('catalog'))

    elif delete_product.created_by != login_session['user_id']:
        flash('You are not the owner of this product and therefore can not \
            edit it')
        return redirect(url_for('product_page',
                                product_name=delete_product.name))

    if request.method == 'POST':
        session.delete(delete_product)
        session.commit()
        flash('Product %s Successfully Deleted' % delete_product.name)
        return redirect(url_for('catalog'))
    else:
        return render_template('delete_product.html')


@app.route('/catalog/<string:product_name>/edit_categories/',
           methods=['GET'])
def edit_categories(product_name):
    """
    Handler for the edit_categories page.

    Args:
        product_name <string>: Name of a product

    Return:
        Render the edit_categories.html template with the categories and
        product variables.
    """

    if 'username' not in login_session:
        return redirect('/login')

    else:
        session = DBSession()
        edited_product = session.query(Products).filter_by(
            name=product_name).one_or_none()

        if not edited_product:
            flash('The product %s does not exist' % product_name)
            return redirect(url_for('catalog'))
        else:
            categories = session.query(ProductsCategories).join(
                Categories).filter(
                ProductsCategories.product_id == edited_product.id).all()
            return render_template('edit_categories.html',
                                   categories=categories,
                                   product=edited_product)


@app.route('/catalog/<string:product_name>/delete_categorization/'
           '<int:product_category_id>/', methods=['GET', 'POST'])
def delete_categorization(product_name, product_category_id):
    """
    Handler for the delete_categorization page.

    Args:
        product_name <string>: Name of a product
        product_name <string/int>: ID of the product - category mapping

    GET: Render the delete_categorization.html template.

    POST: Delete the product - category mapping and redirect to the
    edit_categories page of the product.
    """

    if 'username' not in login_session:
        return redirect('/login')

    session = DBSession()
    product = session.query(Products).filter_by(
        name=product_name).one_or_none()

    if not product:
        flash('A product named %s does not exist' % product_name)
        return redirect(url_for('catalog'))

    delete_categorization = session.query(
        ProductsCategories).filter_by(id=product_category_id).one_or_none()

    if not delete_categorization:
        flash('This categorization does not exist')
        return redirect(url_for('edit_categories', product_name=product_name))

    elif delete_categorization.created_by != login_session['user_id']:
        flash('You are not the owner of this categorization and therefore can \
            not delete it')
        return redirect(url_for('edit_categories', product_name=product_name))

    else:
        if request.method == 'POST':
            session.delete(delete_categorization)
            session.commit()
            flash('Categorization for Product %s Successfully Deleted'
                  % product.name)
            return redirect(url_for('edit_categories',
                            product_name=product.name))
        else:
            return render_template('delete_categorization.html')


@app.route('/catalog/<string:product_name>/new_categorization/',
           methods=['GET', 'POST'])
def new_categorization(product_name):
    """
    Handler for the new_categorization page.

    Args:
        product_name <string>: Name of a product

    GET: Render the new_categorization.html template with the categories
    variable.

    POST: Add the product - category mappings provided by the form and
    redirect to the edit_categories page of the product.
    """

    if 'username' not in login_session:
        return redirect('/login')

    if request.method == 'POST':
        session = DBSession()
        edited_product = session.query(Products).filter_by(
            name=product_name).one_or_none()

        if not edited_product:
            flash('The product %s does not exist' % product_name)
            return redirect(url_for('catalog'))
        else:
            new_categories = request.form.getlist('category')

            if new_categories:
                for cat in new_categories:
                    new_cat = ProductsCategories(
                        product_id=edited_product.id,
                        category_id=cat,
                        created_by=login_session['user_id'])
                    session.add(new_cat)
                    session.commit()

            flash('New Item Categorizations Successfully Created')
            return redirect(url_for('edit_categories',
                                    product_name=product_name))

    else:
        session = DBSession()
        categories = session.query(Categories).all()
        return render_template('new_categorization.html',
                               categories=categories)


@app.route('/products_JSON')
def products_json():
    """API endpoint providing a list of all products as JSON."""

    session = DBSession()
    products = session.query(Products).all()
    return jsonify(products=[p.serialize for p in products])


@app.route('/catalog/products/<string:product_name>/product_JSON')
def product_json(product_name):
    """API endpoint providing the product data of a single product as JSON."""

    session = DBSession()
    product = session.query(Products).filter_by(
            name=product_name).one_or_none()
    return jsonify(product.serialize)


@app.route('/catalog/products/<string:product_name>/product_category_JSON')
def product_category_json(product_name):
    """API endpoint providing the category data of a single product as JSON."""

    session = DBSession()
    product = session.query(Products).filter_by(
            name=product_name).one_or_none()
    categories = session.query(ProductsCategories).filter_by(
            product_id=product.id).all()
    return jsonify(products=[p.serialize for p in categories])


@app.route('/categorization_JSON')
def catalog_json():
    """API endpoint providing a list of all product categorizations as JSON."""
    session = DBSession()
    categorization = session.query(ProductsCategories).all()
    return jsonify(categorization=[pc.serialize for pc in categorization])


def get_user_id(email):
    """Return the user id of the given email."""
    session = DBSession()
    try:
        user = session.query(Users).filter_by(email=email).one()
        return user.id
    except Exception:
        return None


def get_user_info(user_id):
    """Return the user object for a given user_id."""
    session = DBSession()
    try:
        user = session.query(Users).filter_by(id=user_id).one()
        return user
    except Exception:
        return None


def create_user(login_session):
    """Create a user from the given login_session and return it's user id."""
    session = DBSession()
    new_user = Users(name=login_session['username'],
                     email=login_session['email'])
    session.add(new_user)
    session.commit()
    user = session.query(Users).filter_by(email=login_session['email']).one()
    return user.id


if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
