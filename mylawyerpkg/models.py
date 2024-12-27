from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()



class Admin(db.Model):
    __tablename__ = 'admin'
    admin_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(120), unique=True, nullable=True)
    password = db.Column(db.String(300), nullable=True)
    last_logged_in_date = db.Column(db.DateTime, default=datetime.utcnow)



class Lga(db.Model):
    __tablename__ = 'lga'
    lga_id = db.Column(db.Integer, primary_key=True, autoincrement=False)
    lga_name = db.Column(db.String(100), nullable=False)
    lga_state = db.Column(db.Integer(), db.ForeignKey('state.state_id'), nullable=False)


class State(db.Model):
    __tablename__ = 'state'
    state_id = db.Column(db.Integer, primary_key=True, autoincrement=False)
    state_name = db.Column(db.String(100), nullable=False, index=False)
    clients = db.relationship('Client', backref='state', lazy=True)
    lgas = db.relationship('Lga', backref='state')


class Client(db.Model):
    __tablename__ = 'client'
    client_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    client_fname = db.Column(db.String(50), nullable=True)
    client_lname = db.Column(db.String(50), nullable=True)
    client_email = db.Column(db.String(100), unique=True, nullable=True)
    client_phone = db.Column(db.String(50), unique=True, nullable=True)
    client_date_registered = db.Column(db.DateTime, default=datetime.utcnow)
    client_password = db.Column(db.String(300), nullable=True)
    client_profile_picture = db.Column(db.Text,)
    client_gender = db.Column(db.Enum('female', 'male'), nullable=True)
    client_state = db.Column(db.String(100), nullable=True)
    state_id = db.Column(db.Integer, db.ForeignKey('state.state_id'), nullable=True)
    appointments = db.relationship('Appointment',back_populates='client', lazy=True)
    cases = db.relationship('Case', backref='client', lazy=True)


class Lawyer(db.Model):
    __tablename__ = 'lawyer'
    lawyer_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    lawyer_fname = db.Column(db.String(50), nullable=False)
    lawyer_lname = db.Column(db.String(50), nullable=True)
    lawyer_gender = db.Column(db.Enum('female', 'male'), nullable=True)
    lawyer_availability_status = db.Column(db.Enum('yes', 'no'), nullable=True)
    lawyer_license_number = db.Column(db.String(50), nullable=True, unique=True)
    lawyer_email = db.Column(db.String(100), unique=True, nullable=True)
    lawyer_phone = db.Column(db.String(50), unique=True, nullable=True)
    lawyer_password = db.Column(db.String(300), nullable=True)
    lawyer_state = db.Column(db.String(100), nullable=True)
    lawyer_practice_year = db.Column(db.DateTime, default=datetime.utcnow)
    lawyer_date_registered = db.Column(db.DateTime, default=datetime.utcnow)
    lawyer_certification_document = db.Column(db.String(50), nullable=True)
    lawyer_profile_picture = db.Column(db.Text, nullable=False)
    lawyer_price_range_per_hour = db.Column(db.String(200), nullable=True)
    lawyer_specialization = db.Column(db.String(200), nullable=True)
    state_id = db.Column(db.Integer, db.ForeignKey('state.state_id'), nullable=True)
    specialization_id = db.Column(db.Integer, db.ForeignKey('specialization.specialization_id'), nullable=True)
    appointments = db.relationship('Appointment', back_populates='lawyer')
    documents = db.relationship('Document', backref='lawyer', lazy=True)
    state = db.relationship('State', backref='lawyer', lazy=True)


class Appointment(db.Model):
    __tablename__ = 'appointments'

    appointment_id = db.Column(db.Integer, primary_key=True)
    appointment_date = db.Column(db.Date, nullable=False)
    appointment_time = db.Column(db.Time, nullable=False)
    appointment_note = db.Column(db.Text)
    appointment_price = db.Column(db.Float, nullable=False)
    client_id = db.Column(db.Integer, db.ForeignKey('client.client_id'), nullable=False)  # ForeignKey to Client
    lawyer_id = db.Column(db.Integer, db.ForeignKey('lawyer.lawyer_id'), nullable=False)  # ForeignKey to Lawyer

    # Relationship with Client and Lawyer
    client = db.relationship('Client', back_populates='appointments')
    lawyer = db.relationship('Lawyer', back_populates='appointments')



class Case(db.Model):
    __tablename__ = 'case'
    case_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    case_date_added = db.Column(db.DateTime, default=datetime.utcnow)
    case_description = db.Column(db.String(200), nullable=True)
    client_id = db.Column(db.Integer, db.ForeignKey('client.client_id'), nullable=True)
    specialization_id = db.Column(db.Integer, db.ForeignKey('specialization.specialization_id'), nullable=True)


class Document(db.Model):
    __tablename__ = 'document'
    document_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    document_name = db.Column(db.String(100), nullable=True)
    document_file = db.Column(db.String(100), nullable=True)
    document_date_added = db.Column(db.DateTime, default=datetime.utcnow)
    lawyer_id = db.Column(db.Integer, db.ForeignKey('lawyer.lawyer_id'), nullable=True)


class Specialization(db.Model):
    __tablename__ = 'specialization'
    specialization_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    specialization_name = db.Column(db.String(100), nullable=False, unique=True)
    cases = db.relationship('Case', backref='specialization', lazy=True)
    lawyers = db.relationship('Lawyer', backref='specialization', lazy=True)


class Payment(db.Model):
    __tablename__ = 'payment'
    payment_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    payment_date = db.Column(db.DateTime, default=datetime.utcnow)
    payment_status = db.Column(db.String(50), nullable=False)
    reference_number = db.Column(db.String(50), nullable=False, unique=True)
    appointment_id = db.Column(db.Integer, db.ForeignKey('appointments.appointment_id'), nullable=False)
    lawyer_id = db.Column(db.Integer, db.ForeignKey('lawyer.lawyer_id'), nullable=True)
    client_id = db.Column(db.Integer, db.ForeignKey('client.client_id'), nullable=False)


class Review(db.Model):
    __tablename__ = 'review'
    review_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    review_content = db.Column(db.Text, nullable=False)
    review_date = db.Column(db.DateTime, default=datetime.utcnow)
    appointment_id = db.Column(db.Integer, db.ForeignKey('appointments.appointment_id'), nullable=False)
    client_id = db.Column(db.Integer, db.ForeignKey('client.client_id'), nullable=False)
    lawyer_id = db.Column(db.Integer, db.ForeignKey('lawyer.lawyer_id'), nullable=False)






   
    




    

