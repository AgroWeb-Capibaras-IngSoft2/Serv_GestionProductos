from flask import Blueprint, request, jsonify, abort
from Infrastructure.adapterProductRepo import AdapterProductRepo
from application.useCases.CreateProductService import CreateProductService
from application.useCases.GetProductByIdService import GetProductByIdService
from application.useCases.GetAllProductsService import GetAllProductsService
from application.useCases.GetProductsByUserIDService import GetProductsByUserIDService
from observability.MetricsDecorator import monitor_endpoint
import requests
import os
from werkzeug.utils import secure_filename

bp = Blueprint('productos', __name__)
repo = AdapterProductRepo()
create_service = CreateProductService(repo)
get_by_id_service = GetProductByIdService(repo)
get_all_service = GetAllProductsService(repo)
get_by_user_id_service = GetProductsByUserIDService(repo)

def validate_user_exists(user_id):
    resp = requests.get(f"http://localhost:5001/users/getById/{user_id}")
    return resp.status_code == 200

@bp.route("/products", methods=["POST"])
@monitor_endpoint("create_product")
def create_product():
    if not request.content_type.startswith('multipart/form-data'):
        abort(415)
    # Get form fields
    data = request.form.to_dict()
    data["stock"] = int(data["stock"])
    data["price"] = float(data["price"])
    # Get the file
    image = request.files.get('image')
    # Validate required fields except imageUrl
    required_fields = [
        "name", "category", "price", "unit", "stock",
        "origin", "description", "user_id"
    ]
    missing = [f for f in required_fields if f not in data]
    if missing or not image:
        return jsonify({"error": f"Faltan campos obligatorios: {', '.join(missing + (['image'] if not image else []))}"}), 400
    # Validate category and user as before...
    # Temporarily set imageUrl to empty string
    data["imageUrl"] = ""
    try:
        # Create product (generates productId)
        product = create_service.execute(data)
        # Save image with productId as filename
        ext = os.path.splitext(secure_filename(image.filename))[1]
        filename = f"{product.productId}{ext}"
        save_path = os.path.join("static", "catalog", filename)
        image.save(save_path)
        # Update imageUrl
        product.imageUrl = f"http://localhost:5000/static/catalog/{filename}"
        # Save/update product in DB with new imageUrl
        repo.update_image_url(product.productId, product.imageUrl) 
        return jsonify(product.toDictionary()), 201
    except (ValueError, TypeError) as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": "Error interno", "details": str(e)}), 400

@bp.route("/products/<product_id>", methods=["GET"])
@monitor_endpoint("get_product_by_id")
def get_product_by_id(product_id):
    if not isinstance(product_id, str) or not product_id:
        return jsonify({"error": "ID inválido"}), 400
    try:
        product = get_by_id_service.execute(product_id)
        if product is None:
            return jsonify({"error": "Producto no encontrado"}), 404
        return jsonify(product.toDictionary()), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 404
    except Exception as e:
        return jsonify({"error": "Internal server error", "details": str(e)}), 500

@bp.route("/products", methods=["GET"])
@monitor_endpoint("get_all_products")
def get_all_products():
    try:
        products = get_all_service.execute()
        if not products:
            return jsonify([]), 200
        return jsonify([p.toDictionary() for p in products]), 200
    except Exception as e:
        return jsonify({"error": "Error interno", "details": str(e)}), 500
        
@bp.route("/products/user/<user_id>", methods=["GET"])
@monitor_endpoint("get_products_by_user_id")
def get_products_by_user_id(user_id):
    if not isinstance(user_id, str) or not user_id:
        return jsonify({"error": "ID de usuario inválido"}), 400
    try:
        products = get_by_user_id_service.execute(user_id)
        if not products:
            return jsonify([]), 200
        return jsonify([p.toDictionary() for p in products]), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 404
    except Exception as e:
        return jsonify({"error": "Error interno", "details": str(e)}), 500

@bp.route("/test", methods=["GET"])
@monitor_endpoint("test_route")
def test():
    try:
        return "Test route is working!", 200
    except Exception:
        abort(500)