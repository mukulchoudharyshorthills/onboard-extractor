from mongodb import get_database
from bson import ObjectId


db = get_database()

if "users" not in db.list_collection_names():
    db.create_collection("users")
users = db['users']

if "loginlogs" not in db.list_collection_names():
    db.create_collection("loginlogs")
loginlogs = db['loginlogs']

if "documents" not in db.list_collection_names():
    db.create_collection("documents")
documents = db['documents']


def user_helper(user) -> dict:
    return {
    "id": str(user["_id"]),
    "username": user["username"],
    "password": user["pwd"],
    "status": user["status"]
    }


def log_helper(log) -> dict:
    return {
    "id": str(log["_id"]),
    "user_id": log["user_id"],
    "login_time": log["login_time"],
    "action": log["action"]
    }

def document_helper(document) -> dict:
    return {
    "id": str(document["_id"]),
    "user_id": document["user_id"],
    "path": document["path"],
    "title": document["title"],
    "tag": document["tag"],
    "data": document["data"],
    "edited_data": document["edited_data"]
    }