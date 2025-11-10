from flask import Blueprint, render_template, redirect, url_for, flash, request, Response
from flask_login import login_required, current_user
from functools import wraps
from .forms import IceTypeForm, OrderStatusForm, ReportForm
from models.ice_type_service import IceTypeService
from models.order_service import OrderService
from models.user_service import UserService
from models.audit_log_service import AuditLogService
import csv
from io import StringIO

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or current_user.role != 'admin':
            return render_template('errors/403.html'), 403
        return f(*args, **kwargs)
    return decorated_function

@admin_bp.route('/')
@admin_required
def dashboard():
    stats = OrderService.get_order_stats()
    low_stock = IceTypeService.get_low_stock_items()
    return render_template('admin/dashboard.html', title='Admin Dashboard',
                         stats=stats, low_stock_items=low_stock)

@admin_bp.route('/ice')
@admin_required
def ice_list():
    page = int(request.args.get('page', 1))
    search = request.args.get('q')
    ice_types, total = IceTypeService.get_all_ice_types(page=page, search=search)
    return render_template('admin/ice_list.html', title='Manage Ice Types',
                         ice_types=ice_types, page=page, total=total, search=search)

@admin_bp.route('/ice/new', methods=['GET', 'POST'])
@admin_required
def ice_new():
    form = IceTypeForm()
    if form.validate_on_submit():
        ice_type = IceTypeService.create_ice_type(
            name=form.name.data,
            category=form.category.data,
            description=form.description.data,
            price_per_unit=form.price_per_unit.data,
            unit=form.unit.data,
            in_stock=form.in_stock.data,
            image_url=form.image_url.data
        )
        if ice_type:
            AuditLogService.log_action(current_user.get_id(), 'create', 'ice_types', str(ice_type['_id']))
            flash('Ice type created successfully', 'success')
            return redirect(url_for('admin.ice_list'))
        flash('Ice type with this name already exists', 'danger')
    return render_template('admin/ice_form.html', title='Add Ice Type', form=form)

@admin_bp.route('/ice/<ice_type_id>/edit', methods=['GET', 'POST'])
@admin_required
def ice_edit(ice_type_id):
    ice_type = IceTypeService.get_ice_type_by_id(ice_type_id)
    if not ice_type:
        return render_template('errors/404.html'), 404

    form = IceTypeForm()
    if form.validate_on_submit():
        updates = {
            'name': form.name.data,
            'category': form.category.data,
            'description': form.description.data,
            'price_per_unit': form.price_per_unit.data,
            'unit': form.unit.data,
            'in_stock': form.in_stock.data,
            'image_url': form.image_url.data
        }
        IceTypeService.update_ice_type(ice_type_id, updates)
        AuditLogService.log_action(current_user.get_id(), 'update', 'ice_types', ice_type_id, updates)
        flash('Ice type updated successfully', 'success')
        return redirect(url_for('admin.ice_list'))
    elif request.method == 'GET':
        form.name.data = ice_type['name']
        form.category.data = ice_type['category']
        form.description.data = ice_type['description']
        form.price_per_unit.data = ice_type['price_per_unit']
        form.unit.data = ice_type['unit']
        form.in_stock.data = ice_type['in_stock']
        form.image_url.data = ice_type.get('image_url', '')
    return render_template('admin/ice_form.html', title='Edit Ice Type', form=form)

@admin_bp.route('/ice/<ice_type_id>/delete', methods=['POST'])
@admin_required
def ice_delete(ice_type_id):
    ice_type = IceTypeService.get_ice_type_by_id(ice_type_id)
    if ice_type:
        IceTypeService.delete_ice_type(ice_type_id)
        AuditLogService.log_action(current_user.get_id(), 'delete', 'ice_types', ice_type_id)
        flash('Ice type deleted successfully', 'success')
    return redirect(url_for('admin.ice_list'))

@admin_bp.route('/ice/<ice_type_id>/toggle', methods=['POST'])
@admin_required
def ice_toggle(ice_type_id):
    IceTypeService.toggle_active(ice_type_id)
    AuditLogService.log_action(current_user.get_id(), 'toggle_active', 'ice_types', ice_type_id)
    flash('Ice type status updated', 'success')
    return redirect(url_for('admin.ice_list'))

@admin_bp.route('/orders')
@admin_required
def orders_list():
    page = int(request.args.get('page', 1))
    status = request.args.get('status')
    date_from = request.args.get('date_from')
    date_to = request.args.get('date_to')
    orders, total = OrderService.get_all_orders(page=page, status=status, date_from=date_from, date_to=date_to)
    return render_template('admin/orders_list.html', title='Manage Orders',
                         orders=orders, page=page, total=total, status=status,
                         date_from=date_from, date_to=date_to)

@admin_bp.route('/orders/<order_id>', methods=['GET', 'POST'])
@admin_required
def order_detail(order_id):
    order = OrderService.get_order_by_id(order_id)
    if not order:
        return render_template('errors/404.html'), 404

    form = OrderStatusForm()
    if form.validate_on_submit():
        OrderService.update_order_status(order_id, form.status.data)
        AuditLogService.log_action(current_user.get_id(), 'update_status', 'orders', order_id,
                                 {'status': form.status.data})
        flash('Order status updated successfully', 'success')
        return redirect(url_for('admin.order_detail', order_id=order_id))
    elif request.method == 'GET':
        form.status.data = order['status']
    return render_template('admin/order_detail.html', title=f'Order {order_id}', order=order, form=form)

@admin_bp.route('/orders/<order_id>/cancel', methods=['POST'])
@admin_required
def order_cancel(order_id):
    OrderService.cancel_order(order_id)
    AuditLogService.log_action(current_user.get_id(), 'cancel', 'orders', order_id)
    flash('Order cancelled successfully', 'success')
    return redirect(url_for('admin.orders_list'))

@admin_bp.route('/users')
@admin_required
def users_list():
    page = int(request.args.get('page', 1))
    search = request.args.get('q')
    users, total = UserService.get_all_users(page=page, search=search)
    return render_template('admin/users_list.html', title='Manage Users',
                         users=users, page=page, total=total, search=search)

@admin_bp.route('/reports', methods=['GET', 'POST'])
@admin_required
def reports():
    form = ReportForm()
    if form.validate_on_submit():
        date_from = form.date_from.data.isoformat()
        date_to = form.date_to.data.isoformat()
        orders = OrderService.get_orders_by_date_range(date_from, date_to)

        total_revenue = sum(order['grand_total'] for order in orders)
        total_orders = len(orders)

        # Group by ice type for top products
        product_sales = {}
        for order in orders:
            for item in order['items']:
                ice_type_id = item['ice_type_id']
                if ice_type_id not in product_sales:
                    product_sales[ice_type_id] = {'name': item['name'], 'quantity': 0, 'revenue': 0}
                product_sales[ice_type_id]['quantity'] += item['qty']
                product_sales[ice_type_id]['revenue'] += item['line_total']

        top_products = sorted(product_sales.values(), key=lambda x: x['revenue'], reverse=True)[:10]

        return render_template('admin/reports.html', title='Reports',
                             form=form, orders=orders, total_revenue=total_revenue,
                             total_orders=total_orders, top_products=top_products,
                             date_from=date_from, date_to=date_to)
    return render_template('admin/reports.html', title='Reports', form=form)

@admin_bp.route('/reports/download')
@admin_required
def reports_download():
    date_from = request.args.get('date_from')
    date_to = request.args.get('date_to')
    if not date_from or not date_to:
        flash('Date range required', 'danger')
        return redirect(url_for('admin.reports'))

    orders = OrderService.get_orders_by_date_range(date_from, date_to)

    si = StringIO()
    writer = csv.writer(si)
    writer.writerow(['Order ID', 'User', 'Date', 'Status', 'Total'])

    for order in orders:
        user = UserService.get_user_by_id(order['user_id'])
        writer.writerow([
            str(order['_id']),
            user['name'] if user else 'Unknown',
            order['created_at'].strftime('%Y-%m-%d'),
            order['status'],
            f"{order['grand_total']:.2f}"
        ])

    output = si.getvalue()
    si.close()

    return Response(
        output,
        mimetype='text/csv',
        headers={'Content-Disposition': f'attachment;filename=orders_{date_from}_to_{date_to}.csv'}
    )
