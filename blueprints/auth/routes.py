from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash
from blueprints.auth.forms import LoginForm, RegisterForm
from models.user_service import UserService
from models.user import User
from datetime import datetime

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('shop.home'))

    form = LoginForm()
    if form.validate_on_submit():
        user_service = UserService()
        user_data = user_service.authenticate(form.email.data, form.password.data)
        if user_data:
            user = User(user_data)
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('user.dashboard'))
        flash('Invalid email or password', 'error')

    return render_template('auth/login.html', form=form)

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('shop.home'))

    form = RegisterForm()
    if form.validate_on_submit():
        user_service = UserService()
        try:
            user_service.create_user({
                'name': form.name.data,
                'email': form.email.data,
                'password': form.password.data,
                'role': 'user'
            })
            flash('Registration successful! Please log in.', 'success')
            return redirect(url_for('auth.login'))
        except ValueError as e:
            flash(str(e), 'error')

    return render_template('auth/register.html', form=form)

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('shop.home'))
