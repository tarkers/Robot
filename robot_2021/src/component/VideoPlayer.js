import React from 'react'
import ReactPlayer from 'react-player'
import { useState, useEffect, useRef } from 'react'
import PropTypes from 'prop-types'
const VideoPlayer = ({ data, volume, playing, changeSong }) => {
    const [width, setWidth] = useState('1800px')
    const [height, setHeight] = useState('950px')
    const playerRef = useRef(null)
    useEffect(() => {
        console.log(data, "check")
        if (!data.isVideo) {
            setHeight("0px")
            setWidth("0px")
        } else {
            setHeight("950px")
            setWidth("1800px")
        }
        if ("replay" in data) {
            console.log("-----")
            playerRef.current.seekTo(parseFloat(0))
        }
    }, [data])
    const handleOnEnd = async () => {
        changeSong("Next", false)
    }
    return (
        <div >
            <ReactPlayer
                ref={playerRef}
                style={{ marginTop: "5px" }}
                url={data.url}
                className='react-player'
                width={width}
                height={height}
                volume={volume}
                playing={playing}
                // onStart={() => console.log('onStart')}
                // onPlay={() => { console.log('onPlay') }}
                // onPause={() => console.log("onPause")}
                // onBuffer={() => console.log('onBuffer')}
                onEnded={handleOnEnd}
                // onDuration={() => console.log('onDuration')}
            />

        </div>
    )
}
VideoPlayer.defaultProps = {
    data: {
        isVideo: true,
        url: null
    },
    playing: true
}
VideoPlayer.prototype = {
    data: {
        isVideo: PropTypes.bool,
        url: PropTypes.string
    },
    playing: PropTypes.bool

}
export default VideoPlayer
