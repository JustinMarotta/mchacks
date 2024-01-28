from flask import request, jsonify
from backend.main_script import run_main
from backend import app
import logging

@app.route("/translate_image", methods=["POST"])
def translate_image():
    try:
        data = request.get_json()
        result = run_main(data['photo'])
        return jsonify(result)
    except Exception as e:
        # Log the error with additional information
        logging.error(f"Error in translate_image: {e}, Data Received: {request.data}")
        
        # Respond with an error message
        return jsonify({'error': 'An error occurred while processing your request'}), 500
