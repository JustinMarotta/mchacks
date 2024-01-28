from api import create_app
from flask import Flask, request, jsonify
from firebase_functions import https_fn
from backend.main_script import run_main

app = create_app()

if __name__ == '__main__':
  app.run(debug = True)

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
def httpsflask(req: https_fn.Request) -> https_fn.Response:
    with app.request_context(req.environ):
        return app.full_dispatch_request()