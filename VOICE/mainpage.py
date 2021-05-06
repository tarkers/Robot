from dotenv import (
    load_dotenv,
    find_dotenv,
    set_key
)
import os
from flask import(
    render_template,
    request,
    jsonify
)
from VOICE import app
from .reply import words_reply
from flask_sqlalchemy import SQLAlchemy
import pymysql
db=SQLAlchemy(app)
@app.route('/')
def index():
    # db.create_all()
    load_dotenv()
    print(os.environ.get('PASSWORD'))
    return render_template('main.html')

@app.route('/_get_reply')
def get_reply():
    print("add number")
    speak=request.args.get("speak")
    
    # result=words_reply("聽周杰倫的擱淺")
    # result=words_reply("暫停播放周杰倫的擱淺")
    result=words_reply(speak)
    return jsonify(result=result)
    