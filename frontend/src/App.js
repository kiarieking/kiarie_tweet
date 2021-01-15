import {useState, useEffect} from 'react'
import logo from './logo.svg';
import './App.css';

function loadtweets(callback){
  const xhr = new XMLHttpRequest()
  const method = 'GET'
  const url = 'http://localhost:8000/api/tweets'
  const responseType = 'json'

  xhr.responseType=responseType
  xhr.open(method, url)
  xhr.onload = function(){
      callback(xhr.response, xhr.status)     
  }
  xhr.onerror = function(e){
    callback({'message':'There was an error while making the request!'},400)
  }
  xhr.send()
}

function App() {
  const [tweets, setTweets] = useState([])
  useEffect(()=>{
    const callback = (response, status)=>{
      if (status===200){
      setTweets(response)
      }
      else{
        alert("There was an error!")
      }
    }
    loadtweets(callback)
  },[])

  return (
    <div className="App">
      <header className="App-header">
        <img src={logo} className="App-logo" alt="logo" />
        <p>
          Edit <code>src/App.js</code> and save to reload.
        </p>
        <p>
          {tweets.map((tweet, index)=>{
            return <li>{tweet.content}</li>
          })}
        </p>
        <a
          className="App-link"
          href="https://reactjs.org"
          target="_blank"
          rel="noopener noreferrer"
        >
          Learn React
        </a>
      </header>
    </div>
  );
}

export default App;
