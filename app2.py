from flask import Flask, render_template, request, Response, jsonify, url_for, redirect
import database as db
from models.product import Product
from models.user import User

db = db.dbConnection()
app = Flask(__name__)

@app.route('/')
def home():
    products = db['products'].find()
    return render_template('index2.html', products=products)

@app.route('/products', methods=['POST'])
def addProduct():
    products = db['products']
    name = request.form['name']
    price = request.form['price']
    quantity = request.form['quantity']
   
    if name and price and quantity:
        product = Product(name, price, quantity)
        products.insert_one(product.toDBCollection())
        response = jsonify({
            'name': name,
            'price': price,
            'quantity': quantity
        })
        return redirect(url_for('home'))
    else:
        return not_found()

@app.route('/delete/<string:product_name>')
def delete(product_name):
    products = db['products']
    products.delete_one({'name': product_name})
    return redirect(url_for('home'))

@app.route('/update/<string:product_name>', methods=['POST'])
def update(product_name):
    products = db['products']
    name = request.form['name']
    price = request.form['price']
    quantity = request.form['quantity']
   
    if name and price and quantity:
        products.update_one({'name': product_name}, {'$set': {'name': name, 'price': price, 'quantity': quantity}})
        response = jsonify({'message': 'Product ' + product_name + ' updated successfully'})
        return redirect(url_for('home'))
    else:
        return not_found()

@app.errorhandler(404)
def not_found(error=None):
    message = {
        'message': 'Resource not found: ' + request.url,
        'status': '404 Not Found'
    }
    response = jsonify(message)
    response.status_code = 404
    return response

if __name__ == '__main__':
    app.run(debug=True, port=4000)