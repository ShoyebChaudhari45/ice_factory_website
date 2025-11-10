from flask import Flask, render_template, request, flash, redirect, url_for, session
from config import config
from extensions import mongo, login_manager, csrf
from blueprints.auth.routes import auth_bp
from blueprints.shop.routes import shop_bp
from blueprints.user.routes import user_bp
from blueprints.admin.routes import admin_bp
from models.user_service import UserService
from models.user import User
from bson import ObjectId
from flask_wtf.csrf import generate_csrf
import os

def create_app(config_name='development'):
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    # Initialize extensions
    mongo.init_app(app)
    login_manager.init_app(app)
    csrf.init_app(app)

    # Register blueprints
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(shop_bp, url_prefix='/')
    app.register_blueprint(user_bp, url_prefix='/user')
    app.register_blueprint(admin_bp, url_prefix='/admin')

    # User loader for Flask-Login
    @login_manager.user_loader
    def load_user(user_id):
        user_service = UserService()
        user_data = user_service.get_user_by_id(user_id)
        return User(user_data) if user_data else None

    # Error handlers
    @app.errorhandler(403)
    def forbidden(error):
        return render_template('errors/403.html'), 403

    @app.errorhandler(404)
    def not_found(error):
        return render_template('errors/404.html'), 404

    @app.errorhandler(500)
    def internal_error(error):
        return render_template('errors/500.html'), 500

    @app.after_request
    def set_csrf_cookie(response):
        response.set_cookie("csrf_token", generate_csrf())
        return response

    return app

app = create_app(os.getenv('FLASK_ENV', 'development'))

if __name__ == '__main__':
    app.run(debug=True)
