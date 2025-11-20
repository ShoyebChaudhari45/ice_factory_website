# Dipak Ice Factory Inventory Management System - TODO List

## Core Application Files
- [ ] Create app.py (main Flask app)
- [ ] Create config.py (app settings)
- [ ] Create requirements.txt (dependencies)
- [ ] Create .env.example (environment variables template)
- [ ] Create seed.py (database seeding script)

## Extensions Setup
- [ ] Create /extensions/ directory
- [ ] Implement login_manager extension
- [ ] Implement mongo client extension
- [ ] Implement csrf extension

## Models/Services
- [ ] Create /models/ directory
- [ ] Implement user service/repository
- [ ] Implement ice_types service/repository
- [ ] Implement orders service/repository
- [ ] Implement audit_logs service/repository (optional)

## Blueprints
- [ ] Create /blueprints/ directory
- [ ] Implement auth blueprint (routes.py, forms.py)
- [ ] Implement shop blueprint (routes.py)
- [ ] Implement user blueprint (routes.py, forms.py)
- [ ] Implement admin blueprint (routes.py, forms.py)

## Templates
- [ ] Create /templates/ directory
- [ ] Create /templates/layouts/ (base.html, admin_base.html)
- [ ] Create /templates/auth/ (login.html, register.html)
- [ ] Create /templates/shop/ (home.html, ice_list.html, ice_detail.html)
- [ ] Create /templates/user/ (dashboard.html, cart.html, checkout.html, orders.html, order_detail.html, profile.html)
- [ ] Create /templates/admin/ (dashboard.html, ice_list.html, ice_form.html, orders_list.html, order_detail.html, users_list.html, reports.html)
- [ ] Create /templates/errors/ (403.html, 404.html, 500.html)

## Static Assets
- [ ] Create /static/ directory
- [ ] Add basic CSS/JS files

## Implementation Details
- [ ] Implement authentication and authorization
- [ ] Implement role-based access control
- [ ] Implement CSRF protection on forms
- [ ] Implement password hashing
- [ ] Implement session management
- [ ] Implement DB operations for all entities
- [ ] Implement validation and error handling
- [ ] Implement pagination and search/filter
- [ ] Implement cart functionality
- [ ] Implement order processing
- [ ] Implement admin CRUD operations
- [ ] Implement reports and CSV export
- [ ] Implement audit logging (optional)

## Testing and Deployment
- [ ] Install dependencies
- [ ] Configure environment (.env)
- [ ] Seed database
- [ ] Run and test the application
- [ ] Add unit tests (optional)
