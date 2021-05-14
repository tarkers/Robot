import React, { useState, useEffect, useRef } from 'react'
import { Button } from 'react-bootstrap'
import SpeechRecognition, { useSpeechRecognition } from 'react-speech-recognition'
import Message from './Message'
const Robot = ({ setResponse,handleVolume}) => {
  const volumeRef = useRef(0.5)
  const robotCall = useRef(false)
  const nowLabel = useRef(null)
  const timeoutPointer = useRef(null)
  const [userspeak, setuserSpeak] = useState({
    name: "User",
    person: 'remote',
    words: "",
  })
  const [robotspeak, setRobotSpeak] = useState({
    name: "User",
    person: 'local',
    words: "",
  })
  const commands = [
    {
      command: '*電腦*',
      callback: () => buildMessage({ text: `嗨`, index: 0, label: "Robot" }),
      matchInterim: true
    },
    {
      command: ['下一首', '播放下一首', '換首(歌)'],
      callback: () => buildMessage({ text: `好的，為您播放下一首`, index: 3, label: "Next", data: "Next" })
    },
    {
      command: ['重播', '音樂重播', /再[播,放]+一次/],
      callback: () => buildMessage({ text: ``, index: 1, label: "Replay" }),
      matchInterim: true
    },
    {
      command: ['(音樂)(播放)停止(播放)(音樂)', '離開'],
      callback: () => buildMessage({ text: '', index: 15, label: "Exit", data: false })
    },
    {
      command: '(音樂)(播放)暫停(播放)(音樂)',
      callback: () => buildMessage({ text: '', index: 6, label: "Stop", data: false })
    },
    {
      command: '(音樂)繼續(音樂)播(放)',
      callback: () => buildMessage({ text: '', index: 7, label: "Continue", data: true })
    },
    {
      command: ['*(我要)聽*', "*(請)播(放)*"],
      callback: (_addtion, song) => {
        let test = null
        if (song !== "") {
          test = /的歌.?$/.exec(song)
          if (test) {
            let artist = song.substring(0, test.index)
            buildMessage({ text: `好的，請稍等`, index: 1, label: "PlayArtist", data: artist })
          } else {
            buildMessage({ text: `好的，請稍等片刻`, index: 2, label: "PlaySong", data: song })
          }
        }
      }
    },
    {
      command: [/(音量)?調?小[^%]+點?$/, /(音量)?調?大[^%]+點?$/],
      callback: () => {
        let text = ""
        if (finalTranscript.includes('大')) {
          volumeRef.current += 0.15
          if (volumeRef.current > 1) {
            volumeRef.current = 1
            text = "音量已調到最大"
          } else {
            text = `音量調為${(volumeRef.current) * 100}%`
          }
        } else if (finalTranscript.includes('小')) {
          volumeRef.current -= 0.15
          if (volumeRef.current < 0.05) {
            volumeRef.current = 0.05
            text = "音量已調到最小"
          } else {
            text = `音量調為${(volumeRef.current) * 100}%`
          }
        }
        buildMessage({ text: text, index: 8, label: "Set_Volume", data: volumeRef.current })
      }
    },
    {
      command: ['聲音調*%', '音量調*%'],
      callback: (action) => {
        let number = action.match(/\d+/g)
        if (number.length != 0) {
          number = number[0]
        }
        volumeRef.current = number / 100
        buildMessage({ text: `音量調為${volumeRef.current * 100}%`, index: 8, label: "Set_Volume", data: volumeRef.current })
      },
    },
    {
      command: ['*(現在)(聲)音(量)(是)多少', '*(現在)(聲)音(量)多大'],
      callback: () => buildMessage({ text: `現在的音量為${volumeRef.current * 100}%`, index: 9, label: "Get_Volume" }),
    },
  ]
  const { finalTranscript, resetTranscript } = useSpeechRecognition({ commands })

  const responsePeriod = () => {
    timeoutPointer.current = setTimeout(() => {
      clearTimeout(timeoutPointer.current)
      resetTranscript()
      timeoutPointer.current = null
      buildMessage({ text: ``, index: 12, label: "No_Speak" })
      handleVolume(volumeRef.current)
    }, 8000)
  }
  const buildMessage = (message) => {
    nowLabel.current=message.label
    if (timeoutPointer.current) {
      clearTimeout(timeoutPointer.current)
    }
    if (message.label == "Robot") {
      robotCall.current = true
      setuserSpeak({ name: "User", person: 'remote', words: "電腦" })
      setResponse(message, "電腦")
      setRobotSpeak({name: "Robot",  person: 'local',words: message.text})
      responsePeriod()
    } else if (robotCall.current) {
      robotCall.current = false
      setuserSpeak({ name: "User",  person: 'remote',words: finalTranscript})
      setResponse(message)
      setRobotSpeak({name: "Robot",person: 'local',words: message.text})
    }
    resetTranscript()
  }
  useEffect(() => {
    SpeechRecognition.startListening({ language: 'zh-CN', continuous: true })
  }, [])
  if (!SpeechRecognition.browserSupportsSpeechRecognition()) {
    return null
  }
  const getEnd=()=>{
    console.log(nowLabel.current,volumeRef.current,"getend")
    nowLabel.current=="Robot"?handleVolume(0.15):handleVolume(volumeRef.current)
  }
  return (
    <div>
      <Message speak={userspeak}></Message>
      <Message speak={robotspeak} handleEnd={getEnd}></Message>
    </div>
  )
}
export default Robot