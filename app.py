from flask import Flask, request, redirect, url_for, render_template, jsonify
from .api_caller import ApiCaller
from models import user_helper, log_helper, users, loginlogs, documents, document_helper
from schemas import UserSchema, UpdateUserSchema, LoginLogSchema, DocumentSchema, UpdateDocumentSchema
import os
import time
from pymongo import MongoClient
from bson import ObjectId

app = Flask(__name__)

@app.route('/ping')
def ping():
   return 'pong!'

@app.route('/login')
def login():
    username = request.args.get('username')
    password = request.args.get('password')
    if not username or not password:
        return jsonify({'error': 'Missing username or password'}), 400

    user = users.find_one({"username": username})
    if not user:
        users.insert_one({"username": username, "password": password, "status": "unverified"})

    user = users.find_one({"username": username})
    loginlogs.insert_one({
        "user_id": user["_id"],
        "timestamp": int(time.time()),
        "action": "login"
    })

    return jsonify({'message': 'Login successful'}), 200

@app.route('/logout')
def logout():
    user_id = request.args.get('id')
    if not user_id:
        return jsonify({'error': 'Missing user id'}), 400

    loginlogs.insert_one({
        "user_id": user_id,
        "timestamp": int(time.time()),
        "action": "logout"
    })

    return jsonify({'message': 'Logout successful'}), 200

@app.route('/upload', methods=['POST'])
def upload_file():
    id = request.form.get('id')
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    file = request.files['file']
    responses = []
    for file_key in request.files:
        file = request.files[file_key]
        if file.filename == '':
            responses.append({'error': 'No selected file', 'filename': file.filename})
            continue

        prompt_file = f"./prompts/prompt_file.txt"
        file_path = f"./input/{file.filename}"
        if os.path.exists(file_path):
            timestamp = int(time.time())
            name, ext = os.path.splitext(file.filename)
            file.filename = f"{name}_{timestamp}{ext}"
            file_path = f"./input/{file.filename}"
        file.save(file_path)
    
    documents.insert_one({
        "user_id": request.form.get('user_id', 'unknown'),
        "path": file_path,
        "title": request.form.get('title', ''),
        "tag": request.form.get('tag', '')
    })

    caller = ApiCaller(
        api_key=api_key,  # Replace with your actual API key
    )


    data = caller.extract(
        prompt_file=prompt_file,
        path=file_path
    )

    result = documents.update_one(
        {"_id": id},
        {"$set": {"data": data, "status": "verified"}}
    )
    
    print(data)
    responses.append({'message': 'File uploaded successfully', 'filename': file.filename, 'data': data})

    return jsonify(responses), 200

@app.route('/verify', methods=['GET'])
def verify():
    id = request.args.get('id')
    if not id:
        return jsonify({'error': 'Missing document id'}), 400

    result = documents.update_one(
        {"_id": id, "status": "unverified"},
        {"$set": {"status": "verified"}}
    )
    return jsonify({'message': 'API is working'}), 200

@app.route('/edit', methods=['POST'])
def edit():
    id = request.args.get('id')
    if not id:
        return jsonify({'error': 'Missing document id'}), 400
    data = request.json
    if not data or "filter" not in data or "update" not in data:
        return jsonify({'error': 'Missing filter or update data'}), 400

    result = documents.update_one(
        {"_id": id, "status": "unverified"},
        {"$set": {"edited_data": data["update"], "status": "verified"}}
    )
    return jsonify({'message': 'API is working'}), 200

if __name__ == '__main__':
   app.debug = True
   app.run()