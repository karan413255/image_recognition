from flask import Flask, request, send_file, jsonify
from flask_cors import CORS
import os
import tempfile
from matcher import find_and_zip_matches

app = Flask(__name__)
CORS(app)

@app.route('/match-faces', methods=['POST'])
def match_faces():
    input_image = request.files.get('input_image')
    folder_path = request.form.get('folder_path')
    user_name = request.form.get('user_name')

    if not input_image or not folder_path or not user_name:
        return jsonify({'error': 'Missing required inputs'}), 400

    with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as tmp:
        input_image.save(tmp.name)
        zip_path, face_count = find_and_zip_matches(tmp.name, folder_path, user_name)

    print(f"Total faces found in input: {face_count}")
    return send_file(zip_path, as_attachment=True, download_name=f"{user_name}_matches.zip")

@app.route('/test', methods=['GET'])
def test():
    return jsonify({'message': 'API is working!'}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
