from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import PasswordField, SubmitField, EmailField, StringField, TextAreaField, DateTimeField, TimeField, SelectField
from wtforms.validators import DataRequired, Length

from wtforms.validators import DataRequired, Email



class LoginForm(FlaskForm):
    email = EmailField('Email', validators=[Email(message='please enter email')])
    password = PasswordField('Password ', validators=[DataRequired(message='Password can not be empty')])
    submit = SubmitField('Login')


class Profileform(FlaskForm):
    client_fname = StringField('Client First Name', validators=[])
    client_lname = StringField('Client Last Name', validators=[])
    client_email = EmailField('Email', validators=[Email(message='please enter email')])
    client_phone = TextAreaField('Client Phone', validators=[])
    client_date_registered = StringField('Client Date Registered', validators=[])
    client_gender = StringField('Client Gender', validators=[])
    client_state = StringField('client_state', validators=[])
    client_profile_picture = FileField('Profile Picture', validators=[FileAllowed(['jpg','jpeg','png','gif'], 'Images only')])
    submit = SubmitField('Update')


class LawyerRegisterForm(FlaskForm):
    lawyer_fname = StringField('Lawyer First Name', validators=[DataRequired()])
    lawyer_lname = StringField('Lawyer Last Name', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    cpassword = PasswordField('Confirm Password', validators=[DataRequired(), Length(min=6)])
    lawyer_email = EmailField('Email', validators=[Email(message='please enter email')])
    lawyer_phone = StringField('Lawyer Phone', validators=[DataRequired()])
    lawyer_gender = SelectField ('Lawyer Gender', choices=[('male', 'Male'), ('female', 'Female')],)
    lawyer_state = StringField('Lawyer State', validators=[DataRequired()])
    lawyer_license_number = StringField('Lawyer License Number', validators=[DataRequired()])
    submit = SubmitField('Register Now')


class LawyerLoginForm(FlaskForm):
    email = EmailField('Email', validators=[Email(message='please enter email')])
    password = PasswordField('Password ', validators=[DataRequired(message='Password can not be empty')])
    submit = SubmitField('Login')


class Lawyerform(FlaskForm):
    lawyer_fname = StringField('Lawyer First Name', validators=[])
    lawyer_lname = StringField('Lawyer Last Name', validators=[])
    lawyer_email = EmailField('Email', validators=[Email(message='please enter email')])
    lawyer_phone = TextAreaField('Lawyer Phone', validators=[])
    lawyer_license_number = StringField('Lawyer Last Name', validators=[])
    lawyer_gender = StringField('Lawyer Gender', validators=[])
    lawyer_state= StringField('Lawyer State', validators=[])
    lawyer_specialization = StringField('Lawyer Specialization', validators=[])
    lawyer_date_registered = StringField('Lawyer Date Registered', validators=[])
    lawyer_practice_year = DateTimeField('Lawyer Practice Year', validators=[])
    lawyer_certification_document = StringField('lawyer certification document', validators=[])
    lawyer_price_range_per_hour = StringField('Lawyer Price Per Hour', validators=[])
    lawyer_profile_picture = FileField('Profile Picture', validators=[FileAllowed(['jpg','jpeg','png','gif'], 'Images only')])
    submit = SubmitField('Update')

class AdminLoginForm(FlaskForm):
    email = StringField('email', validators=[DataRequired(), Length(min=4, max=25)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    submit = SubmitField('Login')


class AppointmentForm(FlaskForm):

    full_name = StringField('Full Name', validators=[DataRequired()])
    email = EmailField('Email', validators=[Email(message='please enter email')])
    phone = StringField('Phone', validators=[DataRequired()])
    message = TextAreaField('Message', validators=[DataRequired()])
    appointment_date = DateTimeField('Appointment Date', validators=[DataRequired()])
    appointment_time = TimeField('Appointment Time', validators=[DataRequired()]) 
    send = SubmitField('Send Mail')