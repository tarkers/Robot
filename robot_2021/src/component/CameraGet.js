import React, { useState, useEffect } from 'react'
import axios from 'axios'
import PropTypes from 'prop-types'
import { Button } from 'react-bootstrap'
const CameraGet = ({ state }) => {
  const [op, setOp] = useState(false)
  useEffect(() => {
    const giveGrade = async () => {
      window.responsiveVoice.speak("請評分一到五顆星", "Chinese Taiwan Male");
      const receiveGrade = async () => {
        const res = await axios.get('/give_grade')
        setOp(true)
        const answer = res.data.answer
        if (answer != -1) {
          let reply = ""
          reply = answer < 3 ? `您的評分為:${res.data.answer}分。請問您是哪裡不滿意` : `您的評分為:${res.data.answer}分。感謝好評`
          window.responsiveVoice.speak(reply, "Chinese Taiwan Male");
          setTimeout(function () {
            setOp(false)
          }, 1000);
          console.log(res.data.answer, "GOOD Test")
        } else {
          // console.log(res.data.answer, "Count Result")
          setTimeout(() => {
            receiveGrade()
          }, 500);
        }
      }
      receiveGrade()
    }
    if (state == 1 || op) {
      giveGrade()
    }
    console.log(state)
  }, [op, state])

  return (
    <> 
      <div className="float-end">
        {op && <img src={'/video_feed'} alt="Gesture" />}
      </div>
      <Button onClick={() => { setOp(true) }}>評分測試</Button>
    </>
  )
}
CameraGet.state = {
  state: 0
}
CameraGet.prototype = {
  state: PropTypes.number
}
export default CameraGet
