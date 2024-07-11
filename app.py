from datetime import timedelta
import random, string
from flask import Flask, jsonify
from configuration.config import Configuration
from configuration.extensions import mongo, bcrypt, jwt
from routes.routes import auth_bp
from flask_cors import CORS
from flask_wtf import CSRFProtect
from flask_wtf.csrf import generate_csrf

app = Flask(__name__)
app.config.from_object(Configuration)
csrf = CSRFProtect(app)
CORS(app, supports_credentials=True, resources={r"/*": {"origins": "http://localhost:3000"}})

'''with open("/SkyClusters-UserAPI/configuration/appMeta.json", "a+") as metadata:
    appMeta = json.load(metadata)
    last_app_start = datetime.strptime(appMeta["last_start"], "%Y-%m-%d")
    current_date = date.today()
    if (current_date - last_app_start).days > 10:
        appMeta["last_start"] = current_date.strftime("%Y-%m-%d")
        metadata.seek(0)
        json.dump(appMeta, metadata)
        metadata.truncate()'''
        
characters = string.ascii_letters + string.digits + string.punctuation
random_string1 = ''.join(random.choice(characters) for _ in range(25))
random_string2 = ''.join(random.choice(characters) for _ in range(25))

app.config["JWT_COOKIE_SECURE"] = False
app.config["JWT_TOKEN_LOCATION"] = ["cookies"]
app.config["JWT_SECRET_KEY"] = random_string1
app.config["SECRET_KEY"] = random_string2  
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=72)

mongo.init_app(app)
bcrypt.init_app(app)
jwt.init_app(app)

@app.route('/')
def index():
    return jsonify({"msg": "SkyClusters User API"})

@auth_bp.route('/get_csrf_token', methods=['GET'])
def get_csrf_token():
    token = generate_csrf()
    return jsonify({'csrf_token': token})

app.register_blueprint(auth_bp, url_prefix='/api/auth')

if __name__ == "__main__":
    app.run(debug=True)