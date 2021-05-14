import requests
import re
import os
import execjs
import time
import json
import random
from jsonpath import jsonpath
import datetime
import threading
import multiprocessing as mp
from dotenv import (
    load_dotenv,
    find_dotenv,
    set_key
)
import urllib.request
from google_trans_new import google_translator
from bs4 import BeautifulSoup
from multiprocessing import Pool
from urllib.parse import unquote
from selenium import webdriver, common
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By    # 用於定位元素
from selenium.webdriver.support.wait import WebDriverWait    # 用於設置顯示等待
from selenium.webdriver.support import expected_conditions as EC    # 用於判斷定位元素是否被載入完成
from .model import Artist, Song
'''
語音輸入搜尋部分
'''
load_dotenv()
print("--------------------------")


def chrome_login():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36',
    }
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument("user-agent={}".format(headers))
    chrome_options.add_argument("--mute-audio")
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("--allow-running-insecure-content")
    chrome_options.add_argument(
        "accept-language={}".format('zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7'))
    driver = webdriver.Chrome(ChromeDriverManager().install(
    ), port=0, options=chrome_options)  # 創建有介面的瀏覽器對象
    driver.get("https://music.youtube.com/")
    return driver


driver = chrome_login()


class Musicsearch:
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36',
    }

    def __init__(self):
        self.nowsong = {}
        self.pid = ""
        self.songlist = []
        self.url = ""
        self.firstcheck = False
        self.decodecheck = {
            "path": os.getcwd()+"\static\js\key.js", "key": "BASEKEY"}
        self.checkcount = 0

# -----------------get the six part of the data information----------------
    @classmethod
    def music_renderer(cls, url, findtext):
        soup = BeautifulSoup(requests.get(
            url, headers=Musicsearch.headers).text, "html.parser")
        target = str(soup.find("script", text=re.compile('initialData.push')))
        cleantext = re.sub(re.compile('<.*?>'), '', target)
        get = cleantext[cleantext.find(
            findtext):cleantext.rfind("ytcfg.set(")-3]
        get = get[get.find("data:")+5:].replace("\'", "")
        content = re.sub(
            r'(\\x[a-zA-Z0-9]{2})', lambda x: x.group(1).encode("utf-8").decode("unicode-escape"), get)
        return content

# ---------------- youtube change sig(last to check)-----------------------
    def _updatekey(self, soup, firstfile=True):
        # check the key
        tmpjs = str(soup.find("script", text=re.compile('base.js')))
        basejs = tmpjs[tmpjs.index("jsUrl")+8:tmpjs.index('base.js')]+"base.js"
        if os.getenv("BASEURL") == basejs and firstfile:
            print("--------------------the same jsdata---------------")
        else:
            # get the search page
            text = requests.get("https://www.youtube.com"+basejs).text
            print(basejs, "---------------------------")
            index = text.find('(decodeURIComponent(c))')
            firstkey = text[index-2:index]
            result = re.search(firstkey+'=function'+"(.*?)};", text).group(1)
            firstfunc = "var "+firstkey+"=function"+result+"};"
            secondkey = re.search(r";(.*?)(\[|\.)", result).group(1)
            index = text.find("var "+secondkey)
            tmpline = text[index:index+250]
            secondfunc = tmpline[:tmpline.find('};')+1]
            file = open(self.decodecheck['path'], 'w', encoding="utf-8")
            os.environ["BASEKEY"] = firstkey
            set_key(find_dotenv(), "BASEKEY", os.environ["BASEKEY"])
            os.environ["BASEURL"] = basejs
            set_key(find_dotenv(), "BASEURL", os.environ["BASEURL"])
            file.write(firstfunc+"\n\n"+secondfunc)
            print("update key: "+firstkey+"---------"+secondkey)
            file.close()

    def check_is_video(self):
        self.url = ""
        if('https://i.ytimg.com/' not in self.nowsong['pic']):
            return False
        else:
            self.nowsong['pic'] = ""
            self.url = "https://www.youtube.com/watch?v=" + \
                self.nowsong['sid']
            return True

# ----------------------- get video/audio and next song------------------------
    def get_link(self):
        url = "https://www.youtube.com/watch?v=" + self.nowsong['sid']
        print("view url: ", url)
        soup = BeautifulSoup(requests.get(url).text, "html.parser")

        # update the js key
        if not self.firstcheck:
            self._updatekey(soup)
            self.firstcheck = True

        target = str(soup.find("script", text=re.compile('streamingData')))
        cleanr = re.compile('<.*?>|;')
        cleantext = re.sub(cleanr, '', target).replace(
            "var ytInitialPlayerResponse = ", "")
        cleantext = cleantext[:cleantext.rfind('}')]+"}"
        try:
            unci = json.loads(cleantext)
        except json.decoder.JSONDecodeError:
            return False
        formats = jsonpath(unci, '$..adaptiveFormats[*]')
        formats.append(jsonpath(unci, '$..formats[0]')[0])

        # get the audio  keep this audio data or it can change to video mode
        audio = formats[-2]

        if "url" in audio:
            self.url = audio['url']
        else:
            with open(self.decodecheck["path"]) as f:
                funcstring = f.read()
                f.close()
                self.url = self.link_combination(
                    execjs.compile(funcstring), audio)
            try:
                urllib.request.urlopen(self.url)
            except urllib.error.HTTPError:
                print("-------------key need update!!--------------")
                self._updatekey(soup, False)
                with open(self.decodecheck["path"]) as f:
                    funcstring = f.read()
                    f.close()
                    self.url = self.link_combination(
                        execjs.compile(funcstring), audio)
        return True

    def link_combination(self, sigfunc, src):
        key = os.getenv(self.decodecheck["key"])
        splitlink = src["signatureCipher"].split('&')
        siglist = unquote(splitlink[0].replace("s=", ""))
        link = unquote(splitlink[2].replace("url=", "")) + \
            "&sig=" + sigfunc.call(key, siglist)
        return link
 # ---------------------- search page from the speakdata--------------------------

    def id_search(self, d):
        self.nowsong = Musicsearch.form_song_dict(
            d.sname, d.cname, d.aname, d.sid, d.cid, d.aid, d.pic)
        if self.check_is_video():
            return True
        else:
            return self.get_link()

    @classmethod
    def select_best(cls, speakdata, choice):
        if '歌曲' not in choice:
            return False
        elif '熱門搜尋結果' not in choice:
            best_data = choice['歌曲']
        else:
            for key,value in choice.items() :
                print (key)
            ch = speakdata[-1]
            en = speakdata.split(' ')[-1].split('的')[-1]
            print("ch: ", ch, "en: ", en, "----------")
            if "版" == ch or en in ['lyrics', 'live', 'MV'] or 'googleusercontent' in choice['熱門搜尋結果']['pic']:
                best_data = choice['熱門搜尋結果']
            else:
                hot_low_mix = ""
                langoption = []
                translator = google_translator()
                results = translator.detect(choice['歌曲']['sname'])[0]
                cnamelower = choice['歌曲']['cname'].replace(" ", "").lower()
                songcheck = re.sub(
                    r"\(.*?\)", "", choice['歌曲']['sname']).lower()
                try:
                    hottw = choice['熱門搜尋結果']['sname'].lower()
                    if translator.detect(hottw)[0] == "zh-CN":
                        hottw = translator.translate(hottw, lang_tgt='zh-TW')
                    hot_low_mix = hottw.replace(" ", "")
                except KeyError:
                    hot_low_mix = choice['熱門搜尋結果']['sname']
                if "的" in speakdata:
                    speaklower = speakdata.lower().split("的")[-1].strip()
                else:
                    speaklower = speakdata.lower().strip()

                taiwanese = translator.translate(
                    songcheck, lang_tgt='zh-TW').lower().strip()
                english = translator.translate(
                    songcheck, lang_tgt='en').lower().strip()

                # langoption append
                langoption.append(translator.translate(
                    songcheck, lang_tgt=results).strip())
                langoption.append(songcheck)
                langoption.append(taiwanese)
                langoption.append(english)
                if "not" in english:
                    langoption.append(english.replace(" not", "n't"))
                songcheck = songcheck.replace(" ", "")

                print(speaklower, langoption, cnamelower, songcheck, taiwanese, hot_low_mix,
                choice['熱門搜尋結果']['cid'] == choice['歌曲']['cid'] or cnamelower in hot_low_mix,
                      speaklower in langoption or songcheck in hot_low_mix or taiwanese in hot_low_mix)
                print(choice['歌曲'], "\n", choice['熱門搜尋結果'])
                # test code

                if (choice['熱門搜尋結果']['cid'] == choice['歌曲']['cid'] or cnamelower in hot_low_mix) \
                        and (speaklower in langoption or songcheck in hot_low_mix or taiwanese in hot_low_mix):
                    best_data = choice['歌曲']
                else:
                    best_data = choice['熱門搜尋結果']
        return best_data

    def page_search(self, speakdata):
        best_data = None
        choice = {}
        url = "https://music.youtube.com/search?q=" + \
            speakdata.replace(" ", "+")
        print('page_search: ', url)

        content = Musicsearch.music_renderer(url, "path: '\/search',")
        dataget = jsonpath(json.loads(content.replace(
            "\\\\", "\\")), "$..musicShelfRenderer")
        # no data
        if not dataget:
            return False
        for data in dataget:
            # six part
            nameget = jsonpath(data, "$.title[runs][0][text]")[0]
            # if nameget in ["演出者", "專輯", "播放清單"]:
            if nameget in ["演出者", "專輯", "播放清單", "社群播放清單"]:
                continue
            videoid = jsonpath(
                data, "$..playNavigationEndpoint.watchEndpoint[videoId]")
            print(videoid, nameget, "--------")
            if videoid == False:
                continue
            else:
                videoid = videoid[0]

            aid, aname = "", ""
            choice[nameget] = {}
            pic = jsonpath(data, "$..thumbnails[0][url]")[0]
            try:
                cid = jsonpath(data, "$..browseId")[0]
            except TypeError:
                cid="none"


            title = jsonpath(
                data, "$..accessibilityPlayData.accessibilityData.label")[0]
            # print(title)
            title = re.sub(r'播放「|」', '', title).rsplit(" - ", 1)
            if 'googleusercontent' in pic:
                aname = jsonpath(data,
                                 "$..flexColumns[-1:].musicResponsiveListItemFlexColumnRenderer.text.runs[-3:].text")[0]
                aid = jsonpath(data,
                               "$..flexColumns[-1:].musicResponsiveListItemFlexColumnRenderer.text.runs[-3:].navigationEndpoint.browseEndpoint.browseId")[0]
            pid = jsonpath(
                data, "$..playNavigationEndpoint[watchEndpoint][playlistId]")
            if pid != False:
                pid = pid[0]
            else:
                pid = ""
            choice[nameget] = Musicsearch.form_song_dict(
                title[0], title[1], aname, videoid, cid, aid, pic, pid)
            print(aname, "----aname----")

        # choose the best data
        print(speakdata, choice)
        best_data = Musicsearch.select_best(speakdata, choice)
        # search error
        if not best_data:
            return False
        if 'googleusercontent' in best_data['pic']:
            # check song id
            data = Song.check_data(best_data['sid'])
            if data == None:
                artist = Artist.check_data(best_data['cid'])
                if artist == None:
                    url = 'https://music.youtube.com/channel/'+best_data['cid']
                    content = Musicsearch.music_renderer(
                        url, "path: '\/browse',")
                    if content == None:
                        print('no content', artist)

                    content = json.loads(content.replace("\\\\", "\\"))
                    dataget = jsonpath(
                        content, "$..thumbnail.thumbnails[0].url")
                    if dataget == False:
                        print(
                            "----------youtube does not  have this artist----------")
                        best_data['aid'] = best_data['cid']
                        best_data['cid'] = 'none'
                    else:
                        # add new artist
                        piclink = dataget[-1]
                        newartist = Artist(
                            best_data['cid'], best_data['cname'], piclink)
                        newartist.add_artist()
                        print(piclink, best_data['cname'],
                              "-------add new artist-------")
                # add the new song
                newdata = Song(best_data['cid'], best_data['cname'], best_data['sid'], best_data['sname'],
                               best_data['pic'], best_data['aid'], best_data['aname'])
                newdata.add_song()
                print(best_data['sname'], "------ add song to db--------")

            # update the data pic -- remove it when its  all youtube data
            elif 'googleusercontent' not in data.pic:
                Song.updatepic(best_data['aid'], best_data['pic'])
                print(best_data['aname'], '----------update pic-----------')

        self.pid = best_data['pid']
        self.nowsong = best_data
        if self.check_is_video():
            return True
        else:
            return self.get_link()  # get the link data

    def get_songqueue(self):
        global driver
        self.songlist = []
        url = "https://music.youtube.com/watch?v="+self.nowsong['sid']
        if self.pid != "":
            print("https://music.youtube.com/watch?v=" +
                  self.nowsong['sid']+"&list="+self.pid, "\npid url")
            url = "https://music.youtube.com/watch?v=" + \
                self.nowsong['sid']+"&list="+self.pid
        print(url, "-------song queue---------------")
        driver.get(url)
        wait = WebDriverWait(driver, 30)
        element = wait.until(EC.visibility_of_all_elements_located(
            (By.XPATH, '//*[@id="tab-renderer"]')))
        randomicon = driver.find_element_by_xpath(
            '//*[@id="right-controls"]/div/tp-yt-paper-icon-button[3]')
        randomicon.click()
        time.sleep(0.5)
        tmp = element[0]  # need to check if element is null
        for i in range(0, 3):
            driver.execute_script('arguments[0].scrollTop = '+str(i*500), tmp)
            time.sleep(0.8)
        playicon = driver.find_element_by_xpath('//*[@id="play-pause-button"]')
        print(playicon.get_attribute('title'), "the play button")
        if playicon.get_attribute("title") == "暫停":
            playicon.click()
        content = driver.page_source
        soup = BeautifulSoup(content, "html.parser")
        queue = soup.findAll('ytmusic-player-queue-item',
                             class_="style-scope ytmusic-player-queue")
        isvideo = False
        wholedata = []
        print(len(queue))
        for item in queue:
            target = item.find('img', src=re.compile("^https://"))
            # print(target)
            if target == None:
                continue
            imglink = target['src']
            test = item.findAll('yt-formatted-string')
            data = Musicsearch.form_song_dict(
                test[0]['title'], test[1]['title'], "", "", "", "", imglink, self.pid)
            if "https://i.ytimg.com/" in imglink:  # video id
                data['sid'] = re.search('vi/(.*?)/', imglink).group(1)
                isvideo = True
            wholedata.append(data)
        if not isvideo:  # music id
            io = []
            ids = driver.find_elements_by_xpath('//*[@id="play-button"]')
            for ww in ids:
                opop = ww.get_property(
                    'data')['playNavigationEndpoint']['watchEndpoint']['videoId']
                if opop not in io:
                    io.append(opop)
            print(len(wholedata), len(io))
            # print(wholedata,io)
            for i in range(len(io)):
                wholedata[i]['sid'] = io[i]
        print("isvideo:", isvideo)
        # driver.close()
        print(len(wholedata), "--------whole list------")
        for da in wholedata[1:]:
            data = None
            if not isvideo:  # music
                data = Song.check_data(da['sid'])
                # need to add new song to database
                if data == None:
                    print(da['sid'], "--sid not in database--")
                    namesearch = (
                        da['cname']+"+"+re.sub(r'\(.*?\)', '', da['sname'])).replace(" ", "+")
                    url = "https://music.youtube.com/search?q=" + namesearch
                    print(url, "new song")
                    content = Musicsearch.music_renderer(
                        url, "path: '\/search',")
                    dataget = jsonpath(json.loads(content.replace(
                        "\\\\", "\\")), "$..musicShelfRenderer")
                    for inform in dataget:
                        found = False
                        sids = jsonpath(
                            inform, "$..playNavigationEndpoint.watchEndpoint[videoId]")
                        if sids == False:
                            continue
                        for i in range(len(sids)):
                            if sids[i] == da['sid']:
                                found = True
                                da['cid'] = jsonpath(inform, "$..browseId")[i]
                                da['aname'] = jsonpath(inform,
                                                       "$..flexColumns[-1:].musicResponsiveListItemFlexColumnRenderer.text.runs[-3:].text")[i]
                                da['aid'] = jsonpath(inform,
                                                     "$..flexColumns[-1:].musicResponsiveListItemFlexColumnRenderer.text.runs[-3:].navigationEndpoint.browseEndpoint.browseId")[i]
                                data = Song(
                                    da['cid'], da['cname'], da['sid'], da['sname'], da['pic'], da['aid'], da['aname'])
                                data.add_song()
                                print(
                                    da, "--------nextsong update the song-----------")
                                break
                        if found:
                            break
                elif data.pic == "default":
                    Song.updatepic(data.aid, da['pic'])
                    print(data.sname, data.cname, data.aname,
                          '----------update pic-----------')
            if data != None:
                self.songlist.append(data)
            else:
                self.songlist.append(Song(
                    da['cid'], da['cname'], da['sid'], da['sname'], da['pic'], da['aid'], da['aname']))
        playicon = driver.find_element_by_xpath('//*[@id="play-pause-button"]')
        if playicon.get_attribute("title") == "暫停":
            print("---still playing----")
            playicon.click()
            time.sleep(0.5)
        print(self.songlist, "\n-------------songlistfinish---------------")

    @classmethod
    def form_song_dict(cls, sname, cname, aname, sid, cid, aid, pic, pid=None):
        data = {
            'sname': sname,
            'cname': cname,
            'aname': aname,
            'sid': sid,
            'cid': cid,
            'aid': aid,
            'pic': pic,
            'pid': pid,
        }
        return data

    def songrequire(self, speak_words, isartist=False):
        isnext = False
        data = None
        # play the next song
        if "Next" in speak_words: #songlist aussume >0
            try:
                data = self.songlist.pop()
            except IndexError:
                return "已播放完畢"
        # play the whole artist
        elif isartist:
            artist_songs = Song.get_singer_song(speak_words)
            if artist_songs != None:
                self.songlist = artist_songs
                data = self.songlist.pop()
            else:
                speak_words = speak_words+"的歌"  # test new data
        # chcek the data
        if data != None:
            song = Musicsearch.get_song(data)
            noerror = self.id_search(data)   # has id
            if not noerror:
                # test code
                if isnext and len(self.songlist) > 0:
                    noerror=self.id_search(self.songlist.pop(0))
                else:
                    noerror=self.page_search(
                        self.nowsong['cname']+" "+self.nowsong['sname'])
        else:
            noerror = self.page_search(speak_words)  # no id
            song = Musicsearch.get_song(self.nowsong)
        
        song['url'] = self.url
        if not noerror:
            return "找不到歌曲"      
        elif "https://www.youtube.com/" in song['url']:
            song['is_video']=True
        else:
            song['is_video']=False
        if  'googleusercontent' in song['pic']:
            song['pic'] = re.sub(
                r'=w(.*?)-h(.*?)-', '=w600-h600-', song['pic'])
        song['queue_len']=len(self.songlist)
        return song

    @classmethod
    def get_song(cls, data):
        song = {
            'artist': "",
            'pic': "",
            'song': "",
            'url': "",
            'album': "",
        }
        if type(data) == dict:
            print(data)
            song['pic'] = data['pic']
            song['album'] = data['aname']
            song['artist'] = data['cname']
            song['song'] = data['sname']
        else:
            if data.pic == 'default':
                song['pic'] = Artist.check_data(data.cid).pic
            else:
                song['pic'] = data.pic
            song['album'] = data.aname
            song['artist'] = data.cname
            song['song'] = data.sname
        return song
