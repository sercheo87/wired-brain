import logging.config

from flask import Flask, jsonify, request
from sqlalchemy.testing import db

import Product as Product

products = [
    {'id': 1, 'name': 'Product 1'},
    {'id': 2, 'name': 'Product 2'}
]

logging.config.fileConfig("logging.ini", disable_existing_loggers=False)

log = logging.getLogger(__name__)

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:password@db/products'
db.init_app(app)


@app.route('/products')
def get_products():
    products = [product.json for product in Product.find_all()]
    return jsonify(products)


@app.route('/product/<int:id>')
def get_product(id):
    product = Product.find_by_id(id)
    if product:
        return jsonify(product.json)
    return f'Product with {id} not found', 404


@app.route('/product', methods=['POST'])
def post_product():
    request_product = request.json

    product = Product(None, request_product['name'])

    product.save_to_db()

    return jsonify(product.json), 201


@app.route('/product/<int:id>', methods=['PUT'])
def put_product(id):
    existing_product = Product.find_by_id(id)

    if existing_product:
        updated_product = request.json

        existing_product.name = updated_product['name']
        existing_product.save_to_db()
        return jsonify(existing_product.json), 200

    return f'Product with id {id} not found', 404


@app.route('/product/<int:id>', methods=['DELETE'])
def delete_product(id):
    existing_product = Product.find_by_id(id)

    if existing_product:
        existing_product.delete_from_db()
        return jsonify({
            'message': f'Deleted product with id {id}'
        }), 200
    return f'Product with id {id} not found', 404


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
