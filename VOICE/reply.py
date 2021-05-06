import jieba
import jieba.analyse
# import re
# 100 check the test
WORD_DATA = {
    # 'Robot': {"name":"電腦","reply":{"label":"Call","reply":"請說"}},  # test the code
    'Error':{"label":"error","reply":"抱歉，我聽不懂"},
    "Music": {
        "Get": [
            {"播放": 35, "聽": 10, "歌": 5,"歌曲":5,"的":5},  # 35
            {"下":5,"一首": 25, "播放": 15},  # 65
            {"大聲": 40,"調大聲":30,"調大":30,  "一點": 20},  # 40
            {"小聲": 40, "調小聲":30,"調小":30,"一點": 20},  # 40
            {"停止": 40, "暫停": 30, "播放": 10},
            {"繼續": 40, "播放": 5},  # 50
            {"音量": 20, "聲音": 10, "調到": 30,"調為":20,"調成":20},  # 50
            {"音量": 20, "聲音": 10, "多少": 40, "多大": 40}  # 60
        ],
        "Back": [
            {"label":"Play","reply":"好的，請稍等片刻"},
            {"label":"Next","reply":"好的，為您播放下一首"},
            {"label":"Volume_up","reply":"好的，音量調大為"},
            {"label":"Volume_down","reply":"好的，音量調小為"},
            {"label":"Stop","reply":"音樂暫停"},
            {"label":"Continue","reply":""},
            {"label":"Volume_set","reply":"好的，為您調整音量為"},
            {"label":"Volume_show","reply":"現在的音量是"},
        ]
    }
}


def words_reply(text:str ="測試檔案", page: str="Music"):
    # if text==WORD_DATA['Robot']['name']:
    #     return WORD_DATA['Robot']['reply']
    # else:
    speaklist = jieba.lcut(text, cut_all=False, HMM=True)
    print(speaklist)
    return check_data_intersection(speaklist, page)


def check_data_intersection(speakdata: list, page: str):
    best_weight = 0
    best_line = 0
    for i, data in enumerate(WORD_DATA[page]["Get"]):
        intersect_keys = data.keys() & speakdata
        speak_weight = sum([data[key] for key in intersect_keys])
        if speak_weight > best_weight:
            best_weight, best_line = speak_weight, i
    if best_weight>10:
        return WORD_DATA[page]["Back"][best_line]
    else:
        return WORD_DATA["Error"]
