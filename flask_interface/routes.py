from flask import Blueprint, request, jsonify, abort
from Infrastructure.adapterProductRepo import AdapterProductRepo
from application.useCases.CreateProductService import CreateProductService
from application.useCases.GetProductByIdService import GetProductByIdService
from application.useCases.GetAllProductsService import GetAllProductsService

bp = Blueprint('productos', __name__)
repo = AdapterProductRepo()
create_service = CreateProductService(repo)
get_by_id_service = GetProductByIdService(repo)
get_all_service = GetAllProductsService(repo)

@bp.route("/products", methods=["POST"])
def create_product():
    if not request.is_json:
        abort(415)
    data = request.get_json()
    required_fields = [
    "productId", "name", "category", "price", "unit", "imageUrl", "stock",
    "origin", "description", "isActive"
    ]
    # The rest (originalPrice, isOrganic, isBestSeller, freeShipping) are optional
    missing = [f for f in required_fields if f not in data]
    if missing:
        return jsonify({"error": f"Faltan campos obligatorios: {', '.join(missing)}"}), 400
    try:
        product = create_service.execute(data)
        return jsonify(product.toDictionary()), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception:
        abort(500)

@bp.route("/products/<product_id>", methods=["GET"])
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
def get_all_products():
    try:
        products = get_all_service.execute()
        return jsonify([p.toDictionary() for p in products]), 200
    except Exception:
        abort(500)

@bp.route("/test", methods=["GET"])
def test():
    try:
        return "Test route is working!", 200
    except Exception:
        abort(500)