# https://pythonspot.com/login-authentication-with-flask/
#https://pythonspot.com/flask-web-forms/

from flask import Flask
from flask import Flask, flash, redirect, render_template, request, session, abort
import os
from sqlalchemy.orm import sessionmaker
from tabledef import *
engine = create_engine('sqlite:///tutorial.db', echo=True)
 
app = Flask(__name__)
 
@app.route('/')
def home():
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        re = "click  <a href='/stats'>here</a> for stats" + "\n" + "logout <a href='/logout'>Logout</a>" + " Nums <a href='/nums'>Nums</a>"
        return re
 

@app.route('/login', methods=['POST'])
def do_admin_login():
 
    POST_USERNAME = str(request.form['username'])
    POST_PASSWORD = str(request.form['password'])
 
    Session = sessionmaker(bind=engine)
    s = Session()
    query = s.query(User).filter(User.username.in_([POST_USERNAME]), User.password.in_([POST_PASSWORD]) )
    result = query.first()
    if result:
        session['logged_in'] = True
    else:
        flash('wrong password!')
    return home()
 
@app.route("/logout")
def logout():
    session['logged_in'] = False
    return home()

@app.route("/newpage")
def newpage():
    return "newpage!"
 
@app.route("/stats")
def stats():
   if not session.get('logged_in'):
       return render_template('login.html')
   else:
       #return "Hello Boss!  <a href='/logout'>Logout</a>"
       return render_template('stats.html')

@app.route("/nums")
def nums():
   if not session.get('logged_in'):
       return render_template('login.html')
   else:
       #return "Hello Boss!  <a href='/logout'>Logout</a>"
       return render_template('num.html')


if __name__ == "__main__":
    app.secret_key = os.urandom(12)
    app.run(debug=True,host='0.0.0.0', port=4000)

