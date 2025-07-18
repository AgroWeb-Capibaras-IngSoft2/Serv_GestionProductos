from flask import Flask, jsonify
from flask_interface.routes import bp
from flasgger import Swagger
from flask_cors import CORS

app = Flask(__name__, static_folder='static')
swagger = Swagger(app, template_file='swagger/swagger.yaml')
CORS(app, origins=["http://localhost:5173"])  # Allow CORS for the specified origin
app.register_blueprint(bp)

# Aquí van los handlers globales:
@app.errorhandler(400)
def bad_request(error):
    return jsonify({"error": str(error.description) if hasattr(error, "description") else "Solicitud incorrecta"}), 400

@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Recurso no encontrado"}), 404

@app.errorhandler(415)
def unsupported_media_type(error):
    return jsonify({"error": "Content-Type must be application/json"}), 415

@app.errorhandler(500)
def internal_error(error):
    return jsonify({"error": "Error interno del servidor"}), 500

if __name__ == "__main__":
    app.run(debug=True, port=5000)  # Run on port 5000 for Serv_GestionProductos