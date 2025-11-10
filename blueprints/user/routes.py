from flask import Blueprint, render_template, redirect, url_for, flash, request, session
from flask_login import login_required, current_user
from .forms import ProfileForm, ChangePasswordForm, CheckoutForm, AddToCartForm
from models.user_service import UserService
from models.ice_type_service import IceTypeService
from models.order_service import OrderService
from werkzeug.security import check_password_hash, generate_password_hash

user_bp = Blueprint('user', __name__, url_prefix='/user')

def get_cart():
    return session.get('cart', {})

def save_cart(cart):
    session['cart'] = cart

def calculate_cart_total(cart):
    total = 0
    items = []
    for ice_type_id, qty in cart.items():
        ice_type = IceTypeService.get_ice_type_by_id(ice_type_id)
        if ice_type and ice_type['is_active'] and ice_type['in_stock'] >= qty:
            line_total = ice_type['price_per_unit'] * qty
            total += line_total
            items.append({
                'ice_type_id': ice_type_id,
                'name': ice_type['name'],
                'unit_price': ice_type['price_per_unit'],
                'qty': qty,
                'line_total': line_total
            })
    return items, total

@user_bp.route('/dashboard')
@login_required
def dashboard():
    orders, _ = OrderService.get_orders_by_user(current_user.get_id(), page=1, per_page=5)
    return render_template('user/dashboard.html', title='Dashboard', recent_orders=orders)

@user_bp.route('/cart', methods=['GET', 'POST'])
@login_required
def cart():
    cart = get_cart()
    items, subtotal = calculate_cart_total(cart)
    form = CheckoutForm()
    if form.validate_on_submit():
        if not items:
            flash('Your cart is empty', 'warning')
            return redirect(url_for('user.cart'))
        order, error = OrderService.create_order(
            current_user.get_id(), items, form.shipping_address.data
        )
        if order:
            session['cart'] = {}
            flash('Order placed successfully!', 'success')
            return redirect(url_for('user.orders'))
        flash(error or 'Failed to place order', 'danger')
    return render_template('user/cart.html', title='Shopping Cart',
                         items=items, subtotal=subtotal, form=form)

@user_bp.route('/cart/add/<ice_type_id>', methods=['POST'])
@login_required
def cart_add(ice_type_id):
    form = AddToCartForm()
    if not form.validate_on_submit():
        flash('Invalid add-to-cart request.', 'danger')
        return redirect(url_for('shop.ice_detail', ice_type_id=ice_type_id))
    # proceed with qty = form.quantity.data, stock check, save to session, flash success
    ice_type = IceTypeService.get_ice_type_by_id(ice_type_id)
    if not ice_type or not ice_type['is_active']:
        flash('Ice type not found', 'danger')
        return redirect(url_for('shop.ice_list'))

    qty = form.quantity.data
    if ice_type['in_stock'] < qty:
        flash('Insufficient stock', 'danger')
        return redirect(url_for('shop.ice_detail', ice_type_id=ice_type_id))

    cart = get_cart()
    current_qty = cart.get(ice_type_id, 0)
    cart[ice_type_id] = current_qty + qty
    save_cart(cart)
    flash(f'Added {qty} {ice_type["unit"]} of {ice_type["name"]} to cart', 'success')
    return redirect(url_for('shop.ice_detail', ice_type_id=ice_type_id))

@user_bp.route('/cart/remove/<ice_type_id>', methods=['POST'])
@login_required
def cart_remove(ice_type_id):
    cart = get_cart()
    if ice_type_id in cart:
        del cart[ice_type_id]
        save_cart(cart)
        flash('Item removed from cart', 'success')
    return redirect(url_for('user.cart'))

@user_bp.route('/orders')
@login_required
def orders():
    page = int(request.args.get('page', 1))
    orders, total = OrderService.get_orders_by_user(current_user.get_id(), page=page)
    return render_template('user/orders.html', title='My Orders',
                         orders=orders, page=page, total=total)

@user_bp.route('/orders/<order_id>')
@login_required
def order_detail(order_id):
    order = OrderService.get_order_by_id(order_id)
    if not order or str(order['user_id']) != current_user.get_id():
        return render_template('errors/404.html'), 404
    return render_template('user/order_detail.html', title=f'Order {order_id}', order=order)

@user_bp.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    form = ProfileForm()
    if form.validate_on_submit():
        UserService.update_user(current_user.get_id(), {
            'name': form.name.data,
            'email': form.email.data
        })
        flash('Profile updated successfully', 'success')
        return redirect(url_for('user.profile'))
    elif request.method == 'GET':
        form.name.data = current_user.name
        form.email.data = current_user.email
    return render_template('user/profile.html', title='My Profile', form=form)

@user_bp.route('/change-password', methods=['GET', 'POST'])
@login_required
def change_password():
    form = ChangePasswordForm()
    if form.validate_on_submit():
        if not check_password_hash(current_user.password_hash, form.current_password.data):
            flash('Current password is incorrect', 'danger')
        else:
            UserService.update_user(current_user.get_id(), {
                'password_hash': generate_password_hash(form.new_password.data)
            })
            flash('Password changed successfully', 'success')
            return redirect(url_for('user.profile'))
    return render_template('user/change_password.html', title='Change Password', form=form)
