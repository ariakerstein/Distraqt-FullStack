Item Catalog Final Project (called distraqt) for full stack nanodegree:
-----------------------------------------------------------------------

This project is based on Udacity's full stack nanodegree building a fully functional webapp containing the following functionality:
* CRUD functionality
* Working postgres database 
* Google authorization (FB authorization is currently deprecated)
* JSON endpoints
* all data is pushed to a postgres db, tables described in 'distraqt_database_setup.py'
* JSON endpoints available via */JSON. Routes are described in 'distraqt_finalProject.py'
e.g., '/distraqt/<int:restaurant_id>/menu/<int:menu_id>/JSON'
* All pages are currently private by user; unauthenticated users will only have access to the welcome page
* Navbar has logic to show login/logout functionality dependent on users auth status. Navbar returns google profile picture.
* Styled using Twitter bootstrap
* JS countdown timer with form submission logic
* Deployed to Heroku

A note on naming conventions. 
The Distraqt project files generally mirror the final project files though prefixed with the convention 'd_*' or 'distraqt_*'.

Folder overview:
- /catalog: contains the main app files 
- /templates: contains html templates
- /static: contains images, /css, /fonts and /js. the /js folder contains scripts.js Timer functionality contained here (definitely NOT part of the project requirements), as well as some jquery and bootstrap libraries.
- /archive: contains the original final project files from the course. these files have been modified for the final project submission and hence have been moved to the archive dustbin, as noted above.

Testing the functionality: 
-- Click the signup button to authenticate with google.  
-- create a new category
-- click on that category to create a new item within the category. This will take the form of a timer flow block
-- save it enter a time in the timer and use the create button (you'll need to pause)
-- Edit/delete functionality exists both at the category and at the item level


Running the Final Project App:
-------------------------------

0. Clone the repo:
$ git clone https://github.com/ariakerstein/Distraqt-FullStack.git

1. Run vagrant and navigate to the relevant folder (assuming this is already configured for purposes of this file):
>>> vagrant up
>>> vagrant ssh

2. install required libraries using pip. 
$ pip install -r requirements.txt

2a. (optional) run the file 'lotsOfDistraqt.py' to generate mock data
$ python lotsOfDistraqt.py

3. Here are several options to run the app:

-- run the file 'distraqt_finalProject.py' locally:
>>> python distraqt_finalProject.py
you should see the server running:
http://0.0.0.0:33507/

-- Or If you have heroku setup to run locally you can run this via heroku local web:

$ heroku local web
you should see the server running, returning something like:
9:32:59 PM web.1 |   * Running on http://0.0.0.0:5000/
9:32:59 PM web.1 |   * Restarting with reloader

-- Note that a fully functional version of the app is running on Heroku that you can reference:
http://distraqted-restaurantmenu.herokuapp.com/

4. Navigate to the app in your browser at e.g., http://0.0.0.0:5000/



