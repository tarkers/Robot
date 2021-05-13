var recordsound = new webkitSpeechRecognition()
var isvideo = false
var callrobot = false
var callpause = false
var calllabel="Call"
var speakwords = ""
var queue_len = 5
var xhr, playsong = null
var audioplayer,videoplayer ,interval_btn
var userpause = true;
var mediainterval = undefined;
var recotimeout = undefined;
var nospeak = undefined;
var miniwindow = false;
var path=window.location.pathname
console.log(path)
recordsound.continuous = true
recordsound.interimResults = false
recordsound.onend = function () {
    callrobot = false
    console.log("onend", this)
    this.start()
}
recordsound.onstart = function () {
    console.log('start')
}

const get_date = () => {
    var today = new Date();
    var currentDateTime =
        today.getFullYear() + '年' +
        (today.getMonth() + 1) + '月' +
        today.getDate() + '日' +
        today.getHours() + '點' + today.getMinutes() +
        '分';
    return currentDateTime
}

recordsound.onresult = function (event) {
    if (event.results[0].isFinal) {
        var i = event.resultIndex
        var j = event.results[i].length - 1
        speakwords = event.results[i][j].transcript
        if(speakwords == "電腦"){
            reply_motion('Call', '請說')
        }
        else if (callrobot) {
            $.getJSON(path+'_get_reply', {
                speak: speakwords
            }).done((data) => {
                data = data.result
                reply_motion(data['label'], data['reply'])
                console.log(data['label'])
            })
        }
        console.log(speakwords)
    }
};
const bound_number = (num, maxn = 1, minn = 0) => {
    switch (num) {
        case maxn <= num:
            return maxn
        case minn >= num:
            return maxn
        default:
            return num
    }
}
const reply_motion = (label, reply) => {
    if (nospeak != undefined) {
        clearTimeout(nospeak)
    }
    switch (label) {
        case "Call":
            callrobot = true
            nospeak = setTimeout(() => callrobot = false, 15000)
            break;
        case "Play":
            callpause=false
            if (speakwords.substring(0, 3).includes("播放")) {
                speakwords = speakwords.replace("播放", "")
            }
            if (path == "/") {
                $('input[name="speak"]').val(speakwords)
                console.log($('input[name="speak"]').val())
                $('#music-form').submit()
                console.log(speakwords)
            } else { //music
                changesong(speakwords)
                queue_len=0  //test
            }
            break
        case "Next":
            callpause=false
            changesong("Next")
            break
        case "Volume_up":
            audioplayer.volume = bound_number(audioplayer.volume + 0.15)
            reply = reply + (audioplayer.volume * 100).toString() + "%"
            break
        case "Volume_down":
            audioplayer.volume = bound_number(audioplayer.volume - 0.15)
            reply = reply + (audioplayer.volume * 100).toString() + "%"
            break
        case "Volume_set":
            const numberPattern = /\d+/g;
            let vol_number = speakwords.match(numberPattern)[0]
            audioplayer.volume = bound_number(parseInt(vol_number) / 100)
            reply = reply + vol_number.toString() + "%"
            break
        case "Volume_show":
            reply = reply + (audioplayer.volume * 100).toString() + "%"
            break
        case "Continue":
            callpause = false

            break
        case "Stop":
            callpause = true
            mediacontrol(false)
            break
        default:
            break;
    }
    calllabel=label
    responsiveVoice.speak(reply, "Chinese Taiwan Male",responsive_param); //male to speak the task   
}
function voiceStartCallback() {
    if (path== "/music/") {
        mediapause()
    }
    console.log("Voice started");
}
 
function voiceEndCallback() {
    if (calllabel != "Call") {
        if (!["Next","Play","Stop"].includes(calllabel) ) {
            mediacontrol()
        }
        callrobot = false
    }
}
var responsive_param = {
    onstart: voiceStartCallback,
    onend: voiceEndCallback
}

function preload_songs() {
    if (queue_len < 2) {
        console.log("preload", path)
        if (xhr != null) {
            xhr.abort()
        }
        xhr = $.ajax({
            type: "GET",
            url:path + "preload_songs",
            success: function (res) {
                console.log(res)
            },
        });
    }
}

function changesong(songname) {
    console.log(songname,"songname")
    $.ajax({
        url: path+'change_song',
        type: 'POST',
        contentType: 'application/json; charset=utf-8',
        dataType: 'json',
        data: JSON.stringify({
            "song": songname,
        }),
        success: function (data) {
            queue_len = parseInt(data['queue_len'])
            $("#audioplayer source:first-child").attr('src', data['musicurl'])
            $('#albumimg').attr('src', data['albumimg'])
            $('#testimage').attr('src', data['testimage'])
            $('p[name="song"]').text(data['song'])
            console.log(mediainterval)
            document.title= data['artist']+" - "+data['song']
            clearInterval(mediainterval)
            mediainterval = undefined
            audioplayer.load()
            if (data['album'] == "" && data['videourl'] != "") {
                isvideo = true
                console.log("load video")
                $("#videoplayer").css('display', 'block')
                $("#videoplayer source:first-child").attr('src', data['videourl'])
                videoplayer.load()
                $('#albumimg').css('display', 'none')
                $('p[name="album"]').text("")
                $('p[name="artist"]').text("提供者: " + data['artist'])
                $('div[name="inform_div"]').removeClass("p-4").addClass('p-2')
            } else {
                isvideo = false
                $('div[name="inform_div"]').removeClass("p-2").addClass('p-4')
                $("#videoplayer").css('display', 'none')
                $("#videoplayer source:first-child").attr('src', "")
                console.log($("#videoplayer").css('display'))
                $('#albumimg').css('display', 'block')
                $('p[name="artist"]').text("演出者: " + data['artist'])
                $('p[name="album"]').text("專輯: " + data['album'])
            }
            //test code
            preload_songs()
        },
        error: function (e) {
            console.log('error')
        }
    })

}

function mediacontrol(isplay = true) {
    console.log("56546")
    if (isvideo) {
        if (isplay) {
            videoplayer.play()
            audioplayer.play()
            if (mediainterval == undefined) {
                interval_btn.click()
            }
            console.log(mediainterval, "-------play-------")
        } else {
            console.log(mediainterval, "----------pause-----")
            videoplayer.pause()
            audioplayer.pause()
        }
    } else {
        if (isplay) {
            audioplayer.play()
        } else {
            audioplayer.pause()
        }
    }
}

function mediapause() {
    console.log("mediapause")
    if (isvideo) {
        videoplayer.pause()
        clearInterval(mediainterval)
        mediainterval = undefined
    }
    audioplayer.pause()
    console.log(mediainterval)
}
// audioplayer.play()
//start the function
recordsound.start()