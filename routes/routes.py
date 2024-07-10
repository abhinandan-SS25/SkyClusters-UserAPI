import datetime
from flask import Blueprint, request, jsonify
from configuration.extensions import mongo, bcrypt, jwt
from models.models import User
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, set_access_cookies, unset_jwt_cookies
from models.forms.management import RegistrationForm, LoginForm

auth_bp = Blueprint('auth_bp', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    form = RegistrationForm(request.form)

    if form.validate():
        username = form.username.data
        email = form.email.data
        password = form.password.data
        comfirm_password = form.confirm.data

        if password != comfirm_password:
            return jsonify({"msg": "Password and Confirm Password do not match."}), 400

        if User.find_by_email(email):
            return jsonify({"msg": "An account has already been created with this Email address."}), 400

        if User.find_by_username(username):
            return jsonify({"msg": "This username is already taken."}), 400

        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        user = {
            "username": username, 
            "email": email, 
            "password": hashed_password, 
            "is_verified": False, 
            "joined_at": datetime.now(), 
            "last_login": None
        }

        try:
            result = User.insert(user)
            if result.inserted_id:
                return jsonify({"msg": f"{username} registered successfully."}), 200
            else:
                return jsonify({"msg": f"Failed to register {username}"}), 500
        except Exception as e:
            return jsonify({"msg": "Failed to register user", "error": str(e)}), 500
    else:
        errors = form.errors
        return jsonify({"msg": "Please provide appropriate data", "errors": errors}), 400

    return jsonify({"msg": "An error occurred."}), 500

@auth_bp.route('/login', methods=['POST'])
def login():
    form = LoginForm(request.form)

    if form.validate():
        email = form.email.data
        password = form.password.data

        user = User.find_by_email(email)
        if user and bcrypt.check_password_hash(user['password'], password):
            try:
                User.update_last_login(user['_id'], datetime.now())
            except Exception as e:
                pass
                # return jsonify({'msg': 'Failed to update last login', 'error': str(e)}), 500
            
            response = jsonify({"msg": "Succcessfully logged in.", })
            access_token = create_access_token(identity=user['_id'])
            set_access_cookies(response, access_token)
            return response, 200

        return jsonify({'msg': 'Invalid email or password. Please check your detials.'}), 401

@auth_bp.route('/protected', methods=['GET'])
@jwt_required()
def protected():
    current_user_id = get_jwt_identity()
    user = mongo.db.users.find_one({"_id": current_user_id})
    return jsonify(logged_in_as=user['username']), 200

@auth_bp.route("/logout", methods=["POST"])
def logout():
    response = jsonify({"msg": "Logged out successfully."})
    unset_jwt_cookies(response)
    return response