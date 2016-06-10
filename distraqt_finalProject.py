from flask import (
    Flask, render_template, request, redirect, jsonify, url_for, flash)
import os
from flask_sqlalchemy import SQLAlchemy
from flask_sqlalchemy import xrange
from functools import wraps

from sqlalchemy import create_engine, asc
from sqlalchemy.orm import sessionmaker
from distraqt_database_setup import Base, Restaurant, MenuItem, User

from flask import session as login_session
import random
import string

from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json
from flask import make_response
import requests

app = Flask(__name__)

CLIENT_ID = json.loads(
    open('client_secrets.json', 'r').read())['web']['client_id']
APPLICATION_NAME = "Restaurant Menu Application"


# reinstate sqlite for final project review purposes:
engine = create_engine('sqlite:///distraqtJun6.db')

# functional postgres db - commented out for final project submission purposes
# Create postgres db with the following name #
# engine = create_engine(
# postgres://cuymriuwjdobmm:GmodrGMvy-uWsL3_4XOJHMhyLr@ec2-54-225-79-232.
# compute-1.amazonaws.com:5432/dif8vbb8o8q66')

Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

# Create anti-forgery state token #


@app.route('/login')
def showLogin():
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in xrange(32))
    login_session['state'] = state
    # return "The current session state is %s" % login_session['state']
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
        oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
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
        print "Token's client ID does not match app's."
        response.headers['Content-Type'] = 'application/json'
        return response

    stored_credentials = login_session.get('access_token')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_credentials is not None and gplus_id == stored_gplus_id:
        response = make_response(json.dumps
                                 ('Current user is already connected.'),
                                 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Store the access token in the session for later use.
    login_session['access_token'] = credentials.access_token
    login_session['gplus_id'] = gplus_id
    login_session['provider'] = 'google'

    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()
    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']

    # See if a user exists, if it doesn't make a new one
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
    flash("you are now logged in as %s" % login_session['username'])
    print "done!"
    return output

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


# DISCONNECT - Revoke a current user's token and reset their login_session
@app.route('/gdisconnect')
def gdisconnect():
        # Only disconnect a connected user.
    credentials = login_session.get('credentials')
    if credentials is None:
        response = make_response(
            json.dumps('Current user not connected.'), 401)
        response.headers['Content-Type'] = 'application/json'
        # return response
        # redirect customer to the welcome splash on logout
        return redirect('/welcome')
    access_token = login_session.get('credentials')
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % access_token
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]

    if result['status'] == '200':
        # Reset the user's sesson.
        del login_session['credentials']
        del login_session['gplus_id']
        del login_session['username']
        del login_session['email']
        del login_session['picture']

        response = make_response(json.dumps('Successfully disconnected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response
    else:
        # For whatever reason, the given token was invalid.
        response = make_response(
            json.dumps('Failed to revoke token for given user.', 400))
        response.headers['Content-Type'] = 'application/json'
        return response


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'username' in login_session:
            return f(*args, **kwargs)
        else:
            return redirect(url_for('login', next=request.url))
    return decorated_function

# JSON APIs to view Restaurant Information


@app.route('/distraqt/<int:restaurant_id>/menu/JSON')
@login_required
def restaurantMenuJSON(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    items = session.query(MenuItem).filter_by(
        restaurant_id=restaurant_id).all()
    return jsonify(MenuItems=[i.serialize for i in items])

# JSON APIs to view item Information


@app.route('/distraqt/<int:restaurant_id>/menu/<int:menu_id>/JSON')
@login_required
def menuItemJSON(restaurant_id, menu_id):
    Menu_Item = session.query(MenuItem).filter_by(id=menu_id).one()
    return jsonify(Menu_Item=Menu_Item.serialize)

# Deprecated test route - not needed #
# @app.route('/distraqt/JSON')
# @login_required
# def restaurantsJSON():
#     restaurants = session.query(Restaurant).all()
#     return jsonify(restaurants=[r.serialize for r in restaurants])

# create a function decorator to address auth security issues

# Show all restaurants


@app.route('/')
@app.route('/distraqt/')
def showRestaurants():
    """Show all categories"""
    if 'username' not in login_session:
        return redirect('/welcome')
# OLD LOGIC FOR USER AUTHENTICATION - 
    # keeping for possible future use #
    # if 'user.name' == 'restaurant.user':
    # if username not in restaurant.user_id:
    #     return redirect('/login')
    # if restaurant.user == user.id:2
    # if'restaurant.user_id'=='username':
    # restaurants = session.query(Restaurant).order_by
    #(asc(Restaurant.name))
    # #this is the default, since updated
    id = int(login_session['user_id'])
    restaurants = session.query(Restaurant).filter_by(
        user_id=id)  # how to make this by session?
    return render_template('d_restaurants.html',
                           restaurants=restaurants,
                           loginPicUrl=login_session['picture'])


@app.route('/welcome')
def distraqt():
    """render the welcome template"""
    return render_template('d_splash.html')


# Create a new restaurant
@app.route('/distraqt/new/', methods=['GET', 'POST'])
@login_required
def newRestaurant():
    """leverage restaurant paradigm to create a new category"""
    if request.method == 'POST':
        newRestaurant = Restaurant(
            name=request.form['name'],
            user_id=login_session['user_id'])
        session.add(newRestaurant)
        flash('New Restaurant %s Successfully Created' % newRestaurant.name)
        session.commit()
        return redirect(url_for('showRestaurants'))
    else:
        return render_template('d_newRestaurant.html',
                               loginPicUrl=login_session['picture'])

@app.route('/distraqt/<int:restaurant_id>/edit/', methods=['GET', 'POST'])
@login_required
def editRestaurant(restaurant_id):
    """leverage restaurant paradigm to edit the category"""
    # OLD LOGIC FOR USER AUTHENTICATION WITHIN THE APP -
    #keeping for possible future use #
    # if 'username' not in login_session:
    #     return redirect('/login')
    # if user.id != restaurant.user_id:
    #     return redirect('/login')
    editedRestaurant = session.query(
        Restaurant).filter_by(id=restaurant_id).one()
    if request.method == 'POST':
        if request.form['name']:
            editedRestaurant.name = request.form['name']
            flash('Restaurant Successfully Edited %s' %
                  editedRestaurant.name)
            return redirect(url_for('showRestaurants'))
    else:
        return render_template('d_editRestaurant.html',
                               restaurant=editedRestaurant,
                               loginPicUrl=login_session['picture'])


# Delete a restaurant
@app.route('/distraqt/<int:restaurant_id>/delete/', methods=['GET', 'POST'])
@login_required
def deleteRestaurant(restaurant_id):
    """leverage restaurant paradigm to delete the category"""
    # OLD LOGIC FOR USER AUTHENTICATION WITHIN THE APP - keeping for possible future use #
    # if 'username' not in login_session:
    #     return redirect('/login')
    # if user.id != restaurant.user_id:
    #     return redirect('/login')
    restaurantToDelete = session.query(
        Restaurant).filter_by(id=restaurant_id).one()
    if request.method == 'POST':
        session.delete(restaurantToDelete)
        flash('%s Successfully Deleted' % restaurantToDelete.name)
        session.commit()
        return redirect(url_for('showRestaurants',
                                restaurant_id=restaurant_id))
    else:
        return render_template('d_deleteRestaurant.html',
                               restaurant=restaurantToDelete,
                               loginPicUrl=login_session['picture'])


@app.route('/distraqt/<int:restaurant_id>/')
@app.route('/distraqt/<int:restaurant_id>/flowBlocks/')
@login_required
def showMenu(restaurant_id):
    """leverage restaurant/menu paradigm to show all items 
    in a particular category"""
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    items = session.query(MenuItem).filter_by(
        restaurant_id=restaurant_id).all()
    return render_template('d_menu.html', items=items,
                           restaurant=restaurant,
                           loginPicUrl=login_session['picture'])


# Create a new menu item
@app.route('/distraqt/<int:restaurant_id>/flowBlock/new/',
           methods=['GET', 'POST'])
@login_required
def newMenuItem(restaurant_id):
    """leverage restaurant/menu paradigm to create a 
    new item in a particular category"""
# OLD LOGIC FOR USER AUTHENTICATION WITHIN THE APP - 
    # keeping for possible future use #
    # if 'username' not in login_session:
    #     return redirect('/login')
    # if user.id != restaurant.user_id:
    #     return redirect('/login')
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    if request.method == 'POST':
        newItem = MenuItem(name=request.form['name'], description=request.form[
                           'description'],
                           restaurant_id=restaurant_id,
                           user_id=restaurant.user_id)
        session.add(newItem)
        session.commit()
        flash('New Menu %s Item Successfully Created' % (newItem.name))
        return redirect(url_for('showMenu', restaurant_id=restaurant_id))
    else:
        return render_template('d_newmenuitem.html',
                               restaurant_id=restaurant_id,
                               loginPicUrl=login_session['picture'])


@app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/edit',
           methods=['GET', 'POST'])
@login_required
def editMenuItem(restaurant_id, menu_id):
    """leverage restaurant/menu paradigm to edit an 
    item in a particular category"""
# OLD LOGIC FOR USER AUTHENTICATION WITHIN THE APP 
# - keeping for possible future use #
    # if 'username' not in login_session:
    #     return redirect('/login')
    # if user.id != restaurant.user_id:
    # return redirect('/login') #consider updating this to something more
    # graceful
    editedItem = session.query(MenuItem).filter_by(id=menu_id).one()
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    if request.method == 'POST':
        if request.form['name']:
            editedItem.name = request.form['name']
        # if request.form['description']:
        #     editedItem.description = request.form['description']
        # if request.form['price']:
        #     editedItem.price = request.form['price']
        # if request.form['course']:
        #     editedItem.course = request.form['course']
        session.add(editedItem)
        session.commit()
        flash('Menu Item Successfully Edited')
        return redirect(url_for('showMenu', restaurant_id=restaurant_id))
    else:
        return render_template('d_editmenuitem.html',
                               restaurant_id=restaurant_id,
                               menu_id=menu_id,
                               item=editedItem,
                               loginPicUrl=login_session['picture'])


# Delete a menu item
@app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/delete',
           methods=['GET', 'POST'])
@login_required
def deleteMenuItem(restaurant_id, menu_id):
    """leverage restaurant/menu paradigm to delete an 
    item in a particular category"""
# OLD LOGIC FOR USER AUTHENTICATION - 
    #keeping for possible future use #
    # if 'username' not in login_session:
    #     return redirect('/login')
    # if user.id != restaurant.user_id:
    #     return redirect('/login')
    # restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    itemToDelete = session.query(MenuItem).filter_by(id=menu_id).one()
    if request.method == 'POST':
        session.delete(itemToDelete)
        session.commit()
        flash('Menu Item Successfully Deleted')
        return redirect(url_for('showMenu',
                                restaurant_id=restaurant_id))
    else:
        return render_template('d_deleteMenuItem.html',
                               item=itemToDelete,
                               loginPicUrl=login_session['picture'])


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 33507))
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=port)
