#!/usr/bin/python2

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
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in range(32))
    login_session['state'] = state
    return render_template('login.html', STATE=state)


@app.route('/gconnect', methods=['POST'])
def gconnect():
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
    login_session['picture'] = data['picture']

    user_id = get_user_id(login_session['email'])
    if not user_id:
        user_id = create_user(login_session)
    login_session['user_id'] = user_id

    flash("you are now logged in as %s" % login_session['email'])

    return "All good"


@app.route('/logout')
def logout():
    if 'provider' in login_session:
        if login_session['provider'] == 'google':
            glogout()
            del login_session['gplus_id']
            del login_session['access_token']
        del login_session['username']
        del login_session['email']
        del login_session['picture']
        del login_session['user_id']
        del login_session['provider']
        flash("You have been Successfully logged out!")
        return redirect(url_for('catalog'))
    else:
        flash("You were not logged out!")
        return redirect(url_for('catalog'))


@app.route('/glogout')
def glogout():
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
    session = DBSession()
    categories = session.query(Categories).filter_by(parent_id=None).all()
    last_products = session.query(Products).order_by(
        desc(Products.created_at)).limit(10)
    return render_template('catalog.html', categories=categories,
                           last_products=last_products)


@app.route('/catalog/<string:cat_name>/')
def cat_page(cat_name):
    session = DBSession()
    cat = session.query(Categories).filter_by(name=cat_name).one()
    subcats = session.query(Categories).filter_by(parent_id=cat.id).all()
    last_products = session.query(Products).join(ProductsCategories).filter(
        ProductsCategories.category_id == cat.id).order_by(
        desc(Products.created_at)).all()
    return render_template('cat.html', cat=cat, subcats=subcats,
                           last_products=last_products)


@app.route('/catalog/products/<string:product_name>/')
def product_page(product_name):
    session = DBSession()
    product = session.query(Products).filter_by(name=product_name).one()
    return render_template('product.html', product=product)


@app.route('/catalog/add_product/', methods=['GET', 'POST'])
def add_product():
    if 'username' not in login_session:
        return redirect('/login')

    if request.method == 'POST':
        session = DBSession()
        new_item = Products(name=request.form['name'],
                            description=request.form['description'],
                            price_cents=int(request.form['price'])*100,
                            created_by=login_session['user_id'])
        session.add(new_item)
        session.commit()
        flash('New Item %s Successfully Created' % new_item.name)
        return redirect(url_for('catalog'))
    else:
        return render_template('new_product.html')


@app.route('/catalog/<string:product_name>/edit_product/',
           methods=['GET', 'POST'])
def edit_product(product_name):
    if 'username' not in login_session:
        return redirect('/login')

    if request.method == 'POST':
        session = DBSession()
        edited_product = session.query(Products).filter_by(
            name=product_name).one()

        new_name = request.form['name']
        new_description = request.form['description']
        new_price = request.form['price']

        if new_name:
            id_of_new_name = session.query(Products).filter_by(
                name=new_name).first()
            if id_of_new_name:
                flash('A product with the name %s already exists. Please pick \
                    a different name' % new_name)
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
                flash('The price can not be lower than $0.01! This is not a \
                    charity...')
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
    if 'username' not in login_session:
        return redirect('/login')

    if request.method == 'POST':
        session = DBSession()

        try:
            delete_product = session.query(Products).filter_by(
                name=product_name).one()
            session.delete(delete_product)
            session.commit()
            flash('Product %s Successfully Deleted' % delete_product.name)
            return redirect(url_for('catalog'))
        except NoResultFound:
            flash('A product named %s does not exist and can therefore not be \
                deleted' % product_name)
            return render_template('delete_product.html')
    else:
        return render_template('delete_product.html')


@app.route('/catalog/<string:product_name>/edit_categories/',
           methods=['GET', 'POST'])
def edit_categories(product_name):
    if 'username' not in login_session:
        return redirect('/login')

    else:
        session = DBSession()
        edited_product = session.query(Products).filter_by(
            name=product_name).one()
        categories = session.query(ProductsCategories).join(Categories).filter(
            ProductsCategories.product_id == edited_product.id).all()
        return render_template('edit_categories.html', categories=categories,
                               product=edited_product)


@app.route('/catalog/<string:product_name>/delete_categorization/'
           '<int:product_category_id>/', methods=['GET', 'POST'])
def delete_categorization(product_name, product_category_id):
    if 'username' not in login_session:
        return redirect('/login')

    if request.method == 'POST':
        session = DBSession()

        try:
            product = session.query(Products).filter_by(
                name=product_name).one()
            delete_categorization = session.query(
                ProductsCategories).filter_by(id=product_category_id).one()
            session.delete(delete_categorization)
            session.commit()
            flash('Categorization for Product %s Successfully Deleted'
                  % product.name)
            return redirect(url_for('edit_categories',
                            product_name=product.name))
        except NoResultFound:
            flash('Either the product or the categorization does not exist \
                and can therefore not be deleted')
            return redirect('catalog')
    else:
        return render_template('delete_categorization.html')


@app.route('/catalog/<string:product_name>/new_categorization/',
           methods=['GET', 'POST'])
def new_categorization(product_name):
    if 'username' not in login_session:
        return redirect('/login')

    if request.method == 'POST':
        session = DBSession()
        edited_product = session.query(Products).filter_by(
            name=product_name).one()
        new_categories = request.form.getlist('category')

        if new_categories:
            for cat in new_categories:
                new_cat = ProductsCategories(product_id=edited_product.id,
                                             category_id=cat)
                session.add(new_cat)
                session.commit()

        flash('New Item Categorizations Successfully Created')
        return redirect(url_for('edit_categories', product_name=product_name))

    else:
        session = DBSession()
        categories = session.query(Categories).all()
        return render_template('new_categorization.html',
                               categories=categories)


def get_user_id(email):
    session = DBSession()
    try:
        user = session.query(Users).filter_by(email=email).one()
        return user.id
    except Exception:
        return None


def get_user_info(user_id):
    session = DBSession()
    user = session.query(Users).filter_by(id=user_id).one()
    return user


def create_user(login_session):
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
