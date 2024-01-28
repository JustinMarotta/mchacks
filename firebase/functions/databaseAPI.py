from flask import Blueprint, request, jsonify
from firebase_admin import firestore

<<<<<<< HEAD:functions/main.py
from firebase_functions import https_fn, storage_fn
from firebase_admin import initialize_app, firestore, storage, credentials
from flask import Flask, request, jsonify
from backend.main_script import run_main

cred = credentials.Certificate("cred/purplecow-5bb60-b3cfd3302893.json")
initialize_app(cred, {'storageBucket': 'purplecow-5bb60.appspot.com'})

app = Flask(__name__)

# POST Request to upload an image to the firebase storage
@app.route('/upload', methods=['POST'])
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
=======
db = firestore.client()
user_Ref = db.collection('Vocabulary')
>>>>>>> cc70ddf13968172d20b8d45d7dedb99399cbc2dc:firebase/functions/databaseAPI.py

databaseAPI = Blueprint('databaseAPI', __name__)
  
# POST Request to add an element / append images url to the Vocabulary collection
@databaseAPI.route('/add-vocabulary', methods=['POST'])
def add_vocabulary():
    try:
        # Obtain a reference to the Firestore database
        db = firestore.client()

        # Extract the fields from the request's JSON body
        data = request.get_json()
        img = data.get('img')
        noun = data.get('noun')
        source_lang = data.get('source_lang')
        target_lang = data.get('target_lang')

        # Ensure all required fields are present
        if not all([img, noun, source_lang, target_lang]):
            return jsonify({'success': False, 'error': 'Missing required fields'}), 400

        # Check if the noun already exists with the same source_lang and target_lang
        existing_vocab_query = db.collection('Vocabulary').where('noun', '==', noun)
        existing_vocab_docs = list(existing_vocab_query.stream())

        # If the document exists, append img to the imgs field of the document
        if existing_vocab_docs:
            vocab_entry = existing_vocab_docs[0]
            doc_ref = vocab_entry.reference
            doc_ref.update({'imgs': firestore.ArrayUnion([img])})
            # Return a success response indicating the img was appended
            return jsonify({'success': True, 'id': doc_ref.id, 'message': 'Image URL appended to existing vocabulary'}), 200
        else:
            # Construct the new document since it doesn't exist
            vocab_data = {
                'imgs': [img],  # Storing the img as a list to support multiple imgs
                'noun': noun,
                'source_lang': source_lang,
                'target_lang': target_lang,
            }

            # Add the new document to the 'Vocabulary' collection
            vocab_ref = db.collection('Vocabulary').document()
            vocab_ref.set(vocab_data)

            # Return a success response for the created document
            return jsonify({'success': True, 'id': vocab_ref.id}), 201

    except Exception as e:
        # Return an error response if something goes wrong
        return jsonify({'success': False, 'error': str(e)}), 500

# GET Requests to retrieve vocabularies
@databaseAPI.route('/get-vocabulary', methods=['GET'])
def get_all_vocabulary():
    try:
        # Obtain a reference to the Firestore database
        db = firestore.client()

        # Fetch all documents from the 'Vocabulary' collection
        vocab_query = db.collection('Vocabulary').stream()

        # Construct a list to hold all vocabulary entries
        vocab_list = [doc.to_dict() for doc in vocab_query]

        # Return a success response with all vocabulary entries
        return jsonify(vocab_list), 200
    
    except Exception as e:
        # Return an error response if something goes wrong
        return jsonify({'error': str(e)}), 500

#GET Requests to retrieve a specific vocabulary
@databaseAPI.route('/get-vocabulary/<noun>', methods=['GET'])
def get_specific_vocabulary(noun):
    try:
        # Obtain a reference to the Firestore database
        db = firestore.client()

        # Construct a query to find all vocabulary entries with the given noun
        vocab_query = db.collection('Vocabulary').where('noun', '==', noun).stream()

        # Create a list of the returned documents (multiple entries might share the same noun)
        vocab_list = [doc.to_dict() for doc in vocab_query]

        # Check if we found any vocabulary entries
        if vocab_list:
            # Return the found vocabulary entries
            return jsonify(vocab_list), 200
        else:
            # If no entries exist, return a not found error
            return jsonify({'error': 'Vocabulary not found'}), 404
        
    except Exception as e:
        # Return an error response if something goes wrong
        return jsonify({'error': str(e)}), 500
<<<<<<< HEAD:functions/main.py
    

@app.route('translate_image', methods=['POST'])
def translate_image():
    try:
        # get data from req body
        data = request.get_json()
        # run main from backend folder -> translates photo
        result = run_main(data.photo)
        # return whatever run_main returns
        return result
    except Exception as e:
        # return an error if something goes wrong
        return jsonify({'error': str(e)}), 500
    
@https_fn.on_request()
def request(req: https_fn.Request) -> https_fn.Response:

    return https_fn.Response("Hello world!")
=======
>>>>>>> cc70ddf13968172d20b8d45d7dedb99399cbc2dc:firebase/functions/databaseAPI.py
