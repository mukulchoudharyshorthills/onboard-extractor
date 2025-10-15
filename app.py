from flask import Flask, request, redirect, url_for, render_template, jsonify
from .api_caller import ApiCaller
app = Flask(__name__)

@app.route('/hello')
def hello_world():
   return 'Hello World!'
#app.add_url_rule('/hello', 'hello', hello_world)

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    prompt_file = f"./prompts/prompt_file.txt"
    file_path = f"./input/{file.filename}"
    file.save(file_path)

    caller = ApiCaller(
        api_key=api_key,  # Replace with your actual API key
    )

    data = caller.extract(
        prompt_file=prompt_file,
        path=file_path
    )

    print(data)

    return jsonify({'message': 'File uploaded successfully', 'data': data}), 200

if __name__ == '__main__':
   app.debug = True
   app.run()