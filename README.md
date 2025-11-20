# Dipak Ice Factory Inventory Management System

A production-ready Flask web application for managing ice product inventory with user authentication, shopping cart functionality, and admin panel.

## Features

- **User Authentication**: Registration, login, password hashing, role-based access
- **Product Management**: Browse, search, and filter ice products
- **Shopping Cart**: Add/remove items, checkout with address
- **Order Management**: Place orders, view order history
- **Admin Panel**: CRUD operations on products, order management, user reports
- **Security**: CSRF protection, session management, input validation
- **Responsive UI**: Bootstrap 5 based templates

## Tech Stack

- **Backend**: Python 3.11+, Flask
- **Database**: MongoDB with PyMongo
- **Authentication**: Flask-Login, Werkzeug password hashing
- **Forms**: Flask-WTF with CSRF protection
- **Templates**: Jinja2 with Bootstrap 5
- **Configuration**: python-dotenv for environment variables

## Installation

1. **Clone the repository** (if applicable) or ensure you're in the project directory.

2. **Create a virtual environment** (recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**:
   - Copy `.env.example` to `.env`
   - Update the values in `.env`:
     ```
     SECRET_KEY=your-secret-key-here
     MONGO_URI=mongodb://localhost:27017/ice_factory
     FLASK_ENV=development
     ```

5. **Start MongoDB** (ensure MongoDB is running locally or update MONGO_URI accordingly).

6. **Seed the database**:
   ```bash
   python seed.py
   ```

7. **Run the application**:
   ```bash
   flask --app app.py run --debug
   ```

8. **Access the application**:
   - Open http://localhost:5000 in your browser
   - Admin login: admin@ice.com / Admin@123
   - Sample user: john@example.com / password123

## Project Structure

```
ice_factory/
├── app.py                 # Main Flask application
├── config.py             # Configuration settings
├── seed.py               # Database seeding script
├── requirements.txt      # Python dependencies
├── .env.example          # Environment variables template
├── extensions/           # Flask extensions
│   └── __init__.py
├── models/               # Database service classes
│   ├── user_service.py
│   ├── ice_type_service.py
│   ├── order_service.py
│   └── audit_log_service.py
├── blueprints/           # Flask blueprints
│   ├── auth/             # Authentication routes
│   ├── shop/             # Public shop routes
│   ├── user/             # User dashboard routes
│   └── admin/            # Admin panel routes
├── templates/            # Jinja2 templates
│   ├── layouts/          # Base layouts
│   ├── auth/             # Auth templates
│   ├── shop/             # Shop templates
│   ├── user/             # User templates
│   ├── admin/            # Admin templates
│   └── errors/           # Error pages
└── static/               # Static assets (CSS, JS, images)
```

## Usage

### User Features
- Register/Login with email and password
- Browse ice products with search and filtering
- Add products to cart and checkout
- View order history and details
- Update profile information

### Admin Features
- Dashboard with key metrics
- Full CRUD on ice products
- Order management (view, update status)
- User management (read-only)
- Generate reports with CSV export
- Audit logging for admin actions

## API Endpoints

### Public Routes
- `/` - Home page
- `/ice` - Ice products list
- `/ice/<id>` - Product detail

### Authentication
- `/auth/login` - User login
- `/auth/register` - User registration
- `/auth/logout` - User logout

### User Routes (login required)
- `/user/dashboard` - User dashboard
- `/user/cart` - Shopping cart
- `/user/orders` - Order history
- `/user/profile` - Profile management

### Admin Routes (admin role required)
- `/admin/dashboard` - Admin dashboard
- `/admin/ice` - Ice product management
- `/admin/orders` - Order management
- `/admin/users` - User management
- `/admin/reports` - Reports and analytics

## Security Features

- Password hashing with Werkzeug
- CSRF protection on all forms
- Role-based access control
- Session management
- Input validation and sanitization
- Secure error handling

## Development

- The application uses Flask's development server with debug mode
- Templates use Bootstrap 5 for responsive design
- MongoDB for flexible document storage
- Blueprints for modular route organization

## Production Deployment

For production deployment:
1. Set `FLASK_ENV=production` in `.env`
2. Use a production WSGI server like Gunicorn
3. Configure a production MongoDB instance
4. Set up proper logging and monitoring
5. Use environment-specific configuration

## License

This project is for educational purposes. Modify and use as needed.
