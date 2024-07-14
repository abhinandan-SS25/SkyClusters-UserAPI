from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from pymongo import MongoClient
from pymongo.server_api import ServerApi

bcrypt = Bcrypt()
jwt = JWTManager()

mongo_uri = "mongodb+srv://user.hsiypps.mongodb.net/?authSource=%24external&authMechanism=MONGODB-X509&retryWrites=true&w=majority&appName=User"

client = MongoClient(
    mongo_uri,
    tls=True,
    tlsCertificateKeyFile='X509-cert-6226865938273638744.pem',
    server_api=ServerApi('1')
)

def get_mongo_client():
    return client