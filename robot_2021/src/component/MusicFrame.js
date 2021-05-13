import React from 'react'
import { useState, useEffect } from 'react'
import VideoPlayer from './VideoPlayer'
import { Button } from 'react-bootstrap'
const MusicFrame = ({ musicdata, volume, playing, changeSong }) => {
    const [playerdata, setPlayerdata] = useState({})
    const audio_div = (
        <>
            <img id="albumimg" src={musicdata.pic} className="rounded  img-thumbnail  mx-auto" alt="albumpic"></img>
            <div name='audio_div' className="p-4 text-center">
                <p name="song" className=" mb-3" style={{ fontSize: "30px" }} >{musicdata.song}</p>
                <p name="album">專輯: {musicdata.album}</p>
                <p name="artist">演出者: {musicdata.artist}</p>
            </div>
        </>
    )
    const video_div = (
        <div name='video_div ' className="text-center mt-2">
            <label style={{ fontSize: "28px" }} >{musicdata.song} - {musicdata.artist}</label>
        </div>
    )
    useEffect(() => {
        musicdata.isVideo == true ? setPlayerdata({
            url: musicdata.url,
            isVideo: true
        }) : setPlayerdata({
            url: musicdata.url,
            isVideo: false
        })
    }, [musicdata])
    return (

        <div className='center-screen music-frame'>
            <VideoPlayer data={playerdata} volume={volume} playing={playing} changeSong={changeSong}></VideoPlayer>
            {musicdata.url != null && <>{musicdata.isVideo ? video_div : audio_div}</>}
        </div>

    )
}

export default MusicFrame
