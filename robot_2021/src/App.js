//import './css/App.css';
import { BrowserRouter as Router, Route, Switch } from 'react-router-dom'
import { Container, Button } from 'react-bootstrap'
import { useState, useEffect, useRef } from 'react'
import axios from 'axios'
import Message from './component/Message'
import Voice from './routes/Voice'
import Robot from './component/Robot'
import CameraGet from './component/CameraGet'
import MusicFrame from './component/MusicFrame'
import RobotFace from './component/RobotFace'

function App() {
  const [playing, setPlaying] = useState(false)
  const [robotshow, setRobotShow] = useState(true)
  const [state, setstate] = useState(0)
  const [musicdata, setMusicdata] = useState(null)
  const [volume, setVolume] = useState(0.5)
  const lastVolume = useRef(0.5)
  useEffect(() => {
    playing ? setRobotShow(false) : setRobotShow(true)
  }, [playing])
  // get the person needs song
  const changeSong = async (data, is_artist) => {
    const res = await axios.post('/music/change_song', {
      "song": data,
      "is_artist": is_artist
    }, {
      headers: {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'Access-Control-Allow-Origin': '*'
      }
    })
    res.data['date'] = new Date().toLocaleString()
    console.log(res.data)
    if (res.data.noError) {
      setMusicdata(res.data)
      setPlaying(true)
      //preload the songlist
      if (res.data.queueLen < 2) {
        preloadSongs()
      }
    } else {
      // window.responsiveVoice.speak("抱歉，找不到您的歌", "Chinese Taiwan Male");
    }

  }
  const handleVolume=(v)=>{
    setVolume(v)
  }
  //preload the song
  const preloadSongs = async () => {
    const res = await axios.get('/music/preload_songs')
    console.log("---Preload OK!---")
  }
  const setResponse = (message) => {
    console.log(message)
    switch (message.label) {
      case "PlayArtist":
        changeSong(message.data, true)
        break;
      case "PlaySong":
      case "Next":
        changeSong(message.data, false)
        break;
      case "Stop":
      case "Continue":
        if (musicdata == null) {
          window.responsiveVoice.speak("請選擇歌曲", "Chinese Taiwan Male", { onend: () => setVolume(lastVolume.current)});
        } else {
          setPlaying(message.data)
        }
        break
      case "Replay":
        console.log("replay")
        setMusicdata({ ...musicdata, date: new Date().toLocaleString(), replay: true })
        break
      case "Exit":
        setPlaying(false)
        setMusicdata(null)
        break
      default:
        break;
    }
  }
  return (
    <Router>
      <Container fluid>
        {robotshow && <RobotFace></RobotFace>}
        <Robot setResponse={setResponse} handleVolume={handleVolume}></Robot>
        <div style={{ zIndex: -1 }}>
          {musicdata != null && <MusicFrame musicdata={musicdata} volume={volume} playing={playing} changeSong={changeSong}></MusicFrame>}
          <CameraGet></CameraGet>
        </div>
        <div className="App" style={{ padding: '5px' }}>
          <Switch>
            <Route path='/voice' component={Voice} />
          </Switch>
        </div>
      </Container>
    </Router>
  );
}
export default App;
