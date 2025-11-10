from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from extensions import mongo
from bson.objectid import ObjectId

class UserService:
    @staticmethod
    def create_user(data: dict) -> str:
        # validate name, email, password_hash
        name = data.get('name')
        email = data.get('email')
        password = data.get('password')
        role = data.get('role', 'user')
        if not name or not email or not password:
            raise ValueError("Name, email, and password are required")
        # lower-case email, unique check
        email = email.lower()
        if UserService.get_user_by_email(email):
            return None
        user = {
            'name': name,
            'email': email,
            'password_hash': generate_password_hash(password),
            'role': role,
            'created_at': datetime.utcnow()
        }
        result = mongo.db.users.insert_one(user)
        return str(result.inserted_id)

    @staticmethod
    def get_user_by_email(email):
        return mongo.db.users.find_one({'email': email})

    @staticmethod
    def get_user_by_id(user_id):
        return mongo.db.users.find_one({'_id': ObjectId(user_id)})

    @staticmethod
    def update_user(user_id, updates):
        return mongo.db.users.update_one(
            {'_id': ObjectId(user_id)},
            {'$set': updates}
        )

    @staticmethod
    def authenticate(email, password):
        user = UserService.get_user_by_email(email)
        if user and check_password_hash(user['password_hash'], password):
            return user
        return None

    @staticmethod
    def get_all_users(page=1, per_page=10, search=None):
        query = {}
        if search:
            query['$or'] = [
                {'name': {'$regex': search, '$options': 'i'}},
                {'email': {'$regex': search, '$options': 'i'}}
            ]
        users = list(mongo.db.users.find(query)
                    .skip((page-1)*per_page)
                    .limit(per_page))
        total = mongo.db.users.count_documents(query)
        return users, total
