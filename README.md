# ToDo's
### video Demo: <https://youtu.be/h_lUhSzUAbk?si=3q0wO9iJV-4ZdoWV>
### Description:-

   # cs50's final project overview
   in the final project I have made todo list aap with the features like register or login to ensure the security of user's data and
   # Screenshots
   ## login page
    this is my login page that allows the registered user only to login to the web application within login route
    the application directly redirects the user to /login
   ![login][static/images/login.png]

  ## register
   This is register page of ToDo's website that allows new users to register into the aap with in /register route
   the application redirects to the /register from login page
   ![register][static/images/register.png]

  ## dashboard
    THis page shows the overview of user's plan and their repective tasks within /dashboard route
   ![dashboard][static/images/todos.png]

   it also includes /logout route that allows the users to logout if they are login in the ToDo's


**project Description**
  ToDo's is a web application designed to help users create structured plans and break them into manageable tasks with assigned due dates. This feature helps users stay organized and focused, minimizing procrastination. The due-date functionality acts as a motivator, encouraging users to complete tasks within the set timeframe, fostering discipline and time management skills.

  If a task remains incomplete beyond its due date, its status automatically updates to "not-active." This subtle yet effective mechanism leverages psychological reinforcement, gently nudging users to cultivate a habit of timely task completion. Over time, users develop better organizational skills that benefit not only their personal lives but also their academic and professional endeavors.

  By promoting accountability and reducing the mental clutter of unfinished work, ToDo's empowers users to achieve their goals systematically, building confidence and productivity.


  # Technologies
  These are the technologies which I have used in my flask aap:
  * Flask  for backend
  * HTML,CSS,Javascript for frontend
  * SQLite 3 to handle user data

### 1. ** FLASK app.py**

  **Description** : A micro-framework written in python
  **Version**     : Flask == '2.0'
  **Purpose**     : used as backend framework for creating web routes and managing requests
  **Libraries**   : os, SQL from cs50 ,flask , flask_session, werkzeug_security,datetime
  **header file** : helpers.py

### used libraries overview

 **os**
  **Descripton**:provide the way of intraction with the operatins system
  **useage** : used to handle configuration settings
  #### Example
  impot os
**cs50**
  **Description** : From the cs50 library I have imported SQL
  **Usage** : to handle SQLite3 queries, also keeps the record of user data in form of table named as users and tasks in this case
  #### Example
  from cs50 import SQL
  db = SQL("sqlite:///site.db")
**Flask**
 **Description**: A framework to handle routes and manage requests
 **usage** : this is used in this web application to handle http routes, render_templates , or redirect to the certain route
 #### Example
 from flask import Flask, render_template, request
 app = Flask(__name__)
**flask_session**
  **Description**: Flask extension used for session managment. It allows you to store data between requests in a session
  **Usage** : used for storing user data such as user_id in this case also users authentication information
  #### Example
   from flask_session import Session
   app.config["SESSION_PERMANENT"] = False
   app.config["SESSION_TYPE"] = "filesystem"
   Session(app)

   ### werkzeug.security
   **Description**: A module for cryptographic operation
   **Usage**      : used to hash and check the password securely
   #### Example
      from werkzeug.security import check_password_hash, generate_password_hash
      password_hash = generate_password_hash("my_secure_password")
 ### Datetime
 **Description**:A module to work with date and time in python
 **usage** : used for handling and formatting dates and time I used it to formate date
 #### Example
 from datetime import date, datetime
 ### Helpers.py costum module
**acknowledgements cs50 Finance$**
 **Description**: it includes custom define apology and login_required function
 **usage**      : apology is used when the user have to tell the user that he did mistake in providing data and login_required is used to limit the certain routes only when the user have logged in
 #### Example
 from helpers import login_required, apology
 @app.route("/dashboard")
 @login_required
 def dashboard():
     return render_template("dashboard.html")

  if not user_name:
     return apology(" you have not entered the user name ",400)


**Installation**
* Clone the repository
* Download the dependies on requirment.txt
* Run the web application on web browser or lacally

**Future Enhancement**
This web application needs to be enhance that I assure you to correct them in the future and also determined to add more features to the aap.
**Acknowledgements**
 This ToDo's project created under the guidence and assistance of chatGpt.com





