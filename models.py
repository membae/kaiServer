from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy_serializer import SerializerMixin

metadata=MetaData()
db=SQLAlchemy(metadata=metadata)


class User(db.Model,SerializerMixin):
    __tablename__="users"
    
    id=db.Column(db.Integer,primary_key=True)
    first_name=db.Column(db.String,nullable=False)
    last_name=db.Column(db.String,nullable=False)
    email=db.Column(db.String,unique=True,nullable=False)
    password=db.Column(db.String,nullable=False)
    phone=db.Column(db.Integer,nullable=False)
    role=db.Column(db.String,default="customer")
    
    
class Vehicle(db.Model,SerializerMixin):
    __tablename__="vehicles"
    
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String,nullable=False)
    price=db.Column(db.Integer,nullable=False)
    seat_material=db.Column(db.String,nullable=False)
    year_of_manufacture=db.Column(db.Integer,nullable=False)
    current_location=db.Column(db.String,nullable=False)
    availability=db.Column(db.String,nullable=False,default='available')
    drive=db.Column(db.String,nullable=False)
    millage=db.Column(db.String,nullable=False)
    engine_size=db.Column(db.String,nullable=False)
    fuel_type=db.Column(db.String,nullable=False)
    description=db.Column(db.String,nullable=False)
    image_url=db.Column(db.String,nullable=False)


class Bike(db.Model,SerializerMixin):
    __tablename__="bikes"
    
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String,nullable=False)
    price=db.Column(db.Integer,nullable=False)
    year_of_manufacture=db.Column(db.Integer,nullable=False)
    current_location=db.Column(db.String,nullable=False)
    availability=db.Column(db.String,nullable=False,default='available')
    millage=db.Column(db.String,nullable=False)
    engine_size=db.Column(db.String,nullable=False)
    fuel_type=db.Column(db.String,nullable=False)
    description=db.Column(db.String,nullable=False)
    image_url=db.Column(db.String,nullable=False)
    