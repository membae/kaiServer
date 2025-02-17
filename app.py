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




if __name__=='__main__':
    app.run(debug=True)