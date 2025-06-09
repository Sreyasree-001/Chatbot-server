from flask import Blueprint, request, jsonify
from database.extension import db
from werkzeug.security import generate_password_hash, check_password_hash
from database.models import User
from flask_jwt_extended import create_access_token

auth_bp = Blueprint('auth_bp', __name__)

@auth_bp.route("/register", methods=["POST"])
def register():
    try:
        print("Inside try block")
        data = request.get_json()
        print("Data catched properly")
        hashed_password = generate_password_hash(data['password'])
        print("Password hashing done")

        new_user = User(
            user_name=data['username'],
            user_email=data['email'],
            phone_number=data['phoneNumber'],
            user_password=hashed_password
        )

        db.session.add(new_user)
        db.session.commit()

        return jsonify({"message": "User registered successfully"}), 200
    except Exception as e:
        return jsonify("error: ", str(e)),400
    
@auth_bp.route("/login", methods=["POST"])
def login():
    try:
        data = request.get_json()
        user = User.query.filter_by(user_email=data['email']).first()

        if user and check_password_hash(user.user_password, data['password']):
            access_token = create_access_token(identity=user.id)
            return jsonify(token=access_token, message="Login successful"), 200
        return jsonify({"message": "Invalid credentials"}), 401
    except Exception as e:
        return jsonify("error: ", str(e)),400