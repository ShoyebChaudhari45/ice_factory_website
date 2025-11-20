from flask import Blueprint, render_template, request
from models.ice_type_service import IceTypeService
from blueprints.user.forms import AddToCartForm

shop_bp = Blueprint('shop', __name__)

@shop_bp.route('/')
def home():
    featured_ice_types, _ = IceTypeService.get_active_ice_types(page=1, per_page=6)
    return render_template('shop/home.html', title='Dipak Ice Factory - Home', featured_ice_types=featured_ice_types)

@shop_bp.route('/ice')
def ice_list():
    page = int(request.args.get('page', 1))
    per_page = 12
    search = request.args.get('q')
    category = request.args.get('category')
    price_min = request.args.get('price_min', type=float)
    price_max = request.args.get('price_max', type=float)

    ice_types, total = IceTypeService.get_active_ice_types(
        page=page, per_page=per_page, search=search,
        category=category, price_min=price_min, price_max=price_max
    )

    return render_template('shop/ice_list.html', title='Ice Types',
                         ice_types=ice_types, page=page, total=total, per_page=per_page,
                         search=search, category=category, price_min=price_min, price_max=price_max)

@shop_bp.route('/ice/<ice_type_id>')
def ice_detail(ice_type_id):
    ice_type = IceTypeService.get_ice_type_by_id(ice_type_id)
    if not ice_type or not ice_type.get('is_active'):
        return render_template('errors/404.html'), 404
    form = AddToCartForm()
    return render_template('shop/ice_detail.html', title=ice_type['name'], ice=ice_type, add_to_cart_form=form)
