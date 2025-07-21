from flask import Blueprint, request, jsonify, abort
from Infrastructure.adapterProductRepo import AdapterProductRepo
from application.useCases.CreateProductService import CreateProductService
from application.useCases.GetProductByIdService import GetProductByIdService
from application.useCases.GetAllProductsService import GetAllProductsService
from application.useCases.GetProductsByUserIDService import GetProductsByUserIDService
from observability.MetricsDecorator import monitor_endpoint
import requests

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
    if not request.is_json:
        abort(415)
    data = request.get_json()
    required_fields = [
    "name", "category", "price", "unit", "imageUrl", "stock",
    "origin", "description", "isActive", "user_id"
    ]
    # The rest (originalPrice, isOrganic, isBestSeller, freeShipping) are optional
    # productId is auto-generated and should not be provided by client
    missing = [f for f in required_fields if f not in data]
    if missing:
        return jsonify({"error": f"Faltan campos obligatorios: {', '.join(missing)}"}), 400
    if not validate_user_exists(data.get("user_id")):
        return jsonify({"error": "Usuario no encontrado"}), 404
    try:
        product = create_service.execute(data)
        return jsonify(product.toDictionary()), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception:
        abort(500)

@bp.route("/products/<product_id>", methods=["GET"])
@monitor_endpoint("get_product_by_id")
def get_product_by_id(product_id):
    if not isinstance(product_id, str) or not product_id:
        return jsonify({"error": "ID inválido"}), 400
    try:
        product = get_by_id_service.execute(product_id)
        return jsonify(product.toDictionary()), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 404
    except Exception:
        abort(500)

@bp.route("/products", methods=["GET"])
@monitor_endpoint("get_all_products")
def get_all_products():
    try:
        products = get_all_service.execute()
        return jsonify([p.toDictionary() for p in products]), 200
    except Exception:
        abort(500)
        
@bp.route("/products/user/<user_id>", methods=["GET"])
@monitor_endpoint("get_products_by_user_id")
def get_products_by_user_id(user_id):
    if not isinstance(user_id, str) or not user_id:
        return jsonify({"error": "ID de usuario inválido"}), 400
    try:
        products = get_by_user_id_service.execute(user_id)
        return jsonify([p.toDictionary() for p in products]), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 404
    except Exception:
        abort(500)

@bp.route("/test", methods=["GET"])
@monitor_endpoint("test_route")
def test():
    try:
        return "Test route is working!", 200
    except Exception:
        abort(500)