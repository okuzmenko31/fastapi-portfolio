import React from 'react';
import TypeWriterJS from "../../typewritter";
import "./Block1.css"

const Block1 = () => {
    return (
        <div className="block-1">
            <div className="block-1-info">
                <div style={{display:"inline-flex", margin:"none"}} className="hi-block high_index">
                    <h1 style={{fontSize:"60px", fontWeight:"bold"}} className="no-margin-to-bottom">Hi There!</h1>
                    <h1 className="animated-hand no-margin-to-bottom">👋🏻</h1>
                </div>

                <h1 style={{fontSize:"60px", fontWeight:"bold"}} className="no-margin-to-bottom high_index">I am <span className="gradient-text">Oleg Kuzmenko!</span></h1>
                <h3 style={{fontSize:"35px"}} className="high_index">Python Back-End Developer</h3>
                <TypeWriterJS className="TypeText"></TypeWriterJS>
            </div>
            <img alt="man is sitting in front of PC" className="high_index" style={{width:"500px", height: "500px"}} src="https://soumyajit.vercel.app/static/media/home-main.541f8179af8209ce03ccf2178fe62dbf.svg"/>
        </div>
    );
};

export default Block1;