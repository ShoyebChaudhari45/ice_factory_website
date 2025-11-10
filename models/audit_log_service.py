from datetime import datetime
from extensions import mongo
from bson.objectid import ObjectId

class AuditLogService:
    @staticmethod
    def log_action(actor_user_id, action, target_collection, target_id, payload=None):
        log_entry = {
            'actor_user_id': ObjectId(actor_user_id),
            'action': action,
            'target_collection': target_collection,
            'target_id': ObjectId(target_id) if target_id else None,
            'payload': payload,
            'created_at': datetime.utcnow()
        }
        mongo.db.audit_logs.insert_one(log_entry)

    @staticmethod
    def get_audit_logs(page=1, per_page=50):
        logs = list(mongo.db.audit_logs.find()
                   .sort('created_at', -1)
                   .skip((page-1)*per_page)
                   .limit(per_page))
        total = mongo.db.audit_logs.count_documents({})
        return logs, total
