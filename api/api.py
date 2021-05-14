from flask import Flask ,render_template ,Response
from flask.json import jsonify
import cv2
from flask_sqlalchemy import SQLAlchemy
from .models import retrieve_score ,get_answer
from api import app
# cors = CORS(app)
db=SQLAlchemy(app)
data=""

@app.route('/time',methods=['POST'])
def get_current_time():
    print("on time")
    return jsonify(artist="test",mail="mail")

@app.route('/give_grade',methods=['GET'])
def give_grade():
    answer =get_answer()
    return jsonify(answer=answer)

@app.route('/video_feed')
def video_feed():
    return Response(retrieve_score(), mimetype='multipart/x-mixed-replace; boundary=frame')



