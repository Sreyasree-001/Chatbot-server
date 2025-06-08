from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text 
#import os
from database.models import Product
from routes.product_routes import product_bp
from database.extension import db

app = Flask(__name__)
app.secret_key = 'supersecretkey'  # for session management
CORS(app)

# MySQL credentials
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:Sreyasree27@127.0.0.1:3307/chatbotdb'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

# Register your blueprint
app.register_blueprint(product_bp)

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

print("Registered routes:")
print(app.url_map)


if __name__ == '__main__':
    app.run(debug=True)
