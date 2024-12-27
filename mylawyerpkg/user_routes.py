import requests, json, random, os, secrets
from flask import render_template, redirect, flash, request, session, url_for, jsonify
from sqlalchemy import or_
from werkzeug.security import generate_password_hash, check_password_hash
from flask_mail import Message
from mylawyerpkg import app, db, mail
from mylawyerpkg.models import Client,State
from mylawyerpkg.models import db, Client, Appointment, Lawyer
from mylawyerpkg.forms import LoginForm, Profileform, AppointmentForm
  


#user signup routes
@app.route('/user/signup/', methods=['POST', 'GET'])
def user_sign_up():
    if request.method == 'GET':
        return render_template('users/signup.html')
    else:
        firstname = request.form.get('ufirstname')
        secondname = request.form.get('usecondname')
        email  = request.form.get('uemail') 
        password = request.form.get('upassword')
        cpassword = request.form.get('cupassword')
        if password != cpassword:
            flash('errormsg', 'password mismatch, please try again')
            return redirect('/user/signup/')
        else:
            hashed = generate_password_hash(password)
            user = Client(client_fname=firstname, client_lname=secondname, client_password=hashed, client_email=email)
            db.session.add(user)
            db.session.commit()
            flash('feedback', 'An account has been created for you, please login')
            return redirect('/user/login/')
#user signup routes ends

#user login routes


@app.route('/user/login/', methods=['GET','POST'])
def user_login():
    loginform = LoginForm() 
    if request.method == 'GET':
        return render_template('users/login.html', loginform=loginform)
    else: 
        if loginform.validate_on_submit():
            email = loginform.email.data
            password = loginform.password.data
            record = db.session.query(Client).filter(Client.client_email==email).first() 
            if record:  
                hashed_password = record.client_password
                chek = check_password_hash(hashed_password, password) 
                if chek: 
                    session['loggedin'] = record.client_id
                    return redirect('/user/profile/') 
                else:
                    flash ('errormsg', 'Invalid Password')
                    return redirect('/user/login/')
            else:
                flash('errormsg', 'invalid Email')
                return redirect('/user/login/')
            
        else:
            return render_template('users/login.html', loginform=loginform)

#user login routes ends

#user logout routes

@app.route('/user/logout/')
def user_logout():
    session.pop('loggedin', None)
    flash('feedback', 'you have logged out')
    return redirect('/login/')

#logout routes ends


#user profile routes

@app.route('/user/profile/', methods=['POST', 'GET'])
def user_dashboard():
    loggedin_client = session.get('loggedin')
    cform = Profileform()
    if loggedin_client:
        states = State.query.all()
        client_deets = Client.query.get(loggedin_client)       
        client_deets = db.session.query(Client).get(loggedin_client)
        cform.client_fname.data = client_deets.client_fname
        cform.client_lname.data = client_deets.client_lname
        cform.client_email.data = client_deets.client_email
        cform.client_phone.data = client_deets.client_phone
        cform.client_state.data = client_deets.client_state 
        cform.client_date_registered.data = client_deets.client_date_registered
        cform.client_gender.data = client_deets.client_gender   
        cform.client_profile_picture.data = client_deets.client_profile_picture
               
        if cform.validate_on_submit():
            
            file = cform.client_profile_picture.data
            _,ext = os.path.split(file.filename)
            rand_str = secrets.token_hex(10)
            filename = f'{rand_str}{ext}'
            file.save(f'pkg/static/uploads/{filename}')
            client_deets.client_profile_picture = filename


            client_deets.client_profile_picture = filename
            client_deets.client_fname = cform.client_fname.data
            client_deets.client_lname = cform.client_lname.data
            client_deets.client_email = cform.client_email.data
            client_deets.client_phone = cform.client_phone.data
            client_deets.client_state = cform.client_state.data
            client_deets.client_date_registered = cform.client_date_registered.data
            
            db.session.commit()
            flash('feedback', 'Profile details updated successfully!')
            return redirect('/user/profile/')
        
        return render_template('users/client_profile_page.html', client_deets=client_deets, cform=cform, states=states)
    else:
        flash('errormsg', 'Client details not found')
        return redirect('/user/login/')


#user profile routes ends

#user profile update routes

@app.route('/profile/<client_id>/update/', methods=['POST', 'GET'])
def update_profile(client_id):
    loggedin_client = session.get('loggedin')
    if loggedin_client:
        client_deets = db.session.query(Client).get(client_id)
        
   
        if request.method == 'POST':    
            client_fname = request.form.get('client_fname')
            client_lname = request.form.get('client_lname')
            client_email = request.form.get('client_email')
            client_phone = request.form.get('client_phone')
            client_gender = request.form.get('client_gender')
            client_state = request.form.get('client_state')
            client_date_registered = request.form.get('client_date_registered')

            allowed_ext =['.jpg','.jpeg','.png','.gif']
            file = request.files.get('client_profile_picture')
            _,ext = os.path.splitext(file.filename)
            rand_str = secrets.token_hex(10)
            
            if ext in allowed_ext:
                filename = f'{rand_str}{ext}'
                file.save(f'mylawyerpkg/static/uploads/{filename}')
            else:
                flash('errormsg','You cover image must be an image file')
                return redirect ('/user/profile/')

            client_deets.client_fname = client_fname
            client_deets.client_lname = client_lname
            client_deets.client_email = client_email
            client_deets.client_phone = client_phone
            client_deets.client_gender = client_gender
            client_deets.client_state = client_state
            client_deets.client_date_registered = client_date_registered
            client_deets.client_profile_picture = filename
            db.session.commit()
            flash('feedback','Profile details Updated successfully!')
            return redirect ('/user/profile/')
        else:
            return redirect('/user/profile/')
    else:
        flash('errormsg', 'you must be logged in')
        return redirect('/user/login/')
    

#user profile updates routes ends

## Appointment booking Routes

@app.route('/book/appointment/', methods=['POST','GET'])
def book_appointment():
    loggedin_client = session.get('loggedin')
    if loggedin_client:
        client_deets = Client.query.get(loggedin_client)
        if request.method == 'GET':
            return render_template('forms/appointment_form.html', client_deets=client_deets)
        else:
            client_name = request.form.get('clientName')
            client_email = request.form.get('clientEmail')
            appointmentdate = request.form.get('appointmentDate')
            messages = request.form.get('message')
            price = request.form.get('clientPrice')
        

        info = Appointment(appointment_date=appointmentdate, appointment_note=messages, appointment_price=price)
        db.session.add(info)
        db.session.commit()

    return render_template('forms/appointment_form.html', client_deets=client_deets)
   


#appointments booking routes ends

@app.route('/search-lawyers/', methods=['GET'])
def search_lawyers():
    query = request.args.get('query', '').strip()
    if query:
        results = Lawyer.query.filter(
            or_(
                Lawyer.lawyer_fname.ilike(f'%{query}%'),
                Lawyer.lawyer_lname.ilike(f'%{query}%'),
                Lawyer.lawyer_profile_picture.ilike(f'%{query}%'),
                Lawyer.lawyer_email.ilike(f'%{query}%'),
                Lawyer.lawyer_phone.ilike(f'%{query}%'),
                Lawyer.lawyer_specialization.ilike(f'%{query}%'),
                Lawyer.lawyer_state.ilike(f'%{query}%'),
                Lawyer.lawyer_license_number.ilike(f'%{query}%')
            )
        ).all()
    else:
        results = Lawyer.query.all()

    lawyers_data = [
        {
            "id": lawyer.lawyer_id,
            "name": f"{lawyer.lawyer_fname} {lawyer.lawyer_lname}",
            "picture": lawyer.lawyer_profile_picture,
            "email": lawyer.lawyer_email,
            "phone": lawyer.lawyer_phone,
            "specialization": lawyer.lawyer_specialization,
            "state": lawyer.lawyer_state,
            "license_number": lawyer.lawyer_license_number
        }
        for lawyer in results
    ]
    return jsonify(lawyers_data)
#appointment confirmation routes
@app.route("/appointment/confirmation/", methods=['GET','POST'])
def confirmation():
     

    name = request.args.get("name", "Valued Client")  
    return render_template("users/appointment_confirm.html", name=name)

#appointment confirmation routes ends


@app.route('/sendmail/', methods=['POST', 'GET'])
def send_mail_to_lawyer():
    appointmentform = AppointmentForm()
    
    # Fetch lawyers from the database
    lawyers = Lawyer.query.all()  # Assuming `Lawyer` is the model for lawyers

    if appointmentform.validate_on_submit():
        fullname = appointmentform.full_name.data
        email = appointmentform.email.data
        message = appointmentform.message.data
        lawyer_email = request.form.get('Lawyer.lawyer_email')  # Get selected lawyer's email from the form

        if not lawyer_email:
            flash('Please select a lawyer to send the email.', 'error')
            return redirect('/sendmail/')

        # Create and send the email
        try:
            msg = Message(
                subject='Appointment Booking',
                sender=(fullname, 'joshuaolaoluwa@moatcohorts.com.ng'),
                recipients=[Lawyer.lawyer_email]  # Send to the selected lawyer
            )
            msg.body = message
            mail.send(msg)
            flash('Email sent successfully to the selected lawyer.', 'success')
            return redirect('/sendmail/')
        except Exception as e:
            flash(f'Error sending email: {str(e)}', 'error')
            return redirect('/sendmail/')
    
    return render_template('admin/sendmail.html', appointmentform=appointmentform, lawyers=lawyers)
