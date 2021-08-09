import logging.config

from flask import Flask, jsonify, request
from sqlalchemy import exc

from Product import Product
from db import db

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
    log.debug('GET /products')
    try:
        products = [product.json for product in Product.find_all()]
        return jsonify(products)
    except exc.SQLAlchemyError:
        log.exception('An exception occurred while retrieving all products')
        return 'An exception occurred while retrieving all products', 500


@app.route('/product/<int:id>')
def get_product(id):
    log.debug(f'GET /product/{id}')

    try:
        product = Product.find_by_id(id)
        if product:
            return jsonify(product.json)
        return f'Product with {id} not found', 404
    except exc.SQLAlchemyError:
        log.exception(f'An exception occurred while retrieving product {id}')
        return f'An exception occurred while retrieving product {id}', 500


@app.route('/product', methods=['POST'])
def post_product():
    request_product = request.json

    log.debug(f'POST /products with product: /{request_product}')

    product = Product(None, request_product['name'])
    try:
        product.save_to_db()

        return jsonify(product.json), 201
    except exc.SQLAlchemyError:
        log.exception(f'An exception occurred while creating product with name {product.name}')
        return f'An exception occurred while creating product with name {product.name}', 500


@app.route('/product/<int:id>', methods=['PUT'])
def put_product(id):
    log.debug(f'PUT /product/{id}')

    try:
        existing_product = Product.find_by_id(id)
        if existing_product:
            updated_product = request.json

            existing_product.name = updated_product['name']
            existing_product.save_to_db()
            return jsonify(existing_product.json), 200

        log.warning(f'PUT /product/{id}: Existing product not found')
        return f'Product with id {id} not found', 404
    except exc.SQLAlchemyError:
        log.exception(f'An exception occurred while updating product with name {existing_product.name}')
        return f'An exception occurred while updating product with name {existing_product.name}', 500


@app.route('/product/<int:id>', methods=['DELETE'])
def delete_product(id):
    log.debug(f'DELETE /product/{id}')

    try:
        existing_product = Product.find_by_id(id)

        if existing_product:
            existing_product.delete_from_db()
            return jsonify({
                'message': f'Deleted product with id {id}'
            }), 200

        log.warning(f'DELETE /product/{id}: Existing product not found')
        return f'Product with id {id} not found', 404
    except exc.SQLAlchemyError:
        log.exception(f'An exception occurred while deleting product with name {existing_product.name}')
        return f'An exception occurred while deleting product with name {existing_product.name}', 500


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
