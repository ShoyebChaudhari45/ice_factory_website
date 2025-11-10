from datetime import datetime
from extensions import mongo
from bson.objectid import ObjectId
from .ice_type_service import IceTypeService

class OrderService:
    @staticmethod
    def create_order(user_id, items, shipping_address, tax_rate=0.18):
        subtotal = sum(item['line_total'] for item in items)
        tax = subtotal * tax_rate
        grand_total = subtotal + tax

        # Validate and decrement stock
        for item in items:
            ice_type = IceTypeService.get_ice_type_by_id(item['ice_type_id'])
            if not ice_type or ice_type['in_stock'] < item['qty']:
                return None, f"Insufficient stock for {ice_type['name']}"
            IceTypeService.update_stock(item['ice_type_id'], ice_type['in_stock'] - item['qty'])

        order = {
            'user_id': ObjectId(user_id),
            'items': items,
            'subtotal': subtotal,
            'tax': tax,
            'grand_total': grand_total,
            'status': 'pending',
            'shipping_address': shipping_address,
            'created_at': datetime.utcnow(),
            'updated_at': datetime.utcnow()
        }
        result = mongo.db.orders.insert_one(order)
        order['_id'] = result.inserted_id
        return order, None

    @staticmethod
    def get_order_by_id(order_id):
        return mongo.db.orders.find_one({'_id': ObjectId(order_id)})

    @staticmethod
    def get_orders_by_user(user_id, page=1, per_page=10):
        orders = list(mongo.db.orders.find({'user_id': ObjectId(user_id)})
                     .sort('created_at', -1)
                     .skip((page-1)*per_page)
                     .limit(per_page))
        total = mongo.db.orders.count_documents({'user_id': ObjectId(user_id)})
        return orders, total

    @staticmethod
    def get_all_orders(page=1, per_page=10, status=None, date_from=None, date_to=None):
        query = {}
        if status:
            query['status'] = status
        if date_from or date_to:
            query['created_at'] = {}
            if date_from:
                query['created_at']['$gte'] = datetime.fromisoformat(date_from)
            if date_to:
                query['created_at']['$lte'] = datetime.fromisoformat(date_to)

        orders = list(mongo.db.orders.find(query)
                     .sort('created_at', -1)
                     .skip((page-1)*per_page)
                     .limit(per_page))
        total = mongo.db.orders.count_documents(query)
        return orders, total

    @staticmethod
    def update_order_status(order_id, new_status):
        return mongo.db.orders.update_one(
            {'_id': ObjectId(order_id)},
            {'$set': {'status': new_status, 'updated_at': datetime.utcnow()}}
        )

    @staticmethod
    def cancel_order(order_id):
        order = OrderService.get_order_by_id(order_id)
        if order and order['status'] in ['pending', 'confirmed']:
            # Restore stock
            for item in order['items']:
                ice_type = IceTypeService.get_ice_type_by_id(item['ice_type_id'])
                if ice_type:
                    IceTypeService.update_stock(item['ice_type_id'], ice_type['in_stock'] + item['qty'])
            return mongo.db.orders.update_one(
                {'_id': ObjectId(order_id)},
                {'$set': {'status': 'cancelled', 'updated_at': datetime.utcnow()}}
            )
        return None

    @staticmethod
    def get_order_stats():
        pipeline = [
            {'$group': {
                '_id': None,
                'total_orders': {'$sum': 1},
                'total_revenue': {'$sum': '$grand_total'},
                'pending_orders': {'$sum': {'$cond': [{'$eq': ['$status', 'pending']}, 1, 0]}},
                'confirmed_orders': {'$sum': {'$cond': [{'$eq': ['$status', 'confirmed']}, 1, 0]}},
                'shipped_orders': {'$sum': {'$cond': [{'$eq': ['$status', 'shipped']}, 1, 0]}},
                'delivered_orders': {'$sum': {'$cond': [{'$eq': ['$status', 'delivered']}, 1, 0]}},
                'cancelled_orders': {'$sum': {'$cond': [{'$eq': ['$status', 'cancelled']}, 1, 0]}}
            }}
        ]
        result = list(mongo.db.orders.aggregate(pipeline))
        return result[0] if result else {}

    @staticmethod
    def get_orders_by_date_range(date_from, date_to):
        query = {
            'created_at': {
                '$gte': datetime.fromisoformat(date_from),
                '$lte': datetime.fromisoformat(date_to)
            }
        }
        return list(mongo.db.orders.find(query).sort('created_at', -1))
