from flask import Blueprint, request, jsonify
from database.extension import db
from database.models import Product
from utils.query_parser import parse_query
from flask_jwt_extended import get_jwt_identity, jwt_required
from database.models import ChatMessage

product_bp = Blueprint('product_bp', __name__)

@product_bp.route('/add-product', methods=['POST'])
def add_product():
    print("I am inside add-product")
    data = request.get_json()
    try:
        new_product = Product(
            name=data['name'],
            category=data['category'],
            price=data['price'],
            description=data.get('description'),
            stock=data.get('stock', 0),
            image_url=data.get('image_url')
        )
        db.session.add(new_product)
        db.session.commit()
        return jsonify({"message": "Product added", "product": new_product.to_dict()}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400

@product_bp.route('/get-all-products', methods=['GET'])
def get_all_products():
    print("I am inside get-all-products")
    try:
        products = Product.query.all()
        return jsonify([product.to_dict() for product in products])
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    
# @product_bp.route('/products', methods=['GET'])
# def get_filtered_products():
#     print("I am inside filtered product")
#     try:
#         category = request.args.get('category')
#         name = request.args.get('name')
#         min_price = request.args.get('min_price', type=float)
#         max_price = request.args.get('max_price', type=float)

#         # Build base query
#         query = Product.query

#         if category:
#             query = query.filter(Product.category.ilike(f"%{category}%"))
#         if name:
#             query = query.filter(Product.name.ilike(f"%{name}%"))
#         if min_price is not None:
#             query = query.filter(Product.price >= min_price)
#         if max_price is not None:
#             query = query.filter(Product.price <= max_price)

#         products = query.all()
#         return jsonify([product.to_dict() for product in products]), 201
#     except Exception as e:
#         return jsonify("error:", str(e)), 400

@product_bp.route('/search-products', methods=['GET'])
@jwt_required()
def query_products():
    try:
        user_query = request.args.get("q", "")
        filters = parse_query(user_query)
        user_id = get_jwt_identity()

        query = Product.query

        if filters.get("category"):
            query = query.filter(Product.category.ilike(f"%{filters['category']}%"))
        if filters.get("name"):
            query = query.filter(Product.name.ilike(f"%{filters['name']}%"))
        if filters.get("min_price") is not None:
            query = query.filter(Product.price >= filters['min_price'])
        if filters.get("max_price") is not None:
            query = query.filter(Product.price <= filters['max_price'])

        results = query.all()

        # Format results
        if results:
            product_list = "\n".join([
                f"{p.name} - ₹{p.price} [{p.category}]" for p in results
            ])
            bot_reply = f"Found {len(results)} product(s):\n" + product_list
        else:
            bot_reply = "No products found!"

        # Save message
        message = ChatMessage(
            user_id=user_id,
            user_message=user_query,
            bot_response=bot_reply
        )
        db.session.add(message)
        db.session.commit()

        # Return proper response
        return jsonify([p.to_dict() for p in results]) if results else jsonify({"message": "No products found!"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 400
