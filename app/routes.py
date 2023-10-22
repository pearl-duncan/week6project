from app import app, db
from flask import render_template, request, flash, redirect, url_for
from .forms import LoginForm, SignUpForm, ProductForm
from .models import User, Product, Cart
from flask_login import login_user, logout_user, login_required, current_user

@app.route("/")
def index():
    products = Product.query.all()
    return render_template('index.html', products=products)

@app.route("/create_product", methods =['GET', 'POST'])
def create():
    form = ProductForm()
    if request.method == "POST":
        if form.validate():
            img_url = form.img_url.data
            name = form.name.data
            description = form.description.data
            price = form.price.data

            new_product = Product(img_url, name, description, price)
            
            db.session.add(new_product)
            db.session.commit()

            flash("product created!", 'success')
        else:
            flash('Invalid form. Please try again.', 'error')
    return render_template('create_product.html', form = form)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = SignUpForm()
    if request.method == "POST":
        if form.validate():
            first_name = form.first_name.data
            last_name = form.last_name.data
            username = form.username.data
            email = form.email.data
            password = form.password.data

            new_user = User(first_name, last_name, username, email, password)
            db.session.add(new_user)
            db.session.commit()

            flash("You're signed up!", 'success')
            return redirect(url_for('index'))
    else:
        flash('Invalid form. Please try again.', 'error')
    return render_template('signup.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login_page():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if request.method == 'POST':
        if form.validate():
            username = form.username.data
            password = form.password.data

            user = User.query.filter_by(username=username).first() 

            if user:
                if user.password == password:
                    login_user(user)
                    flash('Successfully logged in.', 'success')
                    return redirect(url_for('index'))
                else:
                    flash('Incorrect username/password combination.', 'danger')
            else:
                flash('That username does not exist.', 'danger')
    return render_template('login.html', form = form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash("You have successfully logged out", 'success')
    return redirect(url_for('login_page'))

@app.route('/product_detail/<product_id>')
@login_required
def product_detail(product_id):
    product = Product.query.filter_by(product_id).first()
    return render_template('product_detail.html', product=product) 

@app.route('/cart/add/<product_id>', methods=['GET', 'POST'])
@login_required
def addtocart(product_id):
    product = Product.query.get_or_404(product_id)
    product_key = product.id
    user_key = current_user.id
    cart_item = Cart(user_key, product_key)

    db.session.add(cart_item)
    db.session.commit()
    
    flash(f"{ product.name } has been added to your cart!", "success")
    return redirect(url_for('cart'))

@app.route('/cart', methods=['GET', 'POST'])
@login_required
def cart():
    card = {
    'title': "My Cart",
    'items': Cart.query.all(),
    'items': Cart.query.filter(Cart.user_id==current_user.id).all(),
    'total': Product.query.filter(Product.price).all()
    }
    if not card:
        return render_template('cart.html', card=card)
    else:
        for product in card['items']:
            card['total'] += float(product.price)
    return render_template('cart.html', card=card)

@app.route('/cart/remove/<item_id>', methods=['POST'])
@login_required
def delete(product_id):
    cart = Cart.query.filter(product_id).all()
    db.session.delete(cart)
    db.session.commit()
    flash("Item has been removed from your cart", "danger")
    return redirect(url_for('cart'))
