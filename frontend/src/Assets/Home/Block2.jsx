import React from 'react';
import "../../components/styles.css"
import "./Block2.css"
import Tilt from "react-parallax-tilt";
import { AiFillGithub, AiFillLinkedin, AiFillInstagram, AiFillTwitterCircle } from "react-icons/ai"

const Block2 = () => {
    return (
        <div className="block-2-base">
            <div className="block-2 high_index">
                <div className="block-2-info high_index">
                    <div className="block2-introduce-info">
                        <h1 style={{fontSize:"60px", fontWeight:"bold"}} className="no-margin-to-bottom">Let me <span className="choosed-text">introduce</span> myself!</h1>
                        <h3>I fell in love with programming and I have at least learnt something, I think… 🤷‍♂️</h3>
                        <h3>I am fluent in classics like C++, Javascript and Go.</h3>
                        <h3>My field of Interest's are building new  Web Technologies and Products and also in areas related to Blockchain.</h3>
                        <h3>Whenever possible, I also apply my passion for developing products with Node.js and Modern Javascript Library and Frameworks  like React.js and Next.js</h3>
                    </div>
                </div>
                <div className="block2-interactive-img">
                    <Tilt>
                        <img src="https://soumyajit.vercel.app/static/media/avatar.5852f40fbb38aa284829fa3fb7722225.svg" />
                    </Tilt>
                </div>
            </div>
            <div style={{display:"flex", justifyContent:"center", alignItems:"center", flexDirection:"column"}} className="high_index">
                <h5 style={{fontSize:"50px"}} className="no-margin-to-bottom">FIND ME ON</h5>
                <h5>Feel free to <a style={{color:"#a855f7", textDecoration:"none"}} href="https://t.me/okuzmenko31" target="_blank">connect</a> with me</h5>
                <div style={{fontSize:"50px", marginBottom:"300px"}}>
                    <a style={{color:"black", textDecoration:"none"}} href="#" target="_blank"><AiFillGithub /></a>
                    <a style={{color:"black", textDecoration:"none"}} href="#" target="_blank"><AiFillLinkedin /></a>
                    <a style={{color:"black", textDecoration:"none"}} href="#" target="_blank"><AiFillInstagram /></a>
                    <a style={{color:"black", textDecoration:"none"}} href="#" target="_blank"><AiFillTwitterCircle /></a>
                </div>
            </div>
        </div>
    );
};

export default Block2;