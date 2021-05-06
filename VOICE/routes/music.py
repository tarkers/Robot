from flask import (
    Blueprint,
    render_template,
    request,
    current_app,
    Response
)
from flask.json import jsonify
from VOICE.reply import words_reply
from ..models import Musicsearch
music = Blueprint('music',__name__,url_prefix='/music',static_folder='static',template_folder='templates')
youtube_search = Musicsearch()


@music.route('/', methods=['GET', 'POST'])
def main():
    global youtube_search
    # music_search=Musicsearch()
    songname=request.values.get('speak')
    if songname==None:
        songname="張惠妹的人質"
    print(songname)
    song,queue_len=youtube_search.songrequire(songname)
    print(song)
   
    return render_template('music.html', artist=song['artist'], albumimg=song['image'], song=song['song'],\
        musicurl=song['musicurl'],album=song['album'],videourl=song['videourl'],queue_len=queue_len)

@music.route('/_get_reply')
def get_reply():
    print("add number")
    speak=request.args.get("speak")
    # result=words_reply("聽周杰倫的擱淺")
    # result=words_reply("暫停播放周杰倫的擱淺")
    result=words_reply(speak)
    return jsonify(result=result)


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
    songname = request.get_json()['song']
    print(songname)
    #testcoed
    if songname==None:
        songname="張惠妹的人質"
    if songname!="Next":
        youtube_search.songlist=[]
        print("clear the song")
    song,queue_len=youtube_search.songrequire(songname)
    print(song)
    return jsonify(artist=song['artist'], albumimg=song['image'],  song=song['song'], musicurl=song['musicurl'],
                   album=song['album'], videourl=song['videourl'],queue_len=queue_len)
