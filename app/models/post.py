from flask import current_app
from datetime import datetime
import logging
from bson.objectid import ObjectId

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def save_update_post(post):
    if '_id' in post:
        edited = current_app.db.posts.update_one({'_id': ObjectId(post['_id'])}, {'$set': post})
        if edited.matched_count:
            return True
    updated = current_app.db.posts.insert_one(post)
    if str(updated.inserted_id):
        return True
    return False
    
        