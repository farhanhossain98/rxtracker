from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.orm import validates
from sqlalchemy import MetaData
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.hybrid import hybrid_property

from config import db

# Models go here!
class User(db.Model, SerializerMixin):
    __tablename__ = 'users'
    id  = db.Column(db.Integer, primary_key = True) 
    first_name  = db.Column(db.String) 
    last_name  = db.Column(db.String) 
    username  = db.Column(db.String) 
    password  = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate = db.func.now())
    
    prescriptions = db.relationship("Prescription", backref = "user")
    appointments = db.relationship("Appointment", backref = 'user')

    serialize_rules = ("-prescriptions.user", "appointments.user")

    def __repr__(self):
        return f'<First Name : {self.first_name}, Last Name: {self.last_name}, Username: {self.username}, Password: {self.password}>'

    @validates('first_name')
    def validate_first_name(self, db_column, first_name):
        if type(first_name) is str and 0 <= len(first_name):
            return first_name
        else:
            return ValueError('First name must be a string')
    @validates('last_name')
    def validate_last_name(self, db_column, last_name):
        if type(last_name) is str and 0 <= len(last_name):
            return last_name
        else:
            return ValueError('Last name must be a string')
    


class Prescription(db.Model, SerializerMixin):
    __tablename__ = "prescriptions"
    id = db.Column(db.Integer, primary_key = True) 
    medication_name =  db.Column(db.String)
    instructions = db.Column(db.String)
    date_written = db.Column(db.DateTime, server_default=db.func.now())
    medicine_id = db.Column(db.Integer)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    prescriber_id = db.Column(db.Integer, db.ForeignKey('prescribers.id'))
    medication_id = db.Column(db.Integer, db.ForeignKey('medicines.id'))
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate = db.func.now())

    @validates('medication_name')
    def validate_medication_name(self, db_column, medication_name):
        if type(medication_name) is str and len(medication_name) > 0:
            return medication_name
        else:
            return ValueError('Medication name must be a string.')
    @validates('instructions')
    def validate_instructions(self, db_column, instructions):
        if type(instructions) is str and len(instructions) > 0:
            return instructions
        else:
            return ValueError('Instructions name must be a string.')
    @validates('medication_id')
    def validate_medication_id(self, db_column, medication_id):
        medicine = Medicine.query.get(medication_id)
        if medicine:
            return medication_id
        else:
            raise Exception('Medication not found.')
    @validates('user_id')
    def validate_user_id(self, db_column, user_id):
        user = User.query.get(user_id)
        if user:
            return user_id
        else:
            raise Exception('User not found.')
    @validates('prescriber_id')
    def validate_prescriber_id(self, db_column, prescriber_id):
        prescriber = Prescriber.query.get(prescriber_id)
        if prescriber:
            return prescriber_id
        else:
            raise Exception('Prescriber not found.')

    serialize_rules = ("-user.prescriptions", "prescriber.prescriptions", "medication.prescriptions")

    def __repr__(self):
        return f'<Medication Name: {self.medication_name}, Instructions: {self.instructions}, Date Written: {self.date_written}, Medicine Id: {self.medication_id}, User Id: {self.user_id}, Presciber Id: {self.prescriber_id}, Medication Id: {self.medication_id}>'


class Prescriber(db.Model, SerializerMixin):
    __tablename__ = 'prescribers'
    id  = db.Column(db.Integer,  primary_key = True)
    first_name = db.Column(db.String)
    last_name = db.Column(db.String)
    npi = db.Column(db.Integer)
    address = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate = db.func.now())

    prescriptions = db.relationship("Prescription", backref = "prescriber")
    appointments = db.relationship("Appointment", backref = 'prescriber')


    serialize_rules = ("-prescriptions.prescriber","-appointments.prescriber")

    @validates('first_name')
    def validate_first_name(self, db_column, first_name):
        if type(first_name) is str and 0 <= len(first_name):
            return first_name
        else:
            return ValueError('First name must be a string')
    @validates('last_name')
    def validate_last_name(self, db_column, last_name):
        if type(last_name) is str and 0 <= len(last_name):
            return last_name
        else:
            return ValueError('Last name must be a string')
        
    @validates('npi')
    def validate_npi(self, db_column, npi):
        if type(npi) is int and len(str(int)) is 10:
            return npi 
        else:
            return ValueError('NPI must have 10 digits')
    
    def __repr__(self):
        return f'<First Name : {self.first_name}, Last Name: {self.last_name}, Npi: {self.npi}, Password: {self.address}>'

class Medicine(db.Model, SerializerMixin):
    __tablename__ = 'medicines'
    id = db.Column(db.Integer, primary_key = True)
    medication_name = db.Column(db.String)
    medication_description = db.Column(db.String)
    ingredients = db.Column(db.String)
    side_effects = db.Column(db.String)
    cost = db.Column(db.Integer)
    brand_medicine_id = db.Column(db.Integer, db.ForeignKey('brand_medicines.id'))
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate = db.func.now())

    prescriptions = db.relationship("Prescription", backref = "medicine")

    serialize_rules = ("-prescriptions.medicine",)


    @validates('brand_medicine_id')
    def validate_brand_medicine_id(self, db_column, brand_medicine_id):
        brand_medicine = BrandMedicine.query.get(brand_medicine_id)
        if brand_medicine:
            return brand_medicine_id
        else:
            raise Exception('Medicine not found.')

    @validates('medication_name')
    def validate_medication_name(self, db_column, medication_name):
        if type(medication_name) is str and len(medication_name) > 0:
            return medication_name
        else:
            return ValueError('Medication name must be a string.')
    @validates('medication_description')
    def validate_medication_description(self, db_column, medication_description):
        if type(medication_description) is str and len(medication_description) > 0:
            return medication_description
        else:
            return ValueError('Medication description must be a string.')

    def __repr__(self):
        return f'<Medication Name: {self.medication_name}, Medication Description: {self.medication_description}, Ingredients: {self.ingredients}, Side Effects: {self.side_effects}, Cost: {self.cost}>'
    @validates('ingredients')
    def validate_ingredients(self, db_column, ingredients):
        if type(ingredients) is str and len(ingredients) > 0:
            return ingredients
        else:
            return ValueError('Ingredients must be a string.')
        
    @validates('side_effects')
    def validate_side_effects(self, db_column, side_effects):
        if type(side_effects) is str and len(side_effects) > 0:
            return side_effects
        else:
            return ValueError('Side effects must be a string.')
        
    @validates('cost')
    def validate_cost(self, db_column, cost):
        if type(cost) is int and cost >= 0:
            return cost
        else:
            return ValueError('Cost must be an integer. ')

class BrandMedicine(db.Model, SerializerMixin):
    __tablename__ = "brand_medicines"
    id = db.Column(db.Integer, primary_key = True)
    medication_name = db.Column(db.String)
    medication_description = db.Column(db.String)
    ingredients = db.Column(db.String)
    side_effects = db.Column(db.String)
    generic_medicine = db.Column(db.String)
    cost = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate = db.func.now())

    medicines = db.relationship("Medicine", backref = 'brand_medicine')



    @validates('medication_name')
    def validate_medication_name(self, db_column, medication_name):
        if type(medication_name) is str and len(medication_name) > 0:
            return medication_name
        else:
            return ValueError('Medication name must be a string.')
    @validates('medication_description')
    def validate_medication_description(self, db_column, medication_description):
        if type(medication_description) is str and len(medication_description) > 0:
            return medication_description
        else:
            return ValueError('Medication description must be a string.')

    def __repr__(self):
        return f'<Medication Name: {self.medication_name}, Medication Description: {self.medication_description}, Ingredients: {self.ingredients}, Side Effects: {self.side_effects}, Cost: {self.cost}>'
    @validates('ingredients')
    def validate_ingredients(self, db_column, ingredients):
        if type(ingredients) is str and len(ingredients) > 0:
            return ingredients
        else:
            return ValueError('Ingredients must be a string.')
        
    @validates('side_effects')
    def validate_side_effects(self, db_column, side_effects):
        if type(side_effects) is str and len(side_effects) > 0:
            return side_effects
        else:
            return ValueError('Side effects must be a string.')
        
    @validates('cost')
    def validate_cost(self, db_column, cost):
        if type(cost) is int and cost >= 0:
            return cost
        else:
            return ValueError('Cost must be an integer. ')
        
    
    def __repr__(self):
        return f'<Medication Name: {self.medication_name}, Medication Description: {self.medication_description}, Ingredients: {self.ingredients}, Side Effects: {self.side_effects}, Generic Medicine:{self.generic_medicine}, Cost: {self.cost}, Medicine Id: {self.medicine_id}>'

class Appointment(db.Model, SerializerMixin):
    __tablename__ = "appointments"
    id = db.Column(db.Integer, primary_key = True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    prescriber_id = db.Column(db.Integer, db.ForeignKey('prescribers.id'))
    appointment_date = db.Column(db.Date)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate = db.func.now())

    serialize_rules = ("-user.appointments", "prescriber.appointments")

    @validates('user_id')
    def validate_user_id(self, db_column, user_id):
        user = User.query.get(user_id)
        if user:
            return user_id
        else:
            raise Exception('User not found.')
    @validates('prescriber_id')
    def validate_prescriber_id(self, db_column, prescriber_id):
        prescriber = Prescriber.query.get(prescriber_id)
        if prescriber:
            return prescriber_id
        else:
            raise Exception('Prescriber not found.')
        
        
    # @validates('appointment_date')
    # def validate_appointment_date(self, db_column, appointment_date):
    #     if type(appointment_date) is 
        




    def __repr__(self):
        return f'<User Id: {self.user_id}, Appointment Date: {self.appointment_date}>'
