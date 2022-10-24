from flask import Flask, render_template, request, Response, jsonify, url_for, redirect
import database as db
from models.user import User

db = db.dbConnection()
app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/account')
def account():
    return render_template('account.html')

@app.route('/add-product')
def add_product():
    return render_template('add-product.html')

@app.route('/add-recipe')
def add_recipe():
    return render_template('add-recipe.html')

@app.route('/cart')
def cart():
    return render_template('cart.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/orders')
def orders():
    return render_template('orders.html')

@app.route('/products-admin')
def products_admin():
    return render_template('products-admin.html')

@app.route('/products')
def products():
    return render_template('products.html')

@app.route('/update-product')
def update_product():
    return render_template('update-product.html')

@app.route('/register')
def register():
    # users = db['users']
    # name = request.form['name']
    # username = request.form['username']
    # password = request.form['password']

    # if name and username and password:
    #     user = User(name, username, password)
    #     users.insert_one(user.toBDCollection())
    #     response = jsonify({
    #         'name': name,
    #         'username': username,
    #         'password': password
    #     })
    #     return redirect(url_for('home'))
    # else:
    #     return not_found()
    return render_template('register.html')

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