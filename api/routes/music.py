from flask import (
    Blueprint,
    render_template,
    request,
    current_app,
    Response
)
from flask.json import jsonify
from flask_cors import CORS, cross_origin
from ..models import Musicsearch
music = Blueprint('music',__name__,url_prefix='/music',static_folder='static')
CORS(music)
youtube_search = Musicsearch()
@music.route('/')
def main():
    response = jsonify(artist="opoij")
    return response




@music.route('/preload_songs',methods=['GET'])
def preload_songs():
    global youtube_search
    if len(youtube_search.songlist)<2:
        youtube_search.get_songqueue()
    print(youtube_search.songlist)
    return  Response(status=200)

@music.route('/change_song',methods=['POST'])
def change_song():
    global youtube_search
    try:
       songname = request.get_json()['song']
       is_artist = request.get_json()['is_artist']
    except KeyError:
       songname = None
       
    #test code
    if songname==None:
        songname="張惠妹的人質"
    if songname!="Next":
        youtube_search.songlist=[]
    
    song=youtube_search.songrequire(songname,is_artist)
    if type(song) == str:
      return jsonify(speak=song)
    else:
        return jsonify(artist=song['artist'], pic=song['pic'],  song=song['song'], url=song['url'],
                   album=song['album'],queueLen=song['queue_len'],isVideo=song['is_video'])


