from flask import Flask
from flask.json import jsonify
# from flask_cors import CORS, cross_origin
from flask_sqlalchemy import SQLAlchemy
# from .routes.music import music
    
from api import app
# cors = CORS(app)
# app.config['CORS_HEADERS'] = 'Content-Type'
# app.register_blueprint(music)
db=SQLAlchemy(app)
@app.route('/time',methods=['POST'])
# @cross_origin()
def get_current_time():
    print("on time")
    return jsonify(artist="test",mail="mail")



