from flask import Flask, jsonify
from configuration.extensions import bcrypt, jwt, get_mongo_client
from configuration.config import Configuration
from routes.routes import auth_bp
from flask_cors import CORS
from flask_wtf import CSRFProtect
from flask_wtf.csrf import generate_csrf

app = Flask(__name__)
app.config.from_object(Configuration)
csrf = CSRFProtect(app)
CORS(app, supports_credentials=True, resources={r"/*": {"origins": "http://localhost:3000, https://abhinandan-ss25.github.io/SkyClusters-login"}})

'''with open("/SkyClusters-UserAPI/configuration/appMeta.json", "a+") as metadata:
    appMeta = json.load(metadata)
    last_app_start = datetime.strptime(appMeta["last_start"], "%Y-%m-%d")
    current_date = date.today()
    if (current_date - last_app_start).days > 10:
        appMeta["last_start"] = current_date.strftime("%Y-%m-%d")
        metadata.seek(0)
        json.dump(appMeta, metadata)
        metadata.truncate()'''
    
bcrypt.init_app(app)
jwt.init_app(app)

@app.route('/')
def index():
    return jsonify({"msg": "SkyClusters User API"})

@auth_bp.route('/get_csrf_token', methods=['GET'])
def get_csrf_token():
    response = jsonify({'csrf_token': generate_csrf()})
    response.set_cookie('csrf_token', generate_csrf(), samesite='None', secure=True)
    return response

app.register_blueprint(auth_bp, url_prefix='/api/auth')

if __name__ == "__main__":
    app.run(debug=True)