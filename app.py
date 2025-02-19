from models import User,Vehicle,Bike,db
from flask_migrate import Migrate
from flask import Flask,request,make_response
from flask_restful import Api,Resource
from flask_jwt_extended import JWTManager,create_access_token,create_refresh_token,jwt_required,get_jwt_identity
import os,secrets,datetime,json
from flask_cors import CORS
from werkzeug.security import check_password_hash,generate_password_hash
import cloudinary
import cloudinary.uploader
import cloudinary.api
from datetime import timedelta

BASE_DIR=os.path.abspath(os.path.dirname(__file__))
DATABASE=os.environ.get(
    "DB_URI", f"sqlite:///{os.path.join(BASE_DIR,'app.db')}"
)
UPLOAD_FOLDER = os.path.join(os.getcwd(), 'static')
ALLOWED_EXTENSIONS=set(['png','jpeg','jpg'])
def allowed_file(filename):
    return '.' in filename and filename.rsplit(".",1)[1].lower() in ALLOWED_EXTENSIONS
app=Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER']=UPLOAD_FOLDER
app.config['SECRET_KEY'] =secrets.token_hex(32)
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(minutes=30)
app.config['JWT_REFRESH_TOKEN_EXPIRES'] = timedelta(days=30)
migrate=Migrate(app,db)
db.init_app(app)
api=Api(app)
jwt=JWTManager(app)


cloudinary.config(
    cloud_name="dia2le5vz",
    api_key="716219668214133",
    api_secret="12Wn1cP9Wc_cZb6gFWMe2tdvHWQ"
)

class Home(Resource):
    def get(self):
        return make_response({"msg":"Get yourself a nice car first"},200)
api.add_resource(Home,'/')


class GetVehicles(Resource):
    def get(self):
        vehicles=Vehicle.query.all()
        if vehicles:
            return make_response([vehicle.to_dict() for vehicle in vehicles],200)
        return make_response({"msg":"No vehicles found"},404)
    
    def post(self):
        data=request.form
        images=request.files.getlist("images")
        required_fields = [
        "name", "price", "seat_material", "year_of_manufacture",
        "current_location", "drive", "millage", "engine_size",
        "fuel_type", "description"
        ]
        missing_fields=[field for field in required_fields if not data.get(field)]
        if missing_fields:
            return make_response({"msg":f"Missing field required:{', '.join(missing_fields)}"},400)
        existing=Vehicle.query.filter_by(name=data.get("name"),year_of_manufacture=data.get("year_of_manufacture")).first()
        if existing:
            return make_response({"msg":"the vehicle already exists"},400)
        image_urls=[]
        for image in images:
            upload_result=cloudinary.uploader.upload(image)
            image_urls.append(upload_result["secure_url"])
        new_vehicle = Vehicle(
        name=data.get("name"),
        price=data.get("price"),
        seat_material=data.get("seat_material"),
        year_of_manufacture=int(data.get("year_of_manufacture")),
        current_location=data.get("current_location"),
        availability=data.get("availability", "available"),
        drive=data.get("drive"),
        millage=data.get("millage"),
        engine_size=data.get("engine_size"),
        fuel_type=data.get("fuel_type"),
        description=data.get("description"),
        image_url=json.dumps(image_urls)
        )
        db.session.add(new_vehicle)
        db.session.commit()
        return make_response(new_vehicle.to_dict(),201)
        

api.add_resource(GetVehicles,'/vehicles')


class VehicleById(Resource):
    def get(self,id):
        vehicle=Vehicle.query.filter_by(id=id).first()
        if vehicle:
            return make_response(vehicle.to_dict(),200)
        return make_response({"msg":"vehicle with the given id does not exist"},404)
    def patch(self,id):
        vehicle=Vehicle.query.filter_by(id=id).first()
        if not vehicle:
            return make_response({"msg":"such a vehicle does not exixts in the database"},404)
        data=request.form
        for attr in data:
            if attr in ['name','price','seat_material','year_of_manufacture','current_location','availability','drive','millage','engine_size','fuel_type','description','image_url']:
                setattr(vehicle,attr,data.get(attr))
        db.session.add(vehicle)
        db.session.commit()
        return make_response(vehicle.to_dict(),200)

api.add_resource(VehicleById,'/vehicle/<int:id>')
        
    


if __name__=='__main__':
    app.run(debug=True)