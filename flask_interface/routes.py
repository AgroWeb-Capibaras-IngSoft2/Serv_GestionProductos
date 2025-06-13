from flask import Blueprint, request, jsonify
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
    data = request.get_json()
    try:
        product = create_service.execute(data)
        return jsonify(product.toDictionary()), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@bp.route("/products/<product_id>", methods=["GET"])
def get_product_by_id(product_id):
    try:
        product = get_by_id_service.execute(product_id)
        return jsonify(product.toDictionary()), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 404

@bp.route("/products", methods=["GET"])
def get_all_products():
    products = get_all_service.execute()
    return jsonify([p.toDictionary() for p in products]), 200