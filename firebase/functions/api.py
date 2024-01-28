from flask import Flask
from firebase_admin import credentials, initialize_app

cred = credentials.Certificate('./credentials.json')

default_app = initialize_app(cred, {'storageBucket': 'purplecow-5bb60.appspot.com'})

def create_app():
  app = Flask(__name__)
  app.config['SECRET_KEY'] = '12345rtfescdvf'

  from storageAPI import storageAPI
  from databaseAPI import databaseAPI

  app.register_blueprint(storageAPI, url_prefix='/storage')
  app.register_blueprint(databaseAPI, url_prefix='/db')

  return app
