from flask import Blueprint, request, jsonify
from database.extension import db
from database.models import Product

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
    
@product_bp.route('/products', methods=['GET'])
def get_filtered_products():
    print("I am inside filtered product")
    try:
        category = request.args.get('category')
        name = request.args.get('name')
        min_price = request.args.get('min_price', type=float)
        max_price = request.args.get('max_price', type=float)

        # Build base query
        query = Product.query

        if category:
            query = query.filter(Product.category.ilike(f"%{category}%"))
        if name:
            query = query.filter(Product.name.ilike(f"%{name}%"))
        if min_price is not None:
            query = query.filter(Product.price >= min_price)
        if max_price is not None:
            query = query.filter(Product.price <= max_price)

        products = query.all()
        return jsonify([product.to_dict() for product in products])
    except Exception as e:
        return jsonify("error:", str(e)), 400
