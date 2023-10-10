from app import app
from models import db, User, Prescriber, Prescription, Medicine, BrandMedicine, Appointment

if __name__ == '__main__':
    with app.app_context():
        import ipdb; ipdb.set_trace()
        pass