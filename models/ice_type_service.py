from datetime import datetime
from extensions import mongo
from bson.objectid import ObjectId

class IceTypeService:
    @staticmethod
    def create_ice_type(name, category, description, price_per_unit, unit, in_stock, image_url=''):
        if IceTypeService.get_ice_type_by_name(name):
            return None
        ice_type = {
            'name': name,
            'category': category,
            'description': description,
            'price_per_unit': price_per_unit,
            'unit': unit,
            'in_stock': in_stock,
            'image_url': image_url,
            'is_active': True,
            'created_at': datetime.utcnow(),
            'updated_at': datetime.utcnow()
        }
        result = mongo.db.ice_types.insert_one(ice_type)
        ice_type['_id'] = result.inserted_id
        return ice_type

    @staticmethod
    def get_ice_type_by_name(name):
        return mongo.db.ice_types.find_one({'name': name})

    @staticmethod
    def get_ice_type_by_id(ice_type_id):
        return mongo.db.ice_types.find_one({'_id': ObjectId(ice_type_id)})

    @staticmethod
    def get_active_ice_types(page=1, per_page=10, search=None, category=None, price_min=None, price_max=None):
        query = {'is_active': True}
        if search:
            query['name'] = {'$regex': search, '$options': 'i'}
        if category:
            query['category'] = category
        if price_min is not None:
            query['price_per_unit'] = {'$gte': price_min}
        if price_max is not None:
            if 'price_per_unit' in query:
                query['price_per_unit']['$lte'] = price_max
            else:
                query['price_per_unit'] = {'$lte': price_max}
        ice_types = list(mongo.db.ice_types.find(query)
                        .skip((page-1)*per_page)
                        .limit(per_page))
        total = mongo.db.ice_types.count_documents(query)
        return ice_types, total

    @staticmethod
    def get_all_ice_types(page=1, per_page=10, search=None):
        query = {}
        if search:
            query['name'] = {'$regex': search, '$options': 'i'}
        ice_types = list(mongo.db.ice_types.find(query)
                        .skip((page-1)*per_page)
                        .limit(per_page))
        total = mongo.db.ice_types.count_documents(query)
        return ice_types, total

    @staticmethod
    def update_ice_type(ice_type_id, updates):
        updates['updated_at'] = datetime.utcnow()
        return mongo.db.ice_types.update_one(
            {'_id': ObjectId(ice_type_id)},
            {'$set': updates}
        )

    @staticmethod
    def delete_ice_type(ice_type_id):
        return mongo.db.ice_types.delete_one({'_id': ObjectId(ice_type_id)})

    @staticmethod
    def toggle_active(ice_type_id):
        ice_type = IceTypeService.get_ice_type_by_id(ice_type_id)
        if ice_type:
            return mongo.db.ice_types.update_one(
                {'_id': ObjectId(ice_type_id)},
                {'$set': {'is_active': not ice_type['is_active'], 'updated_at': datetime.utcnow()}}
            )
        return None

    @staticmethod
    def update_stock(ice_type_id, new_stock):
        return mongo.db.ice_types.update_one(
            {'_id': ObjectId(ice_type_id)},
            {'$set': {'in_stock': new_stock, 'updated_at': datetime.utcnow()}}
        )

    @staticmethod
    def get_low_stock_items(threshold=10):
        return list(mongo.db.ice_types.find({'in_stock': {'$lte': threshold}, 'is_active': True}))
