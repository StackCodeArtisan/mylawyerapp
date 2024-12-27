from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify, abort
from werkzeug.security import check_password_hash, generate_password_hash, check_password_hash
from flask_wtf import FlaskForm
from flask_mail import Mail, Message
from flask_sqlalchemy import SQLAlchemy  

from mylawyerpkg.forms import AdminLoginForm, AppointmentForm
from mylawyerpkg import app, mail
from mylawyerpkg.models import Admin, Client, Lawyer, db, Appointment



@app.route('/appointmentform/', methods=['POST', 'GET'])
def contact():
    appointmentform = AppointmentForm()
    if appointmentform.validate_on_submit():
        fullname = appointmentform.fullname.data
        email = appointmentform.email.data
        message = appointmentform.message.data

        msg = Message(subject = 'Thansks for the email', sender=(fullname,'joshuaolaoluwa@moatcohorts.com.ng'), recipients=[email])
        # msg.body = 'Well done! Thank you for contacting us. We have acknowledged your email.'
        msg.html = '<h2 style = "background:green;color:white;padding:20px">Well done!</h2> <p styl="color:tomato">Thank you for contacting us</p>. <i>We have acknowledged your email</i>.'
        mail.send(msg)
        flash('feedback', 'Email sent successfully')
        return redirect('/contact/')
    
    return render_template('user/contact.html', appointmentform=appointmentform) 



@app.route('/admin/login/', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        record = db.session.query(Admin).filter(Admin.email==email, Admin.password==password).first() 
        if record:  
                hashed_password = record.password
                chek = check_password_hash(hashed_password, password) 
                if chek: 
                    session['loggedin'] = record.id
                    return redirect('/admin/dashboard/') 
                else:
                    flash ('errormsg', 'Invalid Password')
                    return redirect('/admin/login/')
        else:
                flash('errormsg', 'invalid Email')
                return redirect('/admin/login/')
            
    else:
            return render_template('admin/admin_login.html')
# admin login routes ends


@app.route('/admin/view-appointments/')
def view_appointments():
    try:
        # Fetch all appointments with related client and lawyer info
        appointments = db.session.query(Appointment, Client, Lawyer).join(Client).join(Lawyer).all()

        return render_template('admin/view_appointment.html', appointments=appointments)
    
    except Exception as e:
        print(f"Error fetching appointments: {e}")
        return f"An error occurred: {e}"



#admin logout routes begins
@app.route('/admin/logout/')
def admin_logout():
    
    if 'admin_logged_in' in session:
        session.pop('admin_logged_in', None)
        flash('Logged out successfully!', 'success')
    return redirect('/admin/login/')

#admin logour route ends

# Admin Dashboard Route
@app.route('/admin/dashboard/')
def admin_dashboard():
  
    clients = Client.query.all()
    lawyers = Lawyer.query.all()
    return render_template('admin/admin_dashboard.html', clients=clients, lawyers=lawyers)
#Admin dashboard routes ends


# Delete Entry routes
@app.route('/delete/<entry_type>/<int:entry_id>/')
def delete_entry(entry_type, entry_id):
    if entry_type == 'client':
        client = Client.query.get(entry_id)
        if client:
            db.session.delete(client)
            db.session.commit()
            flash(f'Client with ID {entry_id} deleted successfully!', 'success')
        else:
            flash(f'Client with ID {entry_id} not found.', 'error')
    elif entry_type == 'lawyer':
        lawyer = Lawyer.query.get(entry_id)
        if lawyer:
            db.session.delete(lawyer)
            db.session.commit()
            flash(f'Lawyer with ID {entry_id} deleted successfully!', 'success')
        else:
            flash(f'Lawyer with ID {entry_id} not found.', 'error')
    else:
        flash('Invalid entry type specified.', 'error')
    
    return redirect(url_for('admin_dashboard'))

#delete entry routes ends

# Edit Entry Route
@app.route('/edit/<entry_type>/<int:entry_id>/', methods=['GET', 'POST'])
def edit_entry(entry_type, entry_id):
    if entry_type == 'client':
        entry = Client.query.get(entry_id)
    elif entry_type == 'lawyer':
        entry = Lawyer.query.get(entry_id)
    else:
        flash('Invalid entry type specified.', 'error')
        return redirect(url_for('admin_dashboard'))

    if not entry:
        flash(f'{entry_type.capitalize()} with ID {entry_id} not found.', 'error')
        return redirect(url_for('admin_dashboard'))

    if request.method == 'POST':
        entry.name = request.form.get('name')
        entry.email = request.form.get('email')
        db.session.commit()
        flash(f'{entry_type.capitalize()} updated successfully!', 'success')
        return redirect(url_for('admin_dashboard'))

    return render_template('edit_entry.html', entry=entry, entry_type=entry_type)
#edit entry routes ends

@app.route('/admin/appointments/', methods=['GET'])
def admin_dashboard2():
    appointments = Appointment.query.all()
    data = [{
        "id": appt.id,
        "lawyer_id": appt.lawyer_id,
        "client_name": appt.client_name,
        "client_email": appt.client_email,
        "appointment_date": appt.appointment_date,
        "message": appt.message
    } for appt in appointments]
    return jsonify(data)

