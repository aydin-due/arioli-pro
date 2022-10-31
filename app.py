from flask import Flask, render_template, request, Response, jsonify, url_for, redirect, session
import database as db
import secrets
from models.user import User

db = db.dbConnection()
app = Flask(__name__)
app.secret_key = secrets.token_hex(16)

def is_admin():
    if 'email' in session:
        users = db['users']
        user = users.find_one({"email": session['email']})
        return user['admin']
    else:
        return False

@app.route('/')
def home():
    return render_template('index.html', admin=is_admin())

@app.route('/account')
def account():
    if 'username' in session:
        user = session['username']
        return render_template('account.html', user=user, admin=is_admin())
    return render_template('account.html', admin=is_admin())

@app.route('/add-product')
def add_product():
    return render_template('add-product.html', admin=is_admin())

@app.route('/add-recipe')
def add_recipe():
    return render_template('add-recipe.html', admin=is_admin())

@app.route('/cart')
def cart():
    return render_template('cart.html', admin=is_admin())

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
                session['email'] = user['email']
                return redirect(url_for('account'))
            return render_template('login.html', error='El correo o la contraseña son incorrectos', admin=is_admin())
        else:
            return render_template('login.html', error='Por favor llene todos los campos', admin=is_admin())
    else:
        return render_template('login.html', admin=is_admin())

@app.route('/orders')
def orders():
    return render_template('orders.html', admin=is_admin())

@app.route('/products-admin')
def products_admin():
    return render_template('products-admin.html', admin=is_admin())

@app.route('/products')
def products():
    return render_template('products.html', admin=is_admin())

@app.route('/update-product')
def update_product():
    return render_template('update-product.html', admin=is_admin())

@app.route('/recipe')
def recipe():
    return render_template('recipe.html', admin=is_admin())

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
                return render_template('register.html', error='El correo ya está en uso', admin=is_admin())
            users.insert_one(user.toBDCollection())
            session['username'] = username
            session['email'] = email
            return redirect(url_for('account'))
        else:
            return render_template('register.html', error='Por favor llene todos los campos', admin=is_admin())
    else:
        return render_template('register.html', admin=is_admin())

@app.route('/logout') 
def logout():
    if 'username' in session:
        session.pop('username',None)
        session.pop('email',None)
        return redirect('/')

if __name__ == '__main__':
    app.run(debug=True, port=4000)