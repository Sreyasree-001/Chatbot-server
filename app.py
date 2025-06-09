from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text 

from database.models import Product
from routes.product_routes import product_bp
from database.extension import db
from routes.auth_routes import auth_bp

from flask_jwt_extended import JWTManager, create_access_token
from datetime import timedelta
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('SUPER_SECRET_KEY')
CORS(app)

# MySQL credentials
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

#JWT configure
app.config["JWT_SECRET_KEY"] = os.getenv('SECRET_KEY')
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=1)

# Register the blueprints
app.register_blueprint(product_bp, url_prefix='/api')
app.register_blueprint(auth_bp, url_prefix='/api')

@app.route("/test-db")
def test_db():
    try:
        db.session.execute(text('SELECT 1'))
        return "Connected to MySQL successfully!"
    except Exception as e:
        return f"MySQL error: {e}"

@app.route('/')
def home():
    return "E-commerce Chatbot Backend Running!"

# print("Registered routes:")
# print(app.url_map)


if __name__ == '__main__':
    app.run(debug=True)
