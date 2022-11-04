import os
from flask import Flask, render_template, request, Response, jsonify, url_for, redirect, session
import database as db
import secrets
from models.user import User
from models.recipe import Recipe
from models.product import Product
from models.cart import Cart

db = db.dbConnection()
app = Flask(__name__)
app.secret_key = secrets.token_hex(16)
app.config['UPLOAD_FOLDER'] = 'static/img/products'

def is_admin():
    if 'email' in session:
        users = db['users']
        user = users.find_one({"email": session['email']})
        return user['admin']
    else:
        return False

@app.route('/add-to-cart/<int:id_product>', methods=["GET", "POST"])
def add_to_cart(id_product):
    products = db['products']
    product = products.find_one({"_id": id_product})
    users = db['users']
    user = users.find_one({"email": session['email']})
    carts = db['carts']
    product['quantity'] = 1
    product['unit_total'] = product['price']
    if 'cart' in user:
        id_cart = user['cart']
        cart = carts.find_one({"_id": id_cart})
        print('CART !!! ', cart)
        index = next((i for i, product in enumerate(cart['products']) if product['_id'] == id_product), None)
        if index is not None:
            product_in_cart = cart['products'][index]
            cart['products'][index]['quantity'] += 1
            cart['products'][index]['unit_total'] = product_in_cart['quantity'] * int(product_in_cart['price'])
        else:
            cart['products'].append(product)
        cart_total = sum(int(product['unit_total']) for product in cart['products'])
        carts.update_one({"_id": id_cart}, {"$set": {"products": cart['products'], "total": cart_total}})
    else:
        id_cart = carts.count_documents({})
        cart = Cart(id_cart, [product], product['price'])
        carts.insert_one(cart.toDBCollection())
        users.update_one({"email": session['email']}, {"$set": {"cart": id_cart}})
    return redirect(url_for('products', error='Producto añadido al carrito :^)'))

@app.route('/')
def home():
    return render_template('index.html', admin=is_admin())

@app.route('/account')
def account():
    if 'username' in session:
        user = session['username']
        return render_template('account.html', user=user, admin=is_admin())
    return render_template('account.html', admin=is_admin())

@app.route('/add-product', methods=['GET', 'POST'])
def add_product():
    if request.method == 'POST':
        ingredients = []
        products = db['products']
        recipes = db['recipes']
        for quantity, unit, ingredient in zip(request.form.getlist('quantity'), request.form.getlist('unit'), request.form.getlist('ingredient')):
            ingredients.append({
                "quantity": quantity,
                "unit": unit,
                "ingredient": ingredient
            })
        id_recipe = recipes.count_documents({})
        id_product = products.count_documents({})

        recipe = Recipe(id_recipe, ingredients, request.form['procedure'])
        recipes.insert_one(recipe.toDBCollection())

        file = request.files['image']
        filename = str(id_product) + '.jpg'
        img_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(img_path)

        product = Product(id_product, request.form['name'], request.form['description'], request.form['price'], img_path, id_recipe)
        products.insert_one(product.toDBCollection())
        return render_template('add-product.html', admin=is_admin(), error='Producto agregado correctamente :^)')
    return render_template('add-product.html', admin=is_admin())

@app.route('/add-recipe')
def add_recipe():
    return render_template('add-recipe.html', admin=is_admin())

@app.route('/cart')
def cart():
    if 'username' in session:
        users = db['users']
        user = users.find_one({"email": session['email']})
        carts = db['carts']
        cart = carts.find_one({"_id": user['cart']})
        return render_template('cart.html', cart=cart, admin=is_admin(), user=user)
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
    products = db['products'].find()
    return render_template('products-admin.html', admin=is_admin(), products=products)

@app.route('/products', methods=["GET", "POST"])
def products():
    error = request.args.get('error')
    products = db['products'].find()
    if 'username' in session:
        return render_template('products.html', admin=is_admin(), products=products, error=error, user=session['username'])
    return render_template('products.html', admin=is_admin(), products=products)
        

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