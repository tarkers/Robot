import React , { useState, useEffect }  from 'react'
import '../scss/message.scss'
import PropTypes from 'prop-types'
import { useSpring, animated } from 'react-spring'
import robotFace from '../img/robotFace.png'
const Message = ({ speak, handleEnd }) => {
    const [show, setShow] = useState(true)
    useEffect(() => {
        if (!show) {
            setShow(true)
        }
        //test computer code
        if (speak.person == "local") {
            if (speak.words == "電腦") {
                window.responsiveVoice.speak(speak.words, "Chinese Taiwan Male", { onstart: () => handleEnd() });
            } else if (speak.words == "") {
                handleEnd()
            }
            else {
                window.responsiveVoice.speak(speak.words, "Chinese Taiwan Male", { onend: () => handleEnd() });
            }
        }
    }, [speak])
    const MesAnime = () => {
        const showUp = useSpring({
            from: { opacity: 0 },
            to: { opacity: 1 },
            config: { duration: 100 },
            onRest: () => { setShow(false) },
        })
        const vanishAway = useSpring({
            from: { opacity: 1 },
            to: { opacity: 0 },
            reverse: false,
            delay: 3000,
            onStart: () => { console.log("new start") },
            onRest: () => { speak.words = "" },
            config: { duration: 500 },
        })
        return (
            <animated.div style={show ? showUp : vanishAway} className={`user px-2 ${speak.person}`}>
                <div className="avatar">
                    <div className="pic">
                        {speak.person == "remote" ? <img src="https://picsum.photos/100/100?random=16" /> : <img src={robotFace} />}
                    </div>
                    <div className="name pt-1">{speak.name}</div>
                </div>
                <div className="text">{speak.words}</div>
            </animated.div>

        )
    }
    return (
        <>
            {speak.words != "" &&
                <div style={{ position: "relative", zIndex: 2, top: "40px" }}>
                    <MesAnime></MesAnime>
                </div>

            }
        </>
    )
}
Message.defaultProps = {
    speak: {
        name: "User",
        person: 'local',
        words: '',
    }
}
Message.prototype = {
    speak: {
        name: PropTypes.string,
        person: PropTypes.string,
        words: PropTypes.string,
    }
}
export default Message

