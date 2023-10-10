#!/usr/bin/env python3

# Standard library imports

# Remote library imports
from flask import Flask, request, make_response, request, session
from flask_restful import Resource
from flask_migrate import Migrate
from flask_cors import CORS

# Local imports
from config import app, db, api
# Add your model imports
from models import db, User, Prescriber, Prescription, Medicine, BrandMedicine, Appointment

# Views go here!
validation_errors = {"errors":["validation errors"]}
class Users(Resource):
    def get(self):
        users = User.query.all()
        users_dict = [user.to_dict() for user in users]
        return make_response(users_dict, 201)
    
    def post(self):
        rq = request.get_json()
        try:
            new_user = User(
                first_name = rq.get('first_name'),
                last_name = rq.get('last_name'),
                username = rq.get('username') ,
                password = rq.get('password')
            )
            db.session.add(new_user)
            db.session.commit()
            return make_response(new_user.to_dict(), 201)
        except:
            return make_response(validation_errors, 400)
api.add_resource(Users, '/users', endpoint = 'users')

class UserbyId(Resource):

    def get(self, id):
        user = User.query.filter(User.id == id).one_or_more()
        
        if user is None:
            return make_response({"error":"User not found"}, 404)
        else:
            return make_response(user.to_dict(), 200)
    
    def delete(self, id ):
        user = User.query.get(id)
        if user:
            db.session.delete(user)
            db.session.commit()
            return make_response({}, 204)
        else:
            return make_response({"error":"User not found"}, 404)

api.add_resource(UserbyId, '/users/')

class Prescriptions(Resource):
    def get(self):
        prescriptions = Prescription.query.all()
        prescriptions_dict = [prescription.to_dict() for prescription in prescriptions]
        return make_response(prescriptions_dict, 201)
    
    def post(self):
        rq = request.get_json()
        try:
            new_prescription = User(
                medication_name = rq.get('medication_name') ,
                instructions = rq.get('instructions') ,
                date_written = rq.get('date_written'),
                medicine_id = rq.get('medication_id'),
                user_id = rq.get('user_id') ,
                prescriber_id = rq.get('prescriber_id') ,
                medication_id = rq.get('medication_id') 
            )
            db.session.add(new_prescription)
            db.session.commit()
            return make_response(new_prescription.to_dict(), 201)
        except:
            return make_response(validation_errors, 400)
    
class PrescriptionsById(Resource):
    def get(self,id):
        prescription = Prescription.query.filter(Prescription.id == id).one_or_more()
        
        if prescription is None:
            return make_response({"error":"Prescription not found"}, 404)
        else:
            return make_response(prescription.to_dict(), 200)
        
    def patch(self, id):
        prescription = Prescription.query.get(id)
        req = request.get_json()
        
        if prescription:
            try:
                for attr in req:
                    setattr(prescription, attr, req.get(attr))
                db.session.commit()

                return make_response(prescription.to_dict(), 202)
            except:
                return make_response(validation_errors, 422)
                
        else:
            return make_response({"error":"Prescription not found"}, 404)

    def delete(self, id ):
        prescription = Prescription.query.get(id)
        if prescription:
            db.session.delete(prescription)
            db.session.commit()
            return make_response({}, 204)
        else:
            return make_response({"error":"Prescription not found"}, 404)

class Prescribers(Resource):
    def get(self):
        prescribers = Prescriber.query.all()
        prescribers_dict = [prescriber.to_dict() for prescriber in prescribers]
        return make_response(prescribers_dict, 201)
    
    def post(self):
        rq = request.get_json()
        try:
            new_prescriber = Prescriber(
                first_name = rq.get('first_name'),
                last_name = rq.get('last_name'),
                npi = rq.get('npi'),
                address = rq.get('address')
            )
            db.session.add(new_prescriber)
            db.session.commit()
            return make_response(new_prescriber.to_dict(), 201)
        except:
            return make_response(validation_errors, 400)


class PresciberById(Resource):
    def get(self,id):
        prescriber = Prescriber.query.filter(Prescriber.id == id).one_or_more()
        
        if prescriber is None:
            return make_response({"error":"Prescriber not found"}, 404)
        else:
            return make_response(prescriber.to_dict(), 200)

    def delete(self, id ):
        prescriber = Prescriber.query.get(id)
        if prescriber:
            db.session.delete(prescriber)
            db.session.commit()
            return make_response({}, 204)
        else:
            return make_response({"error":"Prescriber not found"}, 404)
        

class Medicines(Resource):
    def get(self):
        medicines = Medicine.query.all()
        medicines_dict = [medicine.to_dict() for medicine in medicines]
        return make_response(medicines_dict, 201)

    def post(self):
        rq = request.get_json()
        try:
            new_medicine = Medicine(
                medication_name = rq.get('medication_name'), 
                medication_description = rq.get('medication_description'), 
                ingredients = rq.get('ingredients'), 
                side_effects = rq.get('side_effects'), 
                cost = rq.get('cost') 
            )
            db.session.add(new_medicine)
            db.session.commit()
            return make_response(new_medicine.to_dict(), 201)
        except:
            return make_response(validation_errors, 400)
        
class MedicineById(Resource):
    def get(self,id):
        medicine = Medicine.query.filter(Medicine.id == id).one_or_more()
        
        if medicine is None:
            return make_response({"error":"Medicine not found"}, 404)
        else:
            return make_response(medicine.to_dict(), 200)

    def patch(self, id):
        medicine = Medicine.query.get(id)
        req = request.get_json()
        
        if medicine:
            try:
                for attr in req:
                    setattr(medicine, attr, req.get(attr))
                db.session.commit()

                return make_response(medicine.to_dict(), 202)
            except:
                return make_response(validation_errors, 422)
                
        else:
            return make_response({"error":"Medicine not found"}, 404)
        
    def delete(self, id ):
        medicine = Medicine.query.get(id)
        if medicine:
            db.session.delete(medicine)
            db.session.commit()
            return make_response({}, 204)
        else:
            return make_response({"error":"Medicine not found"}, 404)
        
class BrandMedicines(Resource):
    def get(self):
        brand_medicines = BrandMedicine.query.all()
        brand_medicines_dict = [brand_medicine.to_dict() for brand_medicine in brand_medicines]
        return make_response(brand_medicines_dict, 201)
     
    def post(self):
        rq = request.get_json()
        try:
            new_brand_medicine = BrandMedicine(
                medication_name = rq.get('medication_name'), 
                medication_description = rq.get('medication_description'), 
                ingredients = rq.get('ingredients'), 
                side_effects = rq.get('side_effects'), 
                generic_medicine = rq.get('generic_medicine'),
                cost = rq.get('cost') 
            )
            db.session.add(new_brand_medicine)
            db.session.commit()
            return make_response(new_brand_medicine.to_dict(), 201)
        except:
            return make_response(validation_errors, 400)
    
class BrandMedicineById(Resource):
    def get(self,id):
        brand_medicine = BrandMedicine.query.filter(BrandMedicine.id == id).one_or_more()
        
        if brand_medicine is None:
            return make_response({"error":"Brand Medicine not found"}, 404)
        else:
            return make_response(brand_medicine.to_dict(), 202)
    def patch(self, id):
        brand_medicine = BrandMedicine.query.get(id)
        req = request.get_json()
        
        if brand_medicine:
            try:
                for attr in req:
                    setattr(brand_medicine, attr, req.get(attr))
                db.session.commit()

                return make_response(brand_medicine.to_dict(), 202)
            except:
                return make_response(validation_errors, 422)
                
        else:
            return make_response({"error":"Brand Medicine not found"}, 404)
        
    def delete(self, id ):
        brand_medicine = BrandMedicine.query.get(id)
        if brand_medicine:
            db.session.delete(brand_medicine)
            db.session.commit()
            return make_response({}, 204)
        else:
            return make_response({"error":"Brand Medicine not found"}, 404)
        

class Appointments(Resource):
    def get(self):
        appointments = Appointment.query.all()
        appointments_dict = [appointment.to_dict() for appointment in appointments]
        return make_response(appointments_dict, 201)
    
    def post(self):
        rq = request.get_json()
        try:
            new_appointment = Appointment(
                user_id = rq.get('user_id'),
                appointment_date = rq.get('appointment_date') 
            )
            db.session.add(new_appointment)
            db.session.commit()
            return make_response(new_appointment.to_dict(), 201)
        except:
            return make_response(validation_errors, 400)
        
class AppointmentById(Resource):
    def get(self,id):
        appointment = Appointment.query.filter(Appointment.id == id).one_or_more()
        
        if appointment is None:
            return make_response({"error":"Appointment not found"}, 404)
        else:
            return make_response(appointment.to_dict(), 202)
        
    def patch(self, id):
        appointment = Appointment.query.get(id)
        req = request.get_json()
        
        if appointment:
            try:
                for attr in req:
                    setattr(appointment, attr, req.get(attr))
                db.session.commit()

                return make_response(appointment.to_dict(), 202)
            except:
                return make_response(validation_errors, 422)
                
        else:
            return make_response({"error":"Appointment not found"}, 404)
        
    def delete(self, id ):
        appointment = Appointment.query.get(id)
        if appointment:
            db.session.delete( appointment)
            db.session.commit()
            return make_response({}, 204)
        else:
            return make_response({"error":"Appointment not found"}, 404)


class Signup(Resource):
    def post(self):
        rq = request.get_json()
        User.clear_validation_errors()
        try:
            new_user = User(
                username = rq['username'],
                password_hash = rq['password']
            )
            if new_user.validation_errors:
                raise ValueError
            db.session.add(new_user)
            db.session.commit()

            session['user_id'] = new_user.id

            return new_user.to_dict(), 201
        except:
            errors =  new_user.validation_errors
            new_user.clear_validation_errors()
            return {'errors':'errors'}, 422

api.add_resource(Signup, '/signup', endpoint = 'signup')


class Login(Resource):
    def post(self):
        username = request.get_json()[ 'username' ]
        password = request.get_json()[ 'password' ]

        user = User.query.filter( User.username.like( f'{ username }' ) ).first()

        if user and user.authenticate( password ) :
            session[ 'user_id' ] = user.id
            print( session[ 'user_id' ] )
            return user.to_dict(), 200
        else :
            return { 'errors':['Invalid username or password.'] }, 404

api.add_resource( Login, '/login', endpoint = 'login' )

class Logout ( Resource ) :
    def delete ( ) :
        session[ 'user_id' ] = None
        return {}, 204







if __name__ == '__main__':
    app.run(port=5555, debug=True)

