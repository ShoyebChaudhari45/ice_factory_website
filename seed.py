from app import create_app
from models.user_service import UserService
from models.ice_type_service import IceTypeService
from models.order_service import OrderService
from datetime import datetime
from werkzeug.security import generate_password_hash
from extensions import mongo

def seed_database():
    app = create_app()
    with app.app_context():
        user_service = UserService()
        ice_service = IceTypeService()
        order_service = OrderService()

        # Create admin user
        user_service.create_user({
            'name': 'Admin User',
            'email': 'admin@ice.com',
            'password': 'Admin@123',
            'role': 'admin'
        })

        # Create sample users
        user_service.create_user({
            'name': 'John Doe',
            'email': 'john@example.com',
            'password': 'password123',
            'role': 'user'
        })
        user_service.create_user({
            'name': 'Jane Smith',
            'email': 'jane@example.com',
            'password': 'password123',
            'role': 'user'
        })

        # Create sample ice types
        ice_types_data = [
            {
                'name': 'Crystal Clear Ice Cubes',
                'category': 'cube',
                'description': 'Premium crystal clear ice cubes perfect for cocktails and beverages.',
                'price_per_unit': 2.50,
                'unit': 'kg',
                'in_stock': 100,
                'image_url': '',
                'is_active': True,
                'created_at': datetime.utcnow(),
                'updated_at': datetime.utcnow()
            },
            {
                'name': 'Block Ice',
                'category': 'block',
                'description': 'Large ice blocks ideal for commercial use and sculpting.',
                'price_per_unit': 5.00,
                'unit': 'kg',
                'in_stock': 50,
                'image_url': '',
                'is_active': True,
                'created_at': datetime.utcnow(),
                'updated_at': datetime.utcnow()
            },
            {
                'name': 'Snow Flakes',
                'category': 'flake',
                'description': 'Fluffy snow-like ice flakes perfect for shaved ice desserts.',
                'price_per_unit': 3.25,
                'unit': 'kg',
                'in_stock': 75,
                'image_url': '',
                'is_active': True,
                'created_at': datetime.utcnow(),
                'updated_at': datetime.utcnow()
            },
            {
                'name': 'Tube Ice',
                'category': 'cube',
                'description': 'Long tube-shaped ice perfect for cooling drinks slowly.',
                'price_per_unit': 2.75,
                'unit': 'kg',
                'in_stock': 80,
                'image_url': '',
                'is_active': True,
                'created_at': datetime.utcnow(),
                'updated_at': datetime.utcnow()
            },
            {
                'name': 'Nugget Ice',
                'category': 'cube',
                'description': 'Chewy nugget ice that\'s fun to eat and great for beverages.',
                'price_per_unit': 3.50,
                'unit': 'kg',
                'in_stock': 60,
                'image_url': '',
                'is_active': True,
                'created_at': datetime.utcnow(),
                'updated_at': datetime.utcnow()
            },
            {
                'name': 'Industrial Ice Blocks',
                'category': 'block',
                'description': 'Heavy-duty ice blocks for industrial and commercial applications.',
                'price_per_unit': 4.00,
                'unit': 'kg',
                'in_stock': 30,
                'image_url': '',
                'is_active': True,
                'created_at': datetime.utcnow(),
                'updated_at': datetime.utcnow()
            },
            {
                'name': 'Gourmet Ice Spheres',
                'category': 'cube',
                'description': 'Elegant ice spheres for high-end cocktails and presentations.',
                'price_per_unit': 6.00,
                'unit': 'kg',
                'in_stock': 25,
                'image_url': '',
                'is_active': True,
                'created_at': datetime.utcnow(),
                'updated_at': datetime.utcnow()
            },
            {
                'name': 'Crushed Ice',
                'category': 'flake',
                'description': 'Fine crushed ice perfect for smoothies and cold drinks.',
                'price_per_unit': 2.00,
                'unit': 'kg',
                'in_stock': 120,
                'image_url': '',
                'is_active': True,
                'created_at': datetime.utcnow(),
                'updated_at': datetime.utcnow()
            }
        ]
        for ice_data in ice_types_data:
            ice_service.create_ice_type(
                name=ice_data['name'],
                category=ice_data['category'],
                description=ice_data['description'],
                price_per_unit=ice_data['price_per_unit'],
                unit=ice_data['unit'],
                in_stock=ice_data['in_stock'],
                image_url=ice_data['image_url']
            )

        # Create sample orders
        users = list(mongo.db.users.find({'role': 'user'}).limit(2))
        ice_types = list(mongo.db.ice_types.find({'is_active': True}).limit(5))

        if users and ice_types:
            orders_data = [
                {
                    'user_id': users[0]['_id'],
                    'items': [
                        {
                            'ice_type_id': ice_types[0]['_id'],
                            'name': ice_types[0]['name'],
                            'unit_price': ice_types[0]['price_per_unit'],
                            'qty': 2,
                            'line_total': ice_types[0]['price_per_unit'] * 2
                        },
                        {
                            'ice_type_id': ice_types[1]['_id'],
                            'name': ice_types[1]['name'],
                            'unit_price': ice_types[1]['price_per_unit'],
                            'qty': 1,
                            'line_total': ice_types[1]['price_per_unit'] * 1
                        }
                    ],
                    'subtotal': (ice_types[0]['price_per_unit'] * 2) + (ice_types[1]['price_per_unit'] * 1),
                    'tax': ((ice_types[0]['price_per_unit'] * 2) + (ice_types[1]['price_per_unit'] * 1)) * 0.18,
                    'grand_total': ((ice_types[0]['price_per_unit'] * 2) + (ice_types[1]['price_per_unit'] * 1)) * 1.18,
                    'status': 'delivered',
                    'created_at': datetime.utcnow(),
                    'updated_at': datetime.utcnow(),
                    'shipping_address': '123 Main St, City, State 12345'
                },
                {
                    'user_id': users[1]['_id'],
                    'items': [
                        {
                            'ice_type_id': ice_types[2]['_id'],
                            'name': ice_types[2]['name'],
                            'unit_price': ice_types[2]['price_per_unit'],
                            'qty': 3,
                            'line_total': ice_types[2]['price_per_unit'] * 3
                        }
                    ],
                    'subtotal': ice_types[2]['price_per_unit'] * 3,
                    'tax': (ice_types[2]['price_per_unit'] * 3) * 0.18,
                    'grand_total': (ice_types[2]['price_per_unit'] * 3) * 1.18,
                    'status': 'shipped',
                    'created_at': datetime.utcnow(),
                    'updated_at': datetime.utcnow(),
                    'shipping_address': '456 Oak Ave, Town, State 67890'
                },
                {
                    'user_id': users[0]['_id'],
                    'items': [
                        {
                            'ice_type_id': ice_types[3]['_id'],
                            'name': ice_types[3]['name'],
                            'unit_price': ice_types[3]['price_per_unit'],
                            'qty': 1,
                            'line_total': ice_types[3]['price_per_unit'] * 1
                        },
                        {
                            'ice_type_id': ice_types[4]['_id'],
                            'name': ice_types[4]['name'],
                            'unit_price': ice_types[4]['price_per_unit'],
                            'qty': 2,
                            'line_total': ice_types[4]['price_per_unit'] * 2
                        }
                    ],
                    'subtotal': (ice_types[3]['price_per_unit'] * 1) + (ice_types[4]['price_per_unit'] * 2),
                    'tax': ((ice_types[3]['price_per_unit'] * 1) + (ice_types[4]['price_per_unit'] * 2)) * 0.18,
                    'grand_total': ((ice_types[3]['price_per_unit'] * 1) + (ice_types[4]['price_per_unit'] * 2)) * 1.18,
                    'status': 'confirmed',
                    'created_at': datetime.utcnow(),
                    'updated_at': datetime.utcnow(),
                    'shipping_address': '789 Pine Rd, Village, State 54321'
                }
            ]
            for order_data in orders_data:
                order_service.create_order(
                    user_id=order_data['user_id'],
                    items=order_data['items'],
                    shipping_address=order_data['shipping_address']
                )

        print("Database seeded successfully!")

if __name__ == '__main__':
    seed_database()
