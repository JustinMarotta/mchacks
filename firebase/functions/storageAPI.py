from flask import Blueprint, request, jsonify
from firebase_admin import firestore, storage

storageAPI = Blueprint('storageAPI', __name__)

@storageAPI.route('/upload', methods=['POST'])
def upload_image():
    try:
        # Access the uploaded file from the request
        uploaded_file = request.files['file']

        # Get a reference to the Storage bucket
        bucket = storage.bucket()

        # Define the Storage path where you want to upload the image
        storage_path = 'files/Images/'

        # Upload the file to Firebase Storage
        blob = bucket.blob(storage_path + uploaded_file.filename)
        blob.upload_from_file(uploaded_file)
        blob.make_public()

        # Get the public URL of the uploaded file
        public_url = blob.public_url

        # Return a JSON response with the public URL
        return jsonify({'success': True, 'url': public_url}), 200
    except Exception as e:
        # Return an error response if something goes wrong
        return jsonify({'success': False, 'error': str(e)}), 500