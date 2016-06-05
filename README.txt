<<<<<<< HEAD
Distraqt Final Project:
-----------------------

This project is for Udacity's full stack nanodegree - Item Catalog project.
NOTE: There are two versions - one for the restaurant menu app and one for the final project, called 'Distraqt'. The files prefixed with the convention 'd_*' or 'distraqt_*' indicate they are part of the Distraqt final project. Other files have been moved to archive. 

Folder Structure:
This follows a standard Flask app setup:
- templates: contains html templates
- static: contains images, CSS, Fonts and JS
  -- JS folder contains scripts.js. Timer functionality contained here (definitely NOT part of the project requirements)
- archive: contains the original final project files from the course. these files have been modified, permutated for the final project submission and hence have been moved to the archive dustbin, as noted above.


Distraqt Final Project overview:
---------------------------------

This project is based on Udacity's full stack nanodegree building a fully functional webapp containing the following functionality:
* CRUD functiaonlity 
* Working database 
* Deployed to Heroku
* using Google authorization
* JSON endpoints
* Styled using Twitter bootstrap

The Distraqt project files generally mirror the final project files though prefixed with the convention 'd_*' or 'distraqt_*'.


Running the Final Project App:
---------------------------

0. Clone the repo:
$ git clone https://github.com/ariakerstein/RestaurantMenu.git

1. Run vagrant and navigate to the relevant folder (assuming this is already configured for purposes of this file):
>>> vagrant up
>>> vagrant ssh

2. install required libraries using pip. Note that there are some additional libraries not currently being used in the requirements.txt file
$ pip install -r requirements.txt


2a. (optional) run the file 'lotsOfDistraqt.py' to generate mock data
$ python lotsOfDistraqt.py

3. run the file 'distraqt_finalProject.py' locally:
>>> python distraqt_finalProject.py
you should see the server running:
http://0.0.0.0:33507/

If you have heroku setup to run locally you can run this via heroku local web:

$ heroku local web
you should see the server running, returning something like:
9:32:59 PM web.1 |   * Running on http://0.0.0.0:5000/
9:32:59 PM web.1 |   * Restarting with reloader

If for some reason this isn't working you can access this at the following url:
http://distraqted-restaurantmenu.herokuapp.com/

4. Navigate to the app in your browser at e.g., http://0.0.0.0:5000/

5. Testing the functionality: 
Functionality supported:
-- Click the signup button to authenticate with google.  
-- create a new category
-- click on that category to create a new item within the category. This will take the form of a timer flow block
-- save it enter a time in the timer and use the create button (you'll need to pause)
-- Edit/delete functionality exists both at the category and at the item level.

Additional notes:
-------------------
-- all data is pushed to a postgres db, in distraqt_database_setup.py
-- JSON endpoints available via */JSON. Note that all routes are described in distraqt_finalProject.py
e.g., '/distraqt/<int:restaurant_id>/menu/<int:menu_id>/JSON'
-- FB authorization is currently deprecated
-- All pages are currently private by user; unauthenticated users will only have access to the welcome page
-- CRUD functionality exists for both restaurant and item creation levels
-- Navbar has logic to show login/logout functionality dependent on users auth status. Navbar returns google profile picture.


