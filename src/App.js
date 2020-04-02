import React from 'react';
import logo from './logo.svg';
import Speech from './Speech';
import './App.css';
import axios from 'axios';

function App() {

  const sendit =  ()=>{
     axios({
       method:"post",
       url : '/set_gesture',
       data : {
	   hello: "world"
       }
     });	
  }

  const record = ()=>{
     axios({
      method:"get",
      url : '/record/handup',
     });
  }

  return (
    <div className="App">
      <Speech/>
      <a href="#" onClick={sendit}>send category</a>
      <a href="#" onClick={record}>start recording gesture</a>
      <header className="App-header">
        <img src={logo} className="App-logo" alt="logo" />
        <img src="/video_feed"/>
        <p>
          Edit <code>src/App.js</code> and save to reload.
        </p>
      </header>
    </div>
  );
}

export default App;
