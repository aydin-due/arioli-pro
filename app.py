from flask import Flask, render_template, request, Response, jsonify, url_for, redirect, session
import database as db
import secrets
from models.user import User

db = db.dbConnection()
app = Flask(__name__)
app.secret_key = secrets.token_hex(16)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/account')
def account():
    if 'username' in session:
        user = session['username']
        return render_template('account.html', user=user)
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

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        users = db['users']
        email = request.form['email']
        password = request.form['password']

        if email and password:
            user = users.find_one({"email": email, "password": password})
            if user:
                session['username'] = user['username']
                return redirect(url_for('account'))
            return render_template('login.html', error='El correo o la contraseña son incorrectos')
        else:
            return render_template('login.html', error='Por favor llene todos los campos')
    else:
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

@app.route('/register', methods=['GET','POST'])
def register():
    if request.method == 'POST':
        users = db['users']
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        if username and email and password:
            user = User(username, email, password)
            if users.find_one({'email': email}):
                return render_template('register.html', error='El correo ya está en uso')
            users.insert_one(user.toBDCollection())
            session['username'] = username
            return redirect(url_for('account'))
        else:
            return render_template('register.html', error='Por favor llene todos los campos')
    else:
        return render_template('register.html')

@app.route('/logout') 
def logout():
    if 'username' in session:
        session.pop('username',None)
        return redirect('/')

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