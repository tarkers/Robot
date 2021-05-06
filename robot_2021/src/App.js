//import './css/App.css';
import { BrowserRouter as Router, Route, Switch } from 'react-router-dom'
import { Jumbotron, Container, Button } from 'react-bootstrap'
import { useState, useEffect } from 'react'
import axios from 'axios'
import Voice from './routes/Voice'
function App() {
  const [test, setTest] = useState("test")
  useEffect(() => {

  }, [test])
  // get the person needs song
  const changeSong = async () => {
    const res = await axios.post('/music/change_song', {
      "song": "阿拉斯加海灣",
    }, {
      headers: {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'Access-Control-Allow-Origin': '*'
      }
    })
    setTest(res.data.song)
    console.log(res.data.song)
  }
  //preload the song
  const preloadSongs = async () => {
    const res = await axios.get('/music/preload_songs')
    console.log(res)
  }
  return (
    <Router>
      <Container>
        <Button onClick={changeSong} variant="primary">{test}</Button>
        <Button onClick={preloadSongs} variant="primary">preload</Button>
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
