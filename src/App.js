import classes from "./components/styles.css";
import React from "react";
import TypeWriterJS from "./typewritter";
function App() {

  return (
    <div className="App">
        <div className="navbar">

            <a className="logo" href="http://localhost:3000">OKUZ</a>

            <div className="nabigation-block">
                <a className="navbar-button" href="http://localhost:3000">Home</a>
                <a className="navbar-button" href="http://localhost:3000">About me</a>
                <a className="navbar-button" href="http://localhost:3000">Projects</a>
                <a className="navbar-button" href="http://localhost:3000">Blog</a>
            </div>
        </div>
        <div className="block-1">
            <div className="block-1-info">
                <div style={{display:"inline-flex", margin:"none"}} className="hi-block">
                    <h1 style={{fontSize:"60px", fontWeight:"bold"}} className="no-margin-to-bottom">Hi There!</h1>
                    <h1 className="animated-hand no-margin-to-bottom">👋🏻</h1>
                </div>

                <h1 style={{fontSize:"60px", fontWeight:"bold"}} className="no-margin-to-bottom">I am <span className="gradient-text">Oleg Kuzmenko!</span></h1>
                <h3 style={{fontSize:"35px"}}>Python Back-End Developer</h3>
                <TypeWriterJS className="TypeText"></TypeWriterJS>
            </div>
            <img alt="man is sitting in front of PC" style={{width:"300px"}} src="https://soumyajit.vercel.app/static/media/home-main.541f8179af8209ce03ccf2178fe62dbf.svg"/>
        </div>
    </div>
  );
}

export default App;
