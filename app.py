from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os

# Iniciar aplicación
app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))

# Base de datos
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'products.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Iniciar base de datos
db = SQLAlchemy(app)

# Iniciar serializador
ma = Marshmallow(app)


# Implementación de Clase/Modelo Product
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=True, nullable=False)
    price = db.Column(db.Integer, nullable=False)

    def __init__(self, name, price):
        self.name = name
        self.price = price


# Esquema de Product
class ProductSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'price')


# Inicializar esquema
product_schema = ProductSchema()
products_schema = ProductSchema(many=True)


# Creación de un producto
@app.route('/product', methods=['POST'])
def add_product():
    name = request.json['name']
    price = request.json['price']

    new_product = Product(name, price)

    db.session.add(new_product)
    db.session.commit()

    return product_schema.jsonify(new_product)


# Obtener todos los productos
@app.route('/product', methods=['GET'])
def get_products():
    all_products = Product.query.all()
    result = products_schema.dump(all_products)
    return jsonify(result)


# Obtener un producto en particular
@app.route('/product/<id>', methods=['GET'])
def get_product(id):
    product = Product.query.get(id)
    return product_schema.jsonify(product)


# Actualizar un producto
@app.route('/product/<id>', methods=['PUT'])
def update_product(id):
    product = Product.query.get(id)

    name = request.json['name']
    price = request.json['price']

    product.name = name
    product.price = price

    db.session.commit()

    return product_schema.jsonify(product)


# Borrar un producto
@app.route('/product/<id>', methods=['DELETE'])
def delete_product(id):
    product = Product.query.get(id)
    db.session.delete(product)
    db.session.commit()

    return product_schema.jsonify(product)


# Mensaje de consulta principal.
@app.route('/')
def products_api_main():
    description = {"title": "Products API", "author": "Juan Ignacio Roco",
                   "description": "API para crear, editar, borrar y listar productos y su precio",

                   "routes": [{
                       "endpoint": "/products",
                       "method": "GET",
                       "description": "Obtener listado de productos"
                   },
                       {
                           "endpoint": "/products/<id>",
                           "method": "GET",
                           "description": "Obtener un producto en particular usando su id como parametro"
                       },
                       {
                           "endpoint": "/products",
                           "method": "POST",
                           "description": "Crear un producto, usar campo name y price en formato json"
                       },
                       {
                           "endpoint": "/products/<id>",
                           "method": "PUT",
                           "description": "Actualizar un producto en particular usando su id como parametro"
                       },
                       {
                           "endpoint": "/products/<id>",
                           "method": "DELETE",
                           "description": "Borrar un producto en particular usando su id como parametro"
                       }]},
    return jsonify(description)


# Ejectuar servidor
if __name__ == '__main__':
    app.run()
