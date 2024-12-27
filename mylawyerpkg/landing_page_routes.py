from flask import render_template, redirect, flash, session, request
from werkzeug.security import generate_password_hash, check_password_hash
from mylawyerpkg import app
from mylawyerpkg.models import Client, Lawyer, db
from mylawyerpkg.forms import LoginForm


@app.route('/')
def home_page():
    loggedin_client = session.get('loggedin') 
    if loggedin_client: 
        client_det = db.session.query(Client).get(loggedin_client) 
        return render_template('landing_page/index.html', client_det=client_det)
    else:
        client_det = None
    return render_template('landing_page/index.html', client_det=client_det)

@app.route('/home/message/')
def message_flash():
    flash('We Welcome to MYLAWYEr!',category='success')
    return redirect('/home/')

@app.route('/about/')
def about_us():
    return render_template('landing_page/about_us.html')

@app.route('/blog/')
def blog():
    return render_template('landing_page/blog.html')

@app.route('/cor/')
def cor():
    return render_template('landing_page/about.html')



    