from database.extension import db
from datetime import datetime

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(50), nullable=False)
    price = db.Column(db.Float, nullable=False)
    description = db.Column(db.Text, nullable=True)
    stock = db.Column(db.Integer, default=0)
    image_url = db.Column(db.String(255), nullable=True)

    def __repr__(self):
        return f'<Product {self.name}>'

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "category": self.category,
            "price": self.price,
            "description": self.description,
            "stock": self.stock,
            "image_url": self.image_url
        }

class User(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    user_name = db.Column(db.String(100), nullable=False)
    user_email = db.Column(db.String(100), unique = True, nullable = False)
    phone_number = db.Column(db.String(12), unique = True, nullable = False)
    user_password = db.Column(db.String(255), nullable = False)
    created_at = db.Column(db.DateTime, default=datetime.now)

    def __repr__(self):
        return f'<User {self.user_name}>'
    def to_dict_user(self):
        return{
            "id": self.id,
            "user_name": self.user_name,
            "user_email": self.user_email,
            "phone_number": self.phone_number,
            "created_at": self.created_at.isoformat()
        }

class ChatMessage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', backref=db.backref('messages', lazy=True))
    
    user_message = db.Column(db.Text, nullable=False)
    bot_response = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.now)
